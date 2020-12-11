import hashlib
import os
import pathlib
import argparse

from aiohttp import web
from multidict import MultiDict

HOST: str = ""
PORT: int = 0

BASE_DIR = pathlib.Path.cwd()

storage_path = BASE_DIR / "store"
if not storage_path.exists():
    storage_path.mkdir()


async def upload(request):
    if request.method == "POST":
        data = await request.post()
        if len(data) == 0:
            return web.Response(text=f"no data", content_type="text/html", status=404)

        uploading_file = data['file'].file
        content = uploading_file.read()
        # тут логика, завязанная на сохранении файла и вычислении хеша
        content_hash = hashlib.sha256(content).digest()
        if content_hash:
            folder_name = "".join(char + "\\" for char in str(content_hash).split("\\")[:2])[2:][:4]
            # проверим имеется ли у нас каталог с именем из folder_name внутри storage директории
            if not (storage_path / folder_name).exists():
                (storage_path / folder_name).mkdir()

            full_file_path = storage_path / folder_name / str(content_hash)[2:-1]
            with open(str(full_file_path), "wb+") as new_file:
                new_file.write(content_hash)

            return web.Response(text=f"new file created, hash is:<br/><br/><br/>{str(content_hash)[2:-1]}",
                                content_type="text/html")

        else:
            return web.Response(text=f"your file is empty, system can't create empty file", content_type="text/html",
                                status=404)

    elif request.method == "GET":
        html = """
        <style>
                html, body {
                    padding: o;
                    margin: 0;
                }
                
                form {
                    margin: auto;
                    display: flex;
                    flex-direction: column;
                    place-items: center;
                    box-shadow: 0px 0px 7px rgba(0, 0, 0, 0.3);
                    border-radius: 5px;
                    padding: 10px;
                    background-color: white;
                }
                
                #submit {
                    box-shadow: 0px 0px 7px rgba(0, 0, 0, 0.3);
                    border-radius: 100px;
                    height: 10vw;
                    width: 50vw;
                    border: none;
                    margin: 10px;
                    font-family: 30px sans-serif;
                    background-color: black;
                    color: white;
                    max-width: 300px;
                    max-height: 50px;
                }
                
                h1 {
                    text-align: center;
                    text-shadow: 0px 0px 40px forestgreen;
                    color: yellowgreen;
                    font-family: sans-serif;
                }
            </style>
            
        """ \
        + ("""
            <div style="display:grid;
                 place-content:center;
                 height: 100vh;
                 width: 100vw;
                 ">
                <h1>
                    dataStorage
                </h1>
                <form action="{}" method="POST" enctype="multipart/form-data">
                  <input type="file" id="myFile" name="file">
                  <input id="submit" type="submit">
                </form>
            </div>
        """.format(f"http://{HOST}:{PORT}/upload"))
        return web.Response(text=html, content_type="text/html")


async def download(request):
    file_hash = request.query["file"]
    file_path = storage_path / "".join(char + "\\" for char in file_hash.split("\\")[:2])[:4] / file_hash
    if file_path.exists():
        file_data = file_path.read_bytes()
        return web.Response(body=file_data, headers=MultiDict({"CONTENT-DISPOSITION": file_hash}))
    return web.Response(text="no such file in the storage", content_type="text/html", status=404)


async def delete(request):
    file_hash = request.query["file"]
    file_path = storage_path / "".join(char + "\\" for char in file_hash.split("\\")[:2])[:4] / file_hash
    if file_path.exists():
        file_path.unlink()
        return web.Response(text="file successfully deleted", content_type="text/html")
    return web.Response(text="no such file in the storage", content_type="text/html", status=404)


def run_app(host, port):
    globals().update({"HOST": host, "PORT": port})
    app = web.Application(client_max_size=1024 ** 7)
    # для загрузки данных на сервер
    app.router.add_post("/upload", upload)
    app.router.add_get("/upload", upload)

    # для скачивания с сервера
    # по тз, как я понял, делать ссылку на статические файлы нельзя, так что вот
    app.router.add_get("/download", download)

    # для удаления файла с сервера
    app.router.add_get("/delete", delete)
    web.run_app(app, host=HOST, port=PORT)