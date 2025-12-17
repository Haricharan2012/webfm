from flask import Flask, render_template, request, send_file
import dropbox
import os
from datetime import datetime

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

# ---------- SET YOUR DROPBOX ACCESS TOKEN HERE ----------
DROPBOX_ACCESS_TOKEN = "sl.u.AGJam-tetKtjtZ1fm7aZKrmnlvyZUXp5jKhvBzjfZgYhtKISmP-SHONh_PnwrfS3HkUbkI7HUOeK_Trw4k8Vo4640jzk2kSy2CXnDIEu-P4h7c5ddDcsWK0Gp7Qw7jJ_hrG7YM_o9BKwoQlbvGnz4YSv0rR5ESKfkg2_p-PcgI7ntZnXN116yyz_Rh9_04e6TA5-AslPyD0RJ83lGP3VUsyS3ir7cnjWBC3uc_OCLLuuLeYESYGfg6wW5zXSWX38FINERWuaTmfRCBcZXYQNwUjZ8VI7kYkanOWOPn70GsDrW_WGZknVb8Nt9dAowyFU5w9JIUZalXSzJ4XS8OLcfLE6P5qCr0WuWoqWl9yXP5agEhEc-2K_7zLUJ8w0UBa-LcwGF2iB_Qvy1AN4_N2dD3JBE8Mi0urQ_0ktZex5Ij89NCrK_-3sgRPXPQvQKPHjAvQCV8tS8QnDJCqXBt0f8Pj_tylfI19RAUTc60IgjhD43ErYa5atWnHJRKEcOn7Gu-qc5WpgaIWqz0FZXAB7eRVsSSDPVvWVjdpMMt4kJlr5Fv7o-ARJKfiMnEDrkpc-sHlv2TTbXrnmn5W2raIcxwm698LWuLDQtkyFnZ8yP7e8XNJga1nXxKTyIbPAKTptNarBof0-xOlXO6T3pOf1XMBO_xcJnBoLzvoprOfu0IR_4yqTYctQqE5xykLinz99FPtT7eSI1rEODqRgdFpMqSfQ4WWdvAUjPErnTYzOK5Imbr92ddAPwFZ5XlCBUAwDfKsgqVuUBnpgv20cEN0u8cO8z1TU92GPfgnz_OkQsFasGKvW7m2NZWhC_ynDBdS9giXsqohYPkrqmmimo4pMawqYM_DcOJjXVJWtef6cRnLG5noED3uams0HgZMAeHW3UDXq-BnQlOEFdSBVdRkA_161iPmp4Uis1CBwDSXwpwor3rN8WlX2O2WY7FfEGmF_L3RBhahBQ5QetMBQbAi-_mcGpmRX2Fgnj5lYNo2ymPiJp01G6jy8O1DHFUeY9uMlLx8thtgwLlVV_QgSpRnrXfZQqvEue2gE47TqLTT4KNxUQPWl4vYjx46UbKrc1IadYNOMv0sl2sZFcgCas8g3wD5wW8EWYZkPw3ar6DdDOcbaesqwJIm9AvntL7FtR13hJuqK6PwmdhYp5-yHRNrruREmHuxf2XsRHjOieHpPgLi2GQjm2t88Qf8FW1AdVvFR279nDpgE8ubj1HYNDo77TvXc-iIZPTd64nOrbBbH9Pm8Gkhrfs6e_gSHszQ5vVzvWAu1HZbsw6fufTG10I7KZzqUVBuc96g453rKLVpzqR6wZpt7biWHnbPVdW5h7fCe3D6qh-aMhxszwiqjXDKPe1Zd2b-HJiWjKN01rl-R3msQOPfxWhNgxK6efUhcnMXXh4_qePZQty_0P74PuPZYYzuZpwAQ-vnTsDmerEIGzgCcsw"
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

