#!/usr/bin/env python3
"""Adversarial fixtures for versioned preview identity, independent of the live tree."""
import hashlib, inspect, json, stat, sys, tempfile, unittest, zipfile
from pathlib import Path
from validate_collection import validate_previews, validate_inventory_sources

H = lambda data: hashlib.sha256(data).hexdigest()

class PreviewIdentityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root/'website/previews').mkdir(parents=True)
        (self.root/'website/records/test').mkdir(parents=True)
        self.original = {'index.html': H(b'original')}
        self.current = {'index.html': H(b'new'), 'ar/index.html': H(b'ar')}
        self.entries = []
        for name, contents, role in [('old.zip', {'index.html': b'original'}, 'historical-frozen-import'), ('new.zip', {'index.html': b'new', 'ar/index.html': b'ar'}, 'current')]:
            self.write_zip(name, contents)
            self.entries.append({'path':'website/previews/'+name, 'sha256': H((self.root/'website/previews'/name).read_bytes()), 'role':role, 'files':{n:H(b) for n,b in contents.items()}})
        self.frozen_path = self.entries[0]['path']
        self.frozen_sha256 = self.entries[0]['sha256']
        self.register={'schema_version':1,'active_site_record':'website/records/test/current-site.json','previews':self.entries}
        self.record={'schema_version':1,'current_preview':'website/previews/new.zip','files':self.current}
    def write_zip(self,name,contents):
        with zipfile.ZipFile(self.root/'website/previews'/name,'w') as z:
            for n,b in contents.items(): z.writestr(n,b)
    def failures(self, register_text=None, record_text=None):
        register_text = json.dumps(self.register) if register_text is None else register_text
        record_text = json.dumps(self.record) if record_text is None else record_text
        register_file = self.root/'website/previews/preview-register.json'
        record_file = self.root/'website/records/test/current-site.json'
        register_file.write_bytes(register_text) if isinstance(register_text, bytes) else register_file.write_text(register_text)
        record_file.write_bytes(record_text) if isinstance(record_text, bytes) else record_file.write_text(record_text)
        errors=[]
        parameters = inspect.signature(validate_previews).parameters
        anchors = {}
        if 'frozen_path' in parameters:
            anchors['frozen_path'] = self.frozen_path
        if 'frozen_sha256' in parameters:
            anchors['frozen_sha256'] = self.frozen_sha256
        validate_previews(self.root,self.current,self.original,lambda ok,msg: errors.append(msg) if not ok else None,**anchors)
        return errors
    def test_valid_distinct_historical_and_current(self): self.assertEqual(self.failures(),[])
    def test_historical_tamper(self):
        self.write_zip('old.zip',{'index.html':b'corrupt'})
        self.assertTrue(any('Preview digest mismatch' in x for x in self.failures()))
    def test_original_inventory_tamper(self):
        self.original['index.html']=H(b'fake original')
        self.assertTrue(any('Frozen preview differs' in x for x in self.failures()))
    def test_current_missing_extra_changed(self):
        for contents in ({'index.html':b'new'},{'index.html':b'new','ar/index.html':b'ar','extra':b'x'},{'index.html':b'changed','ar/index.html':b'ar'}):
            with self.subTest(contents=contents):
                self.write_zip('new.zip',contents)
                self.assertTrue(any('Current preview differs' in x for x in self.failures()))
    def test_preview_registry_paths(self):
        self.entries[0]['path']='website/previews/../../outside.zip'
        self.assertTrue(any('Invalid registered preview path' in x for x in self.failures()))
    def test_record_path_escape(self):
        self.register['active_site_record']='../outside.json'
        self.assertTrue(any('Invalid active site record path' in x for x in self.failures()))
    def test_invalid_active_record_does_not_skip_package_integrity(self):
        frozen = self.root/'website/previews/old.zip'
        info = zipfile.ZipInfo('index.html', date_time=(2001, 2, 3, 4, 5, 6))
        info.compress_type = zipfile.ZIP_DEFLATED
        with zipfile.ZipFile(frozen, 'w') as archive:
            archive.comment = b'recompressed while active record is invalid'
            archive.writestr(info, b'original')
        self.entries[0]['files'] = {'index.html': H(b'wrong registered member')}
        self.original['index.html'] = H(b'wrong frozen inventory')
        for record_name, record_error in (
                ('../outside.json', 'Invalid active site record path'),
                ('website/records/test/missing.json', 'Missing active site record')):
            with self.subTest(record_name=record_name):
                self.register['active_site_record'] = record_name
                errors = self.failures()
                for expected in (record_error,
                                 'Frozen preview container identity mismatch',
                                 'Preview digest mismatch',
                                 'Preview registered contents mismatch',
                                 'Frozen preview differs from original ZIP inventory'):
                    self.assertTrue(any(expected in error for error in errors),
                                    (expected, errors))
    def test_duplicate_or_missing_preview(self):
        self.entries.append(dict(self.entries[0]))
        self.assertTrue(any('Duplicate registered preview paths' in x for x in self.failures()))
        self.entries.pop();self.entries.pop()
        self.assertTrue(any('membership mismatch' in x for x in self.failures()))
    def test_current_pointer_or_record_tamper(self):
        self.record['current_preview']='website/previews/old.zip';self.record['files']={}
        errors=self.failures()
        self.assertTrue(any('pointer mismatch' in x for x in errors));self.assertTrue(any('Active site record differs' in x for x in errors))
    def test_unsafe_member(self):
        self.entries[1]['files']['../outside']=H(b'x')
        self.assertTrue(any('Invalid preview member paths' in x for x in self.failures()))
    def test_recompressed_frozen_container_is_rejected(self):
        frozen = self.root/'website/previews/old.zip'
        original_container = frozen.read_bytes()
        info = zipfile.ZipInfo('index.html', date_time=(2001, 2, 3, 4, 5, 6))
        info.compress_type = zipfile.ZIP_DEFLATED
        with zipfile.ZipFile(frozen, 'w') as archive:
            archive.comment = b'recompressed historical fixture'
            archive.writestr(info, b'original')
        self.assertNotEqual(frozen.read_bytes(), original_container)
        with zipfile.ZipFile(frozen) as archive:
            self.assertEqual(archive.read('index.html'), b'original')
        self.entries[0]['sha256'] = H(frozen.read_bytes())
        self.entries[0]['files'] = {'index.html': H(b'original')}
        errors = self.failures()
        self.assertTrue(any('Frozen preview container identity mismatch' in error
                            for error in errors), errors)
    def test_frozen_role_cannot_be_reassigned(self):
        self.entries[0]['role'] = 'historical-candidate'
        self.write_zip('replacement.zip', {'index.html': b'original'})
        replacement = self.root/'website/previews/replacement.zip'
        self.entries.append({
            'path': 'website/previews/replacement.zip',
            'sha256': H(replacement.read_bytes()),
            'role': 'historical-frozen-import',
            'files': {'index.html': H(b'original')},
        })
        errors = self.failures()
        self.assertTrue(any('Frozen preview path/role identity mismatch' in error
                            for error in errors), errors)
    def test_zip_symlink_member_is_rejected(self):
        current = self.root/'website/previews/new.zip'
        link = zipfile.ZipInfo('index.html')
        link.create_system = 3
        link.external_attr = (stat.S_IFLNK | 0o777) << 16
        with zipfile.ZipFile(current, 'w') as archive:
            archive.writestr(link, b'new')
            archive.writestr('ar/index.html', b'ar')
        self.entries[1]['sha256'] = H(current.read_bytes())
        self.entries[1]['files'] = dict(self.current)
        errors = self.failures()
        self.assertTrue(any('Non-regular ZIP member' in error
                            for error in errors), errors)
    def test_special_type_metadata_is_rejected_across_creators(self):
        current = self.root/'website/previews/new.zip'
        for creator in (0, 3, 19):
            with self.subTest(creator=creator):
                link = zipfile.ZipInfo('index.html')
                link.create_system = creator
                link.external_attr = (stat.S_IFLNK | 0o777) << 16
                with zipfile.ZipFile(current, 'w') as archive:
                    archive.writestr(link, b'new')
                    archive.writestr('ar/index.html', b'ar')
                self.entries[1]['sha256'] = H(current.read_bytes())
                self.entries[1]['files'] = dict(self.current)
                errors = self.failures()
                self.assertTrue(any('Non-regular ZIP member' in error
                                    for error in errors), errors)
    def test_zero_type_metadata_is_accepted_across_creators(self):
        current = self.root/'website/previews/new.zip'
        for creator in (0, 3, 19):
            with self.subTest(creator=creator):
                ordinary = zipfile.ZipInfo('index.html')
                ordinary.create_system = creator
                ordinary.external_attr = 0
                with zipfile.ZipFile(current, 'w') as archive:
                    archive.writestr(ordinary, b'new')
                    archive.writestr('ar/index.html', b'ar')
                self.entries[1]['sha256'] = H(current.read_bytes())
                self.entries[1]['files'] = dict(self.current)
                self.assertEqual(self.failures(), [])
    def test_malformed_register_shapes_are_reported(self):
        frozen = self.root/'website/previews/old.zip'
        frozen.write_bytes(frozen.read_bytes() + b'changed container')
        self.register = []
        errors = self.failures()
        self.assertTrue(any('Invalid preview register' in error for error in errors), errors)
        self.assertTrue(any('Frozen preview container identity mismatch' in error
                            for error in errors), errors)

        self.register = {'schema_version': 1,
                         'active_site_record': 'website/records/test/current-site.json',
                         'previews': self.entries}
        self.entries[1] = 'not an object'
        errors = self.failures()
        self.assertTrue(any('Invalid preview entry' in error for error in errors), errors)
        self.assertTrue(any('Frozen preview container identity mismatch' in error
                            for error in errors), errors)
    def test_invalid_json_is_reported(self):
        errors = self.failures(register_text='{')
        self.assertTrue(any('Invalid preview register JSON' in error for error in errors), errors)
        self.entries[1]['sha256'] = '0' * 64
        errors = self.failures(record_text='{')
        self.assertTrue(any('Invalid active site record JSON' in error for error in errors), errors)
        self.assertTrue(any('Preview digest mismatch' in error for error in errors), errors)
    def test_non_object_active_record_is_reported(self):
        self.entries[1]['sha256'] = '0' * 64
        errors = self.failures(record_text='[]')
        self.assertTrue(any('Invalid active site record' in error for error in errors), errors)
        self.assertTrue(any('Preview digest mismatch' in error for error in errors), errors)
    def test_null_active_record_is_rejected_without_skipping_package_integrity(self):
        for tampered_digest in (False, True):
            with self.subTest(tampered_digest=tampered_digest):
                if tampered_digest:
                    self.entries[1]['sha256'] = '0' * 64
                errors = self.failures(record_text='null')
                self.assertIn('Invalid active site record', errors)
                if tampered_digest:
                    self.assertTrue(any('Preview digest mismatch' in error
                                        for error in errors), errors)
    def test_invalid_role_type_is_reported(self):
        self.entries[1]['role'] = []
        errors = self.failures()
        self.assertTrue(any('Invalid preview role' in error for error in errors), errors)
    def test_invalid_utf8_is_reported(self):
        errors = self.failures(register_text=b'\xff')
        self.assertTrue(any('Invalid preview register JSON' in error for error in errors), errors)
        self.entries[1]['sha256'] = '0' * 64
        errors = self.failures(record_text=b'\xff')
        self.assertTrue(any('Invalid active site record JSON' in error for error in errors), errors)
        self.assertTrue(any('Preview digest mismatch' in error for error in errors), errors)
    def test_corrupt_zip_is_reported_without_suppressing_other_checks(self):
        current = self.root/'website/previews/new.zip'
        current.write_bytes(b'not a ZIP archive')
        self.entries[1]['sha256'] = H(current.read_bytes())
        self.original['index.html'] = H(b'wrong frozen inventory')
        errors = self.failures()
        self.assertTrue(any('Invalid preview ZIP' in error for error in errors), errors)
        self.assertTrue(any('Frozen preview differs from original ZIP inventory' in error
                            for error in errors), errors)
    def test_preserved_source_copy_tamper(self):
        p=self.root/'archive/original.py';p.parent.mkdir();p.write_bytes(b'exact original')
        rows=[{'destination':'archive/original.py','source_path':'qa/original.py','sha256':H(b'exact original'),'disposition':'archived-byte-identical'}]
        def errors():
            failures=[]
            validate_inventory_sources(self.root, rows, lambda ok,msg: failures.append(msg) if not ok else None, lambda q:H(q.read_bytes()))
            return failures
        self.assertEqual(errors(),[])
        p.write_bytes(b'changed fixture')
        self.assertEqual(errors(),['Changed source bytes: archive/original.py'])
    def test_help_has_no_side_effect(self):
        import subprocess
        script=Path(__file__).with_name('package_website.py')
        root=script.parents[1];before={p:p.stat().st_mtime_ns for p in (root/'website/previews').glob('*')}
        result=subprocess.run([sys.executable,str(script),'--help'],capture_output=True,text=True)
        self.assertEqual(result.returncode,0);self.assertIn('usage:',result.stdout)
        self.assertEqual(before,{p:p.stat().st_mtime_ns for p in (root/'website/previews').glob('*')})
if __name__=='__main__': unittest.main()
