import unittest
import tempfile
from pathlib import Path
from appscope.scanner import CredentialScanner
from appscope.config import ScopeConfig

class TestAppScope(unittest.TestCase):
    def test_pem_detection(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "app.private-key.pem"
            test_file.write_text("-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC3...\n-----END PRIVATE KEY-----")
            
            findings = CredentialScanner.scan_directory(tmpdir)
            self.assertEqual(len(findings), 1)
            self.assertEqual(findings[0]["severity"], "CRITICAL")

    def test_config(self):
        config = ScopeConfig(target_org="test-org")
        self.assertEqual(config.target_org, "test-org")

if __name__ == "__main__":
    main()
