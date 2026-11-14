"""POST the installed Webmin CGI using synthetic backup metadata and an inert engine.

Run in a disposable root test container with Webmin installed. The setup installs
this checkout's module into that container and supplies local command fixtures.
"""
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]
MODULE = Path('/usr/share/webmin/tklbam')


class RestoreActionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not Path('/usr/share/webmin/WebminCore.pm').is_file():
            raise RuntimeError('Run this integration suite in the disposable Webmin test container')
        shutil.copytree(ROOT / 'tklbam', MODULE, dirs_exist_ok=True)
        cls.temp = tempfile.TemporaryDirectory(prefix='webmin-restore-action-')
        cls.fixture = Path(cls.temp.name)
        cls.engine_calls = cls.fixture / 'engine-calls'
        cls.bin = cls.fixture / 'bin'
        cls.bin.mkdir()
        listing = cls.bin / 'tklbam-list'
        listing.write_text('#!/bin/sh\nprintf "%s\\n" "# local fixture" "3 No created updated 1MB Fixture-three" "4 No created updated 1MB Fixture-four" "17 Yes created updated 2MB Fixture-seventeen"\n')
        listing.chmod(0o755)
        engine = cls.bin / 'tklbam-restore'
        engine.write_text('#!/bin/sh\nprintf "%s\\n" "$*" >> "$RESTORE_ENGINE_CALLS"\necho "Synthetic restore completed"\n')
        engine.chmod(0o755)
        cls.webmin_config = Path('/etc/webmin/config')
        cls.original_config = cls.webmin_config.read_text()
        cls.webmin_config.write_text(re.sub(r'(?m)^path=.*$',
                                            'path=' + str(cls.bin) + os.pathsep + os.environ['PATH'],
                                            cls.original_config))
        Path('/etc/webmin/tklbam/cache.list').unlink(missing_ok=True)

    @classmethod
    def tearDownClass(cls):
        cls.webmin_config.write_text(cls.original_config)
        cls.temp.cleanup()

    def request(self, fields, seed=0, script='restore.cgi', method='POST', expected_error=False):
        body = urlencode(fields).encode()
        env = dict(os.environ, PERL_HASH_SEED=str(seed), PERL_PERTURB_KEYS='2',
                   WEBMIN_CONFIG='/etc/webmin', WEBMIN_VAR='/var/webmin',
                   SERVER_ROOT='/usr/share/webmin', REMOTE_USER='root',
                   THEME_ROOT='/usr/share/webmin/authentic-theme',
                   SCRIPT_NAME='/tklbam/' + script, SCRIPT_FILENAME=str(MODULE / script),
                   HTTP_HOST='localhost', REMOTE_ADDR='127.0.0.1',
                   HTTP_REFERER='http://localhost/tklbam/index.cgi',
                   REQUEST_METHOD=method, CONTENT_TYPE='application/x-www-form-urlencoded',
                   CONTENT_LENGTH=str(len(body)),
                   QUERY_STRING=body.decode() if method == 'GET' else '',
                   PATH=str(self.bin) + os.pathsep + os.environ['PATH'],
                   RESTORE_ENGINE_CALLS=str(self.engine_calls))
        result = subprocess.run(['perl', '-I.', '-I..', str(MODULE / script)], cwd=MODULE,
                                env=env, input=body if method == 'POST' else b'',
                                capture_output=True, timeout=15)
        output = result.stdout.decode(errors='replace')
        stderr = result.stderr.decode()
        if script == 'restore_run.cgi':
            # The unchanged runner warns when its normal no-passphrase redirect
            # leaves this optional value undefined.
            stderr = re.sub(r'\AUse of uninitialized value \$passphrase in concatenation '
                            r'\(\.\) or string at /usr/share/webmin/tklbam/restore_run.cgi '
                            r'line [0-9]+\.\n\Z', '', stderr)
        if expected_error:
            self.assertRegex(stderr, r'Unsupported operation\n$')
        else:
            self.assertEqual('', stderr, output[-1000:])
        return output

    def test_actual_restore_post_ignores_tab_and_csrf_fields_across_hash_orders(self):
        for seed in range(8):
            for flag in ('yes', 'no'):
                for reverse in (False, True):
                    with self.subTest(seed=seed, flag=flag, reverse=reverse):
                        fields = [('list_backups', 'this_server'),
                                  (f'restore:3:{flag}', 'Restore'),
                                  ('csrf_token', 'synthetic'), ('mode', 'restore')]
                        output = self.request(list(reversed(fields)) if reverse else fields, seed)
                        self.assertIn(f'Location: /tklbam/restore_run.cgi?id=3&skpp={flag}', output)

    def test_exact_native_restore_body(self):
        for seed in range(8):
            with self.subTest(seed=seed):
                output = self.request([('list_backups', 'this_server'), ('restore:3:no', 'Restore')], seed)
                self.assertIn('Location: /tklbam/restore_run.cgi?id=3&skpp=no', output)

    def test_direct_action_alone_preserves_backup_and_passphrase_flag(self):
        for backup, flag in ((3, 'no'), (17, 'yes')):
            with self.subTest(backup=backup):
                output = self.request([(f'restore:{backup}:{flag}', 'Restore')])
                self.assertIn(f'Location: /tklbam/restore_run.cgi?id={backup}&skpp={flag}', output)

    def test_advanced_post_renders_existing_options_with_authoritative_metadata(self):
        for seed in range(4):
            for backup, submitted, expected in ((3, 'yes', 'no'), (17, 'no', 'yes')):
                with self.subTest(seed=seed, backup=backup):
                    output = self.request([('list_backups', 'all_backups'),
                                           (f'advanced:{backup}:{submitted}', 'Options'),
                                           ('csrf_token', 'synthetic')], seed)
                    self.assertNotIn('Unsupported operation', output)
                    self.assertRegex(output, r'<form[^>]+action=[\'"]restore_run.cgi[\'"]')
                    self.assertRegex(output, rf'name=[\'"]id[\'"][^>]*value=[\'"]{backup}[\'"]')
                    self.assertRegex(output, rf'name=[\'"]skpp[\'"][^>]*value=[\'"]{expected}[\'"]')

    def test_invalid_and_ambiguous_actions_are_rejected_before_dispatch(self):
        cases = [[], [('list_backups', 'this_server')]]
        for key in ('restore', 'restore:3', 'restore:3:maybe', 'restore:x:no',
                    'restore:-1:no', 'restore:3:no:extra', 'restore:3:no\n',
                    'advanced:3:', 'advanced:3;id:no', 'delete:3:no'):
            cases.append([(key, 'Restore'), ('list_backups', 'this_server')])
        cases += [[('restore:3:no', 'Restore'), ('advanced:3:no', 'Options')],
                  [('restore:3:no', 'Restore'), ('restore:17:yes', 'Restore')],
                  [('restore:3:no', 'Restore'), ('restore:bad:no', 'Restore')]]
        self.engine_calls.unlink(missing_ok=True)
        for fields in cases:
            for seed in range(2):
                with self.subTest(fields=fields, seed=seed):
                    output = self.request(fields, seed, expected_error=True)
                    self.assertIn('Unsupported operation', output)
                    self.assertNotIn('Location: /tklbam/restore_run.cgi', output)
                    self.assertNotRegex(output, r'<form[^>]+action=[\'"]restore_run.cgi[\'"]')
                    self.assertFalse(self.engine_calls.exists())

    def test_repeated_button_fields_select_one_action_across_hash_and_field_orders(self):
        for seed in range(4):
            for operation in ('restore', 'advanced'):
                for flag in ('yes', 'no'):
                    for reverse in (False, True):
                        with self.subTest(seed=seed, operation=operation, flag=flag, reverse=reverse):
                            key = f'{operation}:4:{flag}'
                            label = 'Restore' if operation == 'restore' else 'Advanced Options'
                            fields = [('list_backups', 'this_server'), (key, label), (key, label)]
                            output = self.request(list(reversed(fields)) if reverse else fields, seed)
                            if operation == 'restore':
                                self.assertIn(f'Location: /tklbam/restore_run.cgi?id=4&skpp={flag}', output)
                            else:
                                self.assertRegex(output, r'<form[^>]+action=[\'"]restore_run.cgi[\'"]')
                                self.assertRegex(output, r'name=[\'"]id[\'"][^>]*value=[\'"]4[\'"]')
                                self.assertRegex(output, r'name=[\'"]skpp[\'"][^>]*value=[\'"]no[\'"]')

    def test_direct_redirect_reaches_existing_restore_runner(self):
        self.engine_calls.unlink(missing_ok=True)
        output = self.request([('list_backups', 'this_server'), ('restore:3:no', 'Restore')], 3)
        self.assertIn('Location: /tklbam/restore_run.cgi?id=3&skpp=no', output)
        output = self.request([('id', '3'), ('skpp', 'no')], script='restore_run.cgi', method='GET')
        self.assertIn('Synthetic restore completed', output)
        self.assertEqual('3 --noninteractive\n', self.engine_calls.read_text())


if __name__ == '__main__':
    unittest.main()
