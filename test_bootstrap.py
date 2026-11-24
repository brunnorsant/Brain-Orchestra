"""Reproducible acceptance checks using fresh synthetic workspaces only."""
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parent
SCRIPT = REPO / 'bootstrap.py'
spec = importlib.util.spec_from_file_location('orchestra_bootstrap', SCRIPT)
bootstrap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bootstrap)


class BootstrapAcceptance(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='orchestra-acceptance-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.target = self.base / 'private-workspace'

    def cli(self, *args):
        # Isolated Python, no user site packages or provider/profile environment.
        env = {key: os.environ[key] for key in ('SYSTEMROOT', 'WINDIR') if key in os.environ}
        return subprocess.run(
            [sys.executable, '-I', '-X', 'utf8', str(SCRIPT), *map(str, args)],
            cwd=REPO, env=env, capture_output=True, text=True, encoding='utf-8',
        )

    def snapshot(self):
        return {p.relative_to(self.target).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
                for p in self.target.rglob('*') if p.is_file()}

    def test_full_cli_creates_18_roles_and_34_files(self):
        run = self.cli('--target', self.target, '--full')
        self.assertEqual(run.returncode, 0, run.stderr)
        result = json.loads(run.stdout)
        self.assertEqual((result['agents'], result['files']), (18, 34))
        self.assertFalse(result['external_accounts_connected'])
        self.assertFalse(result['terminals_started'])
        roles = [p for p in (self.target / 'roles').glob('*.md') if p.name != 'README.md']
        self.assertEqual(len(roles), 18)
        self.assertEqual(len(self.snapshot()), 34)

    def test_core_cli_creates_three_roles(self):
        run = self.cli('--target', self.target)
        self.assertEqual(run.returncode, 0, run.stderr)
        result = json.loads(run.stdout)
        self.assertEqual((result['agents'], result['files']), (3, 19))
        manifest = json.loads((self.target / 'setup-manifest.json').read_text(encoding='utf-8'))
        self.assertEqual(set(manifest['agents']), {'maestro', 'carrosseis', 'revisao'})

    def test_dry_run_does_not_create_destination(self):
        run = self.cli('--target', self.target, '--full', '--dry-run')
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)['mode'], 'dry-run')
        self.assertFalse(self.target.exists())

    def test_spaces_and_unicode_in_destination(self):
        target = self.base / 'Equipe de demonstração com espaços'
        run = self.cli('--target', target, '--full')
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertTrue((target / 'brain' / 'RECALL.md').is_file())

    def test_repeat_preserves_contents_and_mtimes(self):
        bootstrap.generate(self.target, full=True)
        before = self.snapshot()
        bootstrap.generate(self.target, full=True)
        self.assertEqual(before, self.snapshot())

    def test_modified_file_is_not_overwritten(self):
        bootstrap.generate(self.target, full=True)
        role = self.target / 'roles' / 'maestro.md'
        role.write_text('Synthetic user modification\n', encoding='utf-8')
        before = self.snapshot()
        with self.assertRaises(ValueError):
            bootstrap.generate(self.target, full=True)
        self.assertEqual(before, self.snapshot())

    def test_preflight_refuses_partial_write_on_conflict(self):
        bootstrap.generate(self.target, full=True)
        missing = self.target / 'AGENTS.md'
        missing.unlink()
        (self.target / 'roles' / 'maestro.md').write_text('modified', encoding='utf-8')
        before = self.snapshot()
        with self.assertRaises(ValueError):
            bootstrap.generate(self.target, full=True)
        self.assertFalse(missing.exists())
        self.assertEqual(before, self.snapshot())

    def test_unrelated_nonempty_folder_is_preserved(self):
        self.target.mkdir()
        (self.target / 'existing.txt').write_text('synthetic existing content', encoding='utf-8')
        before = self.snapshot()
        run = self.cli('--target', self.target)
        self.assertNotEqual(run.returncode, 0)
        self.assertIn('Setup interrompido:', run.stderr)
        self.assertEqual(before, self.snapshot())

    def test_target_file_is_refused(self):
        self.target.write_text('synthetic existing file', encoding='utf-8')
        run = self.cli('--target', self.target)
        self.assertNotEqual(run.returncode, 0)
        self.assertIn('Setup interrompido:', run.stderr)
        self.assertEqual(self.target.read_text(encoding='utf-8'), 'synthetic existing file')

    def test_target_inside_public_checkout_is_refused_before_write(self):
        target = REPO / 'forbidden-test-workspace'
        self.assertFalse(target.exists())
        run = self.cli('--target', target)
        self.assertNotEqual(run.returncode, 0)
        self.assertFalse(target.exists())

    def test_checkout_and_ancestor_destinations_are_refused(self):
        for target in (REPO, REPO.parent):
            with self.subTest(target=target.name), self.assertRaises(ValueError):
                bootstrap.generate(target)

    def test_profile_change_does_not_mutate_existing_workspace(self):
        bootstrap.generate(self.target)
        before = self.snapshot()
        with self.assertRaises(ValueError):
            bootstrap.generate(self.target, full=True)
        self.assertEqual(before, self.snapshot())

    def test_invalid_manifest_is_refused_without_mutation(self):
        bootstrap.generate(self.target)
        (self.target / 'setup-manifest.json').write_text('{invalid', encoding='utf-8')
        before = self.snapshot()
        run = self.cli('--target', self.target)
        self.assertNotEqual(run.returncode, 0)
        self.assertEqual(before, self.snapshot())

    def test_json_routes_and_integrations_are_generic_and_disabled(self):
        bootstrap.generate(self.target, full=True)
        for path in self.target.rglob('*.json'):
            json.loads(path.read_text(encoding='utf-8'))
        routes = json.loads((self.target / 'config' / 'routes.example.json').read_text(encoding='utf-8'))
        integrations = json.loads((self.target / 'config' / 'integrations.example.json').read_text(encoding='utf-8'))
        self.assertFalse(routes['enabled'])
        self.assertEqual(len(routes['routes']), 18)
        self.assertTrue(all(route['channel_id'] is None for route in routes['routes']))
        for value in integrations.values():
            self.assertFalse(value['enabled'])
            self.assertIsNone(value['adapter'])
            self.assertIsNone(value['credential_source'])

    def test_claude_and_codex_entries_and_memory_references_exist(self):
        bootstrap.generate(self.target, full=True)
        self.assertIn('AGENTS.md', (self.target / 'CLAUDE.md').read_text(encoding='utf-8'))
        self.assertIn('brain/RECALL.md', (self.target / 'AGENTS.md').read_text(encoding='utf-8'))
        recall = (self.target / 'brain' / 'RECALL.md').read_text(encoding='utf-8')
        for relative in ('01 Base/regras.md', '02 Projetos/exemplo.md', '../roles/README.md'):
            self.assertIn(relative, recall)
            self.assertTrue((self.target / 'brain' / relative).is_file())
        role_index = self.target / 'roles' / 'README.md'
        for relative in re.findall(r'\]\(([^)]+)\)', role_index.read_text(encoding='utf-8')):
            self.assertTrue((role_index.parent / relative).is_file())

    def test_generated_files_have_no_host_paths_or_contact_addresses(self):
        bootstrap.generate(self.target, full=True)
        for path in self.target.rglob('*'):
            if path.is_file():
                text = path.read_text(encoding='utf-8')
                self.assertNotIn(str(self.target), text)
                self.assertNotRegex(text, r'(?i)\b[a-z]:[\\/]|/(?:Users|home)/|[\w.+-]+@[\w.-]+\.[a-z]{2,}')

    def test_public_documentation_local_links_exist(self):
        for path in REPO.glob('*.md'):
            for relative in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
                if not relative.startswith(('https://', '#')):
                    self.assertTrue((path.parent / relative).exists(), (path.name, relative))


if __name__ == '__main__':
    unittest.main()
