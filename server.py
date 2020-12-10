from aiohttp import web
import pathlib
import hashlib
import os
from multidict import MultiDict

BASE_DIR = pathlib.Path.cwd()
HOST = "127.0.0.1"
PORT = 8082

storage_path = BASE_DIR / "storage"
if not storage_path.exists():
    storage_path.mkdir()


async def upload(request):
    if request.method == "POST":
        data = await request.post()
        if len(data) == 0:
            return web.Response(text=f"no data", content_type="text/html")

        uploading_file = data['filename'].file
        content = uploading_file.read()
        # тут логика, завязанная на сохранении файла и вычислении хеша
        content_hash = hashlib.sha256(content).digest()
        if content_hash:
            folder_name = str(content_hash[0:2])[2:-1]
            folder_name = "".join(char + "\\" for char in folder_name.split("\\")[:2])
            # проверим имеется ли у нас каталог с именем из folder_name внутри storage директории
            if not (storage_path / folder_name).exists():
                (storage_path / folder_name).mkdir()

            full_file_path = storage_path / folder_name / str(content_hash)[2:-1]
            with open(str(full_file_path), "wb+") as new_file:
                new_file.write(content_hash)

            return web.Response(text=f"new file created, hash is:<br/><br/><br/>{str(content_hash)[2:-1]}", content_type="text/html")

        else:
            return web.Response(text=f"your file is empty, system can't create empty file", content_type="text/html")

    elif request.method == "GET":
        html = """
        <form action="{}" method="POST" enctype="multipart/form-data">
          <input type="file" id="myFile" name="filename">
          <input type="submit">
        </form>
        """.format(f"http://{HOST}:{PORT}/upload")
        return web.Response(text=html, content_type="text/html")


async def download(request):
    file_hash = request.query["filename"]
    file_path = storage_path / "".join(char + "\\" for char in file_hash.split("\\")[:2]) / file_hash
    if file_path.exists():
        file_data = file_path.read_bytes()
        return web.Response(body=file_data, headers=MultiDict({"CONTENT-DISPOSITION": file_hash}))
    else:
        return web.Response(text="no such file in storage", content_type="text/html")


async def delete(request):
    file_hash = request.query["filename"]
    file_path = storage_path / "".join(char + "\\" for char in file_hash.split("\\")[:2]) / file_hash
    if file_path.exists():
        file_path.unlink()
        return web.Response(text="file successfully deleted", content_type="text/html")
    else:
        return web.Response(text="no such file", content_type="text/html")


app = web.Application(client_max_size=1024**7)
# для загрузки данных на сервер
app.router.add_post("/upload", upload)
app.router.add_get("/upload", upload)

# для скачивания с сервера
# по тз, как я понял, делать ссылку на статические файлы нельзя, так что вот
app.router.add_get("/download", download)
app.router.add_post("/download", download)

# wD\xe7*\xcc\x9b\n\xfd\xadC\xef\xffV\xac\xdeZ\x9c)Ue#\n\x94y\x99\xd8l$?\xab\xd4\x8c
# для удаления файла с сервера
app.router.add_get("/delete", delete)
app.router.add_post("/delete", delete)


if __name__ == "__main__":
    web.run_app(app, host=HOST, port=PORT)
