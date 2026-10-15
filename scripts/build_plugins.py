"""Build deterministic skills-only public-upload drafts; Python standard library only."""
import argparse
import copy
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import struct
import subprocess
import zipfile
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
URL_FIELDS = ('websiteURL', 'supportURL', 'privacyPolicyURL', 'termsOfServiceURL')


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def contained(root, relative):
    path = PurePosixPath(relative)
    if path.is_absolute() or '..' in path.parts or '\\' in relative or not path.parts:
        raise ValueError('Unsafe package path')
    result = root.joinpath(*path.parts)
    if not result.resolve().is_relative_to(root.resolve()):
        raise ValueError('Path escapes source root')
    return result


def collect(root):
    result = {}
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            raise ValueError('Symlinks are not supported')
        if path.is_file():
            name = path.relative_to(root).as_posix()
            if any(part in ('.git', '__pycache__', 'node_modules') for part in path.parts):
                raise ValueError('Unexpected generated/private source path')
            if path.name.startswith('.env') or path.suffix in ('.pem', '.key'):
                raise ValueError('Credential-like file is not allowed')
            result[name] = path.read_bytes()
    return result


def valid_url(value):
    if not isinstance(value, str) or len(value) > 1024:
        return False
    url = urlsplit(value)
    return bool(url.scheme == 'https' and url.hostname and not url.username and
                not url.password and url.hostname not in ('localhost', 'example.com', '127.0.0.1'))


def validate(entries):
    """Local structural checks, not the full OpenAI schema or approval."""
    if '.app.json' in entries or 'mcp.json' in entries:
        raise ValueError('This factory currently accepts skills-only packages')
    manifests = [json.loads(entries['plugin.json'])]
    if '.codex-plugin/plugin.json' in entries:
        manifests.append(json.loads(entries['.codex-plugin/plugin.json']))
    manifest = manifests[0]
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', manifest['name']):
        raise ValueError('Invalid plugin identity')
    if not re.fullmatch(r'\d+\.\d+\.\d+', manifest['version']):
        raise ValueError('Explicit semantic version required')
    for item in manifests:
        ext = item.get('extensions', {}).get('com.openai', {})
        if any(item.get(key) is not None for key in ('apps', 'hooks')) or any(
                ext.get(key) is not None for key in ('apps', 'hooks')):
            raise ValueError('Public upload contains app bindings or hooks')
        if item['name'] != manifest['name'] or item['version'] != manifest['version']:
            raise ValueError('Compatibility manifest identity/version mismatch')
    ui = manifest['extensions']['com.openai']['interface']
    for field, limit in (('displayName', 30), ('shortDescription', 30),
                         ('longDescription', 4000), ('developerName', 80)):
        if not isinstance(ui.get(field), str) or not ui[field].strip() or len(ui[field]) > limit:
            raise ValueError('Invalid listing field: ' + field)
    prompts = ui.get('defaultPrompt', [])
    if not isinstance(prompts, list) or len(prompts) > 3:
        raise ValueError('Invalid starter prompts')
    normalized = [' '.join(p.split()) for p in prompts]
    if len(set(normalized)) != len(prompts) or any(
            not p.strip() or len(p) > 128 or '\n' in p or '\r' in p for p in prompts):
        raise ValueError('Invalid starter prompts')
    for field, minimum in (('logo', 256), ('composerIcon', 48)):
        name = str(PurePosixPath(ui[field]))
        contained(Path('/package'), name)
        data = entries.get(name, b'')
        if len(data) < 24 or data[:8] != b'\x89PNG\r\n\x1a\n' or data[12:16] != b'IHDR':
            raise ValueError('Missing PNG icon: ' + name)
        width, height = struct.unpack('>II', data[16:24])
        if width != height or width < minimum or len(data) > 5 * 1024 * 1024:
            raise ValueError('Invalid icon dimensions/size')
    skills = [name for name in entries if name.startswith('skills/') and name.endswith('/SKILL.md')]
    if not skills:
        raise ValueError('Missing skill')
    for name in skills:
        text = entries[name].decode()
        front = text.split('---', 2)
        if len(front) != 3 or not text.startswith('---\n'):
            raise ValueError('Missing skill frontmatter')
        skill_name = PurePosixPath(name).parent.name
        if not re.search(r'^name:\s*' + re.escape(skill_name) + r'\s*$', front[1], re.M):
            raise ValueError('Skill folder/name mismatch')
        if not re.search(r'^description:\s*\S', front[1], re.M):
            raise ValueError('Missing skill description')
        reference = str(PurePosixPath(name).parent / 'references/studio-handoff.md')
        if reference not in entries:
            raise ValueError('Missing handoff reference')
    return manifest


