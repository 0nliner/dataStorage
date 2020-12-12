import typing
import unittest
import requests
import pathlib
import warnings

HOST = "127.0.0.1"
PORT = 8080


class TestServer(unittest.TestCase):
    test_file_hash: typing.List[str] = None
    test_data_path = pathlib.Path.cwd() / "store" / "test_data"

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_upload()

    @classmethod
    def test_upload(cls) -> None:
        """
        тест загрузки файлов на сервер
        :return:
        """
        cls.file_hashes = []
        for path in TestServer.test_data_path.iterdir():
            if path.is_dir():
                continue
            with open(str(path), "rb") as file_stream:
                traceback = requests.post(f"http://{HOST}:{PORT}/upload",
                            files={"file": file_stream})

                if traceback.status_code != 200:
                    warnings.warn(f"traceback.status_code is {traceback.status_code}. Should be 200")

                cls.file_hashes.append(traceback.text.split("<br/>")[-1])

    def test_download(self):
        """
        тест скачивания файла с сервера
        :return:
        """
        for file_hash in TestServer.file_hashes:
            traceback = requests.get(f"http://{HOST}:{PORT}/download", {"file": file_hash})
            self.assertEqual(traceback.status_code, 200)

    def test_delete(self):
        """
        тест удаления файла с сервера
        :return:
        """
        for file_hash in TestServer.file_hashes:
            traceback = requests.get(f"http://{HOST}:{PORT}/delete", {"file": file_hash})
            self.assertEqual(traceback.status_code, 200)


class TestServerE2E(TestServer):
    """
    тест всего приложения
    """
    @classmethod
    def setUpClass(cls) -> None:
        return

    def test_E2E(self) -> None:
        """
        тут происходит E2E тест
        :return:
        """
        TestServer.test_upload()
        self.test_download()
        self.test_delete()
