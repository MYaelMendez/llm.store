"""Offline, read-only validator for the foundation's deliberately unbound proposals.

Supports ONLY the included schema vocabulary; rejects unsupported keywords. Not a
complete JSON Schema implementation, signature verifier, installer or provisioner.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

LIMIT = 65536
KEYWORDS = {'$schema', 'title', 'description', 'type', 'const', 'properties',
            'required', 'additionalProperties', 'pattern', 'minLength', 'maxLength',
            'maxItems'}

class Invalid(ValueError):
    pass


def pairs(values):
    result = {}
    for key, value in values:
        if key in result:
            raise Invalid('Duplicate JSON member')
        result[key] = value
    return result


def raw_file(root, relative):
    path = root / relative
    if path.is_symlink() or any(p.is_symlink() for p in path.parents if p != root.parent):
        raise Invalid('Symlink paths are forbidden')
    resolved = path.resolve(strict=True)
    if not resolved.is_relative_to(root) or not resolved.is_file():
        raise Invalid('Artifact must be a regular file inside the foundation')
    # Bound the read itself, not just the result after allocating an entire file.
    with resolved.open('rb') as stream:
        value = stream.read(LIMIT + 1)
    if len(value) > LIMIT:
        raise Invalid('Artifact exceeds 64 KiB')
    return value


def load(root, relative):
    return json.loads(raw_file(root, relative), object_pairs_hook=pairs,
                      parse_constant=lambda _: (_ for _ in ()).throw(Invalid('Non-finite JSON number')))


def check_schema(schema, depth=0):
    if depth > 20 or type(schema) is not dict or set(schema) - KEYWORDS:
        raise Invalid('Unsupported schema vocabulary or excessive nesting')
    if schema.get('type') not in {'object', 'array', 'string', 'null', 'boolean', 'integer'}:
        raise Invalid('Unsupported schema type')
    if schema['type'] == 'object':
        props = schema.get('properties')
        required = schema.get('required')
        if type(props) is not dict or type(required) is not list or set(required) != set(props) or len(required) != len(set(required)) or schema.get('additionalProperties') is not False:
            raise Invalid('Every object must be closed and every field required')
        for child in props.values():
            check_schema(child, depth + 1)
    if 'pattern' in schema:
        re.compile(schema['pattern'])


def validate(value, schema, depth=0):
    if depth > 20:
        raise Invalid('Excessive instance nesting')
    kinds = {'object': dict, 'array': list, 'string': str, 'null': type(None),
             'boolean': bool, 'integer': int}
    if type(value) is not kinds[schema['type']]:
        raise Invalid('Value type does not match schema')
    if 'const' in schema and json.dumps(value, sort_keys=True) != json.dumps(schema['const'], sort_keys=True):
        raise Invalid('Constant policy value changed')
    if type(value) is dict:
        if set(value) != set(schema['properties']):
            raise Invalid('Missing or unexpected object members')
        for name, child in schema['properties'].items():
            validate(value[name], child, depth + 1)
    if type(value) is str:
        if not value.strip() or any(ord(c) < 32 or ord(c) == 127 for c in value):
            raise Invalid('Blank or control-character metadata')
        if not schema.get('minLength', 0) <= len(value) <= schema.get('maxLength', LIMIT):
            raise Invalid('String length out of bounds')
        if 'pattern' in schema and re.search(schema['pattern'], value) is None:
            raise Invalid('String pattern mismatch')
    if type(value) is list and len(value) > schema.get('maxItems', 0):
        raise Invalid('Array exceeds permitted length')


def inspect(root):
    root = Path(root).absolute()
    if root.is_symlink():
        raise Invalid('Foundation root must not be a symlink')
    root = root.resolve(strict=True)
    manifest_schema = load(root, 'registry/schema/computer-manifest.schema.json')
    governance_schema = load(root, 'registry/schema/governance-template.schema.json')
    for schema in (manifest_schema, governance_schema):
        if schema.get('$schema') != 'https://json-schema.org/draft/2020-12/schema':
            raise Invalid('Unknown schema dialect')
        check_schema(schema)
    manifest = load(root, 'computers/default/manifest.json')
    validate(manifest, manifest_schema)
    # Fixed local paths: metadata never chooses a file, command, URL or schema to load.
    governance = load(root, 'computers/default/governance/dao.template.json')
    validate(governance, governance_schema)
    if governance['authorityRoot'] != 'human://root' or governance['status'] != 'PROPOSED' or governance['members'] or governance['decisionRule'] is not None or governance['delegatedScopes'] or any(governance[k] is not None for k in ['grantExpiry', 'revocationPolicy', 'recoveryPolicy']):
        raise Invalid('Inactive human-root governance required')
    if manifest['version'] != governance['version']:
        raise Invalid('Manifest and governance versions differ')
    for binding, path in [('charter', 'CHARTER.md'), ('governance', 'computers/default/governance/dao.template.json')]:
        if manifest[binding]['path'] != path or manifest[binding]['sha256'] != hashlib.sha256(raw_file(root, path)).hexdigest():
            raise Invalid('Policy binding does not match the reviewed file')
    # Independent semantic guard: a relaxed schema must not turn a proposal into a grant.
    if manifest['image'] is not None or manifest['status'] != 'PROPOSED' or manifest['authority'] != {'root': 'human://root', 'inherit': False, 'grants': [], 'provisionerRetainsRuntimeAuthority': False}:
        raise Invalid('Unbound human-root proposal required')
    if manifest['provisioning'] != {'status': 'NOT_IMPLEMENTED', 'adapter': None} or manifest['verification'] != {'status': 'NOT_EXECUTED', 'evidence': []} or manifest['agents'] or manifest['modules']:
        raise Invalid('Executable or verified state is not supported')
    if manifest['publication'] != {'status': 'DRAFT', 'publisherIdentity': None, 'artifactDigest': None} or any(type(v) is not int or v != 0 for v in manifest['resourceLimits'].values()):
        raise Invalid('Runnable release or resource budget is not supported')
    return {'status': 'VALID_UNBOUND_PROPOSAL', 'runtimeVerified': False,
            'provisioningAuthorized': False, 'manifestSha256': hashlib.sha256(raw_file(root, 'computers/default/manifest.json')).hexdigest()}


if __name__ == '__main__':
    try:
        if len(sys.argv) > 2:
            raise Invalid('Expected at most one foundation path')
        print(json.dumps(inspect(sys.argv[1] if len(sys.argv) == 2 else Path(__file__).resolve().parents[1])))
    except (ValueError, OSError, RecursionError, TypeError, KeyError, re.error, AttributeError):
        # Never echo untrusted file contents or accidentally committed credentials.
        print('INVALID_FOUNDATION: schema, policy binding, path or unbound-state check failed.', file=sys.stderr)
        sys.exit(1)
