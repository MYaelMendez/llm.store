import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'tools/validate.py'
MANIFEST = Path('computers/default/manifest.json')
GOVERNANCE = Path('computers/default/governance/dao.template.json')

class FoundationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / 'foundation'
        shutil.copytree(ROOT, self.root)
        self.addCleanup(self.temp.cleanup)

    def run_validator(self, expected):
        result = subprocess.run([sys.executable, '-I', '-B', str(SCRIPT), str(self.root)],
                                capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def write(self, path, value):
        (self.root / path).write_text(json.dumps(value, indent=2) + '\n')

    def manifest(self):
        return json.loads((self.root / MANIFEST).read_text())

    def rebind_governance(self):
        manifest = self.manifest()
        manifest['governance']['sha256'] = hashlib.sha256((self.root / GOVERNANCE).read_bytes()).hexdigest()
        self.write(MANIFEST, manifest)

    def test_valid_proposal_is_not_runtime_authority(self):
        before = (self.root / MANIFEST).read_bytes()
        result = json.loads(self.run_validator(0).stdout)
        self.assertEqual(result['status'], 'VALID_UNBOUND_PROPOSAL')
        self.assertIs(result['provisioningAuthorized'], False)
        self.assertIs(result['runtimeVerified'], False)
        self.assertEqual(before, (self.root / MANIFEST).read_bytes())

    def test_privilege_and_execution_escalation_matrix(self):
        original = self.manifest()
        cases = [
            ('authority', 'root', 'agent://root'), ('authority', 'inherit', True),
            ('authority', 'inherit', 0), ('authority', 'grants', ['execute']),
            ('authority', 'provisionerRetainsRuntimeAuthority', True),
            ('provisioning', 'status', 'READY'), ('provisioning', 'adapter', 'shell'),
            ('verification', 'status', 'VERIFIED'), ('verification', 'evidence', ['claimed']),
            ('publication', 'status', 'RELEASED'), ('publication', 'publisherIdentity', 'claimed'),
            ('resourceLimits', 'memoryBytes', 1024), ('resourceLimits', 'cpuMillis', True),
            ('charter', 'path', '../outside'), ('governance', 'path', 'https://example.com/policy'),
        ]
        for parent, key, value in cases:
            with self.subTest(parent=parent, key=key, value=value):
                m = copy.deepcopy(original); m[parent][key] = value
                self.write(MANIFEST, m); self.run_validator(1)
        for key, value in [('image', {'url':'https://example.com/image'}), ('agents', ['agent']),
                           ('modules', ['tool']), ('status', 'ACTIVE'), ('secret', 'private-sentinel'),
                           ('purpose', ' '), ('id', 'ae.default\n')]:
            with self.subTest(key=key):
                m = copy.deepcopy(original); m[key] = value
                self.write(MANIFEST, m); result = self.run_validator(1)
                self.assertNotIn('private-sentinel', result.stderr + result.stdout)

    def test_charter_tampering_fails_without_rewriting_bindings(self):
        p = self.root / 'CHARTER.md'; p.write_text(p.read_text() + '\nchanged\n')
        original = (self.root / MANIFEST).read_bytes()
        self.run_validator(1)
        self.assertEqual(original, (self.root / MANIFEST).read_bytes())

    def test_governance_cannot_become_a_live_dao_even_with_fresh_digest(self):
        original = json.loads((self.root / GOVERNANCE).read_text())
        for key, value in [('status','ACTIVE'), ('members',['claimed-owner']), ('decisionRule', {'threshold':1}),
                           ('delegatedScopes',['all']), ('recoveryPolicy','operator-backdoor'),
                           ('grantExpiry','never'), ('revocationPolicy','none'), ('authorityRoot','dao://unbound'),
                           ('legalEntityStatus','FORMED'), ('runtimeEnforcement','ENFORCED'), ('version','0.2.0')]:
            with self.subTest(key=key):
                g = copy.deepcopy(original); g[key] = value
                self.write(GOVERNANCE, g); self.rebind_governance(); self.run_validator(1)

    def test_duplicate_json_members_are_rejected(self):
        p = self.root / MANIFEST
        p.write_text(p.read_text().replace('"inherit": false', '"inherit": true, "inherit": false'))
        self.run_validator(1)

    def test_oversized_and_malformed_json_are_rejected(self):
        for raw in [' ' * 65537, '{bad', '{"value":NaN}', '[' * 2000]:
            with self.subTest(size=len(raw)):
                (self.root / MANIFEST).write_text(raw); self.run_validator(1)

    def test_external_symlink_is_rejected_even_with_matching_digest(self):
        external = Path(self.temp.name) / 'outside'
        external.write_bytes((self.root / 'CHARTER.md').read_bytes())
        (self.root / 'CHARTER.md').unlink()
        (self.root / 'CHARTER.md').symlink_to(external)
        self.run_validator(1)

    def test_missing_policy_and_digest_tampering_are_rejected(self):
        m = self.manifest(); m['charter']['sha256'] = '0' * 64
        self.write(MANIFEST, m); self.run_validator(1)
        (self.root / GOVERNANCE).unlink(); self.run_validator(1)

    def test_unknown_schema_keywords_and_remote_refs_fail_closed(self):
        p = Path('registry/schema/computer-manifest.schema.json')
        original = json.loads((self.root / p).read_text())
        for key, value in [('$ref','https://example.com/schema'), ('anyOf', [{}]), ('$schema','unknown')]:
            with self.subTest(key=key):
                s = copy.deepcopy(original); s[key] = value
                self.write(p, s); self.run_validator(1)

    def test_missing_and_unknown_nested_members_are_rejected(self):
        original = self.manifest()
        for value in [{}, {**original['authority'], 'admin':True}]:
            m = copy.deepcopy(original); m['authority'] = value
            self.write(MANIFEST, m); self.run_validator(1)

if __name__ == '__main__':
    unittest.main()
