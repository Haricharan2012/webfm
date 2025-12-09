from flask import Flask, render_template, request, send_file
import dropbox
import os
from datetime import datetime

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

# ---------- SET YOUR DROPBOX ACCESS TOKEN HERE ----------
DROPBOX_ACCESS_TOKEN = "sl.u.AGJnRVdYSWqo0gg7CXe8nM-_WEHvMQSXwBZa1uCPKKJeh4zGhmdMwVL42e9tVcoYg18zsDJf8QPAhJunfMJXaw9Z9Xkk38SJeYWUEJo-PhD31W757ZS8d940_mg3f2g_iScm1AT8v0hAnrZX4QKRjktezBaCtqZW6AreuPbfueBd5gp0atqrX1QIEJHUbtpJBbRkFvxnpQ-dlHHT-Nxhv_PB0rOJv2vib2M5Vgfi14H7BrFgILSJ_Hi-bOR4AT3fW1VjWFIXAWIAzXVuGutQcGBcc0IkhPudyIQx99NU5nQhRk9621v4uw9YJatOowbluqAEEkdjOMSw7J-cIBjnTnmbYfx8uTawEbrrHYqPt16HlhEB24lL7Bf1AX_mG2G3ENWcbaUeVFpL_kl6WF5XQZFzOyru_k6qFcC7Oo60jTjps2dc7YcCKxFMBlDQY2eD0ilSYDnd-kCH24W98SyaHgRRGPZXfou6-KET_2o1ZDMS2R1yhXlWTYM6PWfPdxrIt0w_RAeBPElZ-fmQdyWf8DZVf4wonP2le0jGyxnz7twOGVq2UrtOnvyeWqmh2Ok0-XeHtyWRMNZ-e8XsFDJha522qXo9oIsNPLSWpSP_hhzWhzyclIVfFMxkHUVlvbWAbTvdgsyvJxQKMFk8-fZ7oAJrfyCEJHchQg33CdRPrC0pozFi_fAdXHTz7STs9lNQlDpMWw9C2smWdG3o7z66iKneHuzlYzY4Hl2UKKDCwiVmH6_0jVE2E3ZcPjvPbnpRsngS7sqRYfd1etsFjRU8cm3F2MLlSzhQVNoPc95bIz1NSNxVjEUV56xR2OSUuj9vEOAAXpcaJubsgf2aUW7FKHqtSdf4NwCODj_2qhc5yYRsHcrfQc9a4zaIBNHBXgOUjgTj5_-fihf2iH-Rt-daopn7J1RlE6noQb0-x650auGwTzoXFKyJQuPh3TexT5FX2q-u5zdw31gIyr2Ib8lcEACl3iSIt1WpajTZttiLBzZxuUS7hNtcEuYXZvM2sadSfVg8SikLw_2yAp-hY5KdR1izKoQq35WxvgAPfOezZi4rOWZpG0TUcI2-DEfOacioNjQ5Szx6A13cxIYCf03ZcnbbkKh-WNEBjw0Ce-wI-WdIVyg-qEfPy17EBUH3nO-L838QZ-gEBtLeSSiujORtNF646NCRgfhFk3-jJF255SWOumy_9hhny8I760BMIPJSw9MEbxHDrE-1Je174rlvaA_Rv8JC_QDx9kCAY-J9n65nVCL8ef-TkfTeEx76xEmiY0QLC6OWGZOG_mwY7bCMl5UBVxdY8qAOwNpAWbbv44BR3p9CtXT3FUx-q6Kz5U5OzaTjb0D6181I3JrlzlMqS5pXosBIoOnvdNTmqZl9LJibMkqelTmf4c3Ica2MAdJuNh9ugifaV8hnAU-lJKovl5v8fQSZ7XdB8ogJRx6IK-nlbg"
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)


@app.route("/fileup")
def index():
    # List files from Dropbox
    files = []
    res = dbx.files_list_folder("")

    for entry in res.entries:
        if isinstance(entry, dropbox.files.FileMetadata):
            files.append({
                "name": entry.name,
                "size": round(entry.size / 1024, 2),
                "date": entry.client_modified.strftime("%Y-%m-%d %H:%M"),
                "path": entry.path_lower.replace("/", "")
            })

    return render_template("fileupload.html", files=files)


@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]

    if file:
        filename = file.filename
        local_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        # save file temporarily
        file.save(local_path)

        # upload to Dropbox
        with open(local_path, "rb") as f:
            dbx.files_upload(f.read(), "/" + filename, mode=dropbox.files.WriteMode.overwrite)

        os.remove(local_path)  # remove local file after upload

    return "File uploaded successfully! <a href='/fileup'>Back</a>"


@app.route("/download/<path>")
def download_file(path):
    dropbox_path = "/" + path

    # temporary download
    local_path = os.path.join(app.config["UPLOAD_FOLDER"], path)

    md, res = dbx.files_download(dropbox_path)

    with open(local_path, "wb") as f:
        f.write(res.content)

    return send_file(local_path, as_attachment=True)


if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    app.run(debug=True)

