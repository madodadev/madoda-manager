from flask import Flask, request, Response
from pathlib import Path
from werkzeug.utils import secure_filename
from datetime import date
import json

from server.auth import auth
from mmanager import MMangaer
app = Flask(__name__)
manager = MMangaer()

main_upload_path = Path(__file__).parent / "musics" / "uploads"
if not main_upload_path.is_dir():
    main_upload_path.mkdir()

@app.route("/")
def hello():
    return "Hello Word"

@app.route("/down_up_gdrive", methods=["POST", "PUT"])
def down_up_gdrive():
    req_content = dict(request.get_json())
    if not req_content: return Response("error: data not found", 400)
    if not auth(req_content.get("api_key")):return Response("error: auth error", 400)

    m_contents = req_content.get("m_contents", 0)
    m_contents, dump_file = manager.main(m_contents)
    posts = []
    posts_failed = []
    for m_content in m_contents:
        if(m_content.get("gdrive_ids")):
            posts.append({"post_id": m_content["post_id"], "gdrive_ids":m_content["gdrive_ids"], "filename":m_content["filename"]})
        else:
            posts_failed.append(m_content)
    resp = {"posts": posts, "posts_failed": posts_failed, "mms_dump_file": dump_file}
    return json.dumps(resp)


@app.route("/upload_file", methods=["POST", "PUT"])
def upload_file():
    if not auth(request.form.get("api_key")):
        return Response("error: auth error", 400)

    def is_allowed_file(filename):
        ALLOWED_EXTENSIONS = ('.mp3', '.mp4', '.txt', '.jpg', '.jpeg', '.zip', ".rar")
        if str(Path(filename).suffix) in ALLOWED_EXTENSIONS:
            return True

    files = request.files
    if not files: return  Response("error: files not found", 400)
    
    music_save_folder = main_upload_path / str(date.today())
    if not music_save_folder.is_dir():
        music_save_folder.mkdir()
    res = []
    for f in files:
        req_filename_field = request.form.get("filename")
        req_file_name = Path(request.files[f].filename)
        if req_filename_field:
            if not Path(req_filename_field).suffix ==  req_file_name.suffix:
                name = req_filename_field+Path(request.files[f].filename).suffix
                filename = music_save_folder / secure_filename( name )
            else:
                filename = music_save_folder / secure_filename( req_filename_field )
        else:
            filename = music_save_folder / secure_filename( Path(request.files[f].filename).name )
        print(filename)
        if is_allowed_file(filename):
            files[f].save(filename)
            res.append({"ID": f, "filename":str(filename.absolute())})
        break
    
    return json.dumps(res)
    
@app.route("/verify_file", methods=["GET"])
def verify_file():
    def is_in_upload_dir(filename):
        in_upload_dir = False
        for key, value in enumerate( main_upload_path.absolute().parts ):
            in_upload_dir = False
            if value == filename.parts[key]:
                in_upload_dir = True
        return in_upload_dir

    if request.args.get("filename"):
        filename = Path(request.args.get("filename"))
        if filename.is_file() and is_in_upload_dir(filename):
            return "1"
    return ""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6060, debug=True)