def build(root, output):
    catalog = json.loads((root / 'plugins/catalog.json').read_text())
    settings = json.loads((root / 'publication/settings.json').read_text())
    revision = None
    try:
        head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, stderr=subprocess.DEVNULL).decode().strip()
        dirty = subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=normal'], cwd=root).strip()
        if not dirty:
            revision = head
    except subprocess.CalledProcessError:
        pass
    output.mkdir(parents=True, exist_ok=True)
    receipts = []
    seen = set()
    for plugin in catalog['plugins']:
        slug = plugin['id']
        if not re.fullmatch(r'[a-z0-9-]+', slug) or slug in seen:
            raise ValueError('Invalid or duplicate catalog id')
        seen.add(slug)
        entries = collect(contained(root, plugin['source']))
        source_hashes = {name: sha(data) for name, data in entries.items()}
        manifest = json.loads(entries['plugin.json'])
        overlay = json.loads(contained(root, plugin['listing']).read_text())
        ext = manifest['extensions']['com.openai']
        ext['interface'].update(overlay.get('interface', {}))
        ext['publication'] = copy.deepcopy(overlay.get('publication', {}))
        if settings.get('countries') is not None:
            ext['publication']['countries'] = settings['countries']
        if settings.get('commerce') is not None:
            ext.setdefault('review', {})['commerce'] = settings['commerce']
        entries['plugin.json'] = encoded(manifest)
        if '.codex-plugin/plugin.json' in entries:
            legacy = json.loads(entries['.codex-plugin/plugin.json'])
            legacy['interface'] = copy.deepcopy(ext['interface'])
            entries['.codex-plugin/plugin.json'] = encoded(legacy)
        provenance = {'format': 'ae-plugin-source-v1', 'repository': catalog['repository'],
                      'source_revision': revision, 'imported_release_id': plugin['imported_release_id'],
                      'source_files': source_hashes}
        entries['SOURCE.json'] = encoded(provenance)
        validate(entries)
        filename = slug + '-' + manifest['version'] + '-draft.zip'
        archive = output / filename
        with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_STORED) as zipped:
            for name, data in sorted(entries.items()):
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                zipped.writestr(info, data)
        with zipfile.ZipFile(archive) as zipped:
            readback = {name: zipped.read(name) for name in zipped.namelist()}
            if readback != entries or zipped.testzip() is not None:
                raise ValueError('ZIP readback mismatch')
            validate(readback)
        ui = manifest['extensions']['com.openai']['interface']
        gaps = [field for field in URL_FIELDS if not valid_url(ui.get(field))]
        gaps += ['verify_' + field for field in URL_FIELDS if valid_url(ui.get(field)) and
                 ui[field] not in settings.get('verified_urls', [])]
        gaps += [field for field in ('publisher_identity', 'countries', 'commerce') if settings.get(field) is None]
        # These checks must be confirmed externally, never inferred from a local build.
        gaps += ['confirm_listing_category', 'confirm_icon_light_dark_legibility',
                 'confirm_redistribution_rights', 'portal_validation_and_attestations', 'openai_review']
        receipt = {'id': slug, 'archive': filename, 'sha256': sha(archive.read_bytes()),
                   'source_revision': revision, 'file_sha256': {n: sha(d) for n, d in sorted(entries.items())},
                   'package_checks': 'passed', 'publication_status': 'draft_not_submitted',
                   'type': 'skills-only', 'mcp_review_cases_demo_credentials': 'not_applicable',
                   'remaining': gaps, 'runtime_evaluation': 'not_run',
                   'validation_scope': 'Local structural and ZIP readback checks; not full schema validation or approval.'}
        (output / (slug + '-readiness.json')).write_bytes(encoded(receipt))
        receipts.append(receipt)
    (output / 'index.json').write_bytes(encoded(receipts))
    return receipts


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'plugin-dist')
    parser.add_argument('--require-ready', action='store_true')
    args = parser.parse_args()
    receipts = build(ROOT, args.output.resolve())
    for receipt in receipts:
        print(receipt['id'] + ': package checks passed; public submission incomplete')
    if args.require_ready and any(item['remaining'] for item in receipts):
        raise SystemExit(2)
