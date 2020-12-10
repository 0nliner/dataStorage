import unittest
import requests
from server import HOST, PORT


class TestServer(unittest.TestCase):
    def setUp(self) -> None:
        self.test_file_hash = r"0\x19\x0c\x85\xd5\xf9\x03qm\x94\xb2N\x8cH\xdbO3\x10\xbc\xb6\x84\xfdG\x14\x19\xf9\xa5\x07\xafl\xf6\x9b"

    def test_download(self):
        traceback = requests.get(f"http://{HOST}:{PORT}/download", {"filename": self.test_file_hash})
        self.assertEqual(traceback.status_code, 200, "200")

    def test_delete(self):
        traceback = requests.get(f"http://{HOST}:{PORT}/delete", {"filename": self.test_file_hash})
        self.assertEqual(traceback.status_code, 200, "200")


if __name__ == "__main__":
    unittest.main()