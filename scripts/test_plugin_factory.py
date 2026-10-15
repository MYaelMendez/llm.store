"""Exercise generated archives and rejection paths without network or credentials."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
from build_plugins import ROOT, build, contained, validate


class PluginFactoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.output = Path(self.tmp.name)
        self.receipts = build(ROOT, self.output)
        with zipfile.ZipFile(self.output / self.receipts[0]['archive']) as zipped:
            self.entries = {n: zipped.read(n) for n in zipped.namelist()}

    def test_reproducible_full_archives(self):
        before = {r['archive']: (self.output / r['archive']).read_bytes() for r in self.receipts}
        again = build(ROOT, self.output)
        self.assertEqual(len(again), 4)
        for r in again:
            self.assertEqual(before[r['archive']], (self.output / r['archive']).read_bytes())
            self.assertEqual(r['publication_status'], 'draft_not_submitted')
            self.assertIn('publisher_identity', r['remaining'])
            with zipfile.ZipFile(self.output / r['archive']) as zipped:
                source = ROOT / 'plugins' / r['id']
                self.assertEqual(zipped.read('assets/gpt-icon.png'), (source / 'assets/gpt-icon.png').read_bytes())
                for p in (source / 'skills').rglob('*'):
                    if p.is_file():
                        self.assertEqual(zipped.read(p.relative_to(source).as_posix()), p.read_bytes())
                private = json.loads((source / 'plugin.json').read_text())
                public = json.loads(zipped.read('plugin.json'))
                self.assertEqual(private['name'], public['name'])
                self.assertEqual(private['extensions']['com.openai']['interface']['defaultPrompt'],
                                 public['extensions']['com.openai']['interface']['defaultPrompt'])

    def test_rejects_binding_in_compatibility_manifest(self):
        entries = copy.deepcopy(self.entries)
        legacy = json.loads(entries['.codex-plugin/plugin.json'])
        legacy['apps'] = []
        entries['.codex-plugin/plugin.json'] = json.dumps(legacy).encode()
        with self.assertRaises(ValueError):
            validate(entries)

    def test_rejects_missing_icon(self):
        del self.entries['assets/gpt-icon.png']
        with self.assertRaises(ValueError):
            validate(self.entries)

    def test_rejects_missing_handoff_reference(self):
        del self.entries['skills/instructions/references/studio-handoff.md']
        with self.assertRaises(ValueError):
            validate(self.entries)

    def test_rejects_escape(self):
        for path in ('../token', '/tmp/token', 'skills/../../token', 'skills\\token'):
            with self.assertRaises(ValueError):
                contained(ROOT, path)


if __name__ == '__main__':
    unittest.main()
