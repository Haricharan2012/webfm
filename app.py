from flask import Flask, render_template, request, send_file
import dropbox
import os
from datetime import datetime

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

# ---------- SET YOUR DROPBOX ACCESS TOKEN HERE ----------
DROPBOX_ACCESS_TOKEN = "sl.u.AGJNLi3rVgzT7Fc1cPFdmyJuoBBvRXTcnuZRYKyisZoyslzOP7QNNdBtJHfhns_zfM17cbBHI3oSTN26t9-ZXMSeaXdnpXzQ5_hxu0e3QUynlx6Qls6s3xLCqv-phB2j8SBtG3MDZ2nPj0VT39CeZ3CKUwZZn7QaNr-HERAlYj31rL-7p78SwF0hL-MNE3_Zq-2jhR6B_qO5C8H0u8dE3Mzo2BZkjI-ZwZlxzLbORzYuShf9U-QzPclSK0rVAtt5qzm8XSYtojJVMlRl1fnzAx_ulhcg1DNp-V9uAk2HJhKfas-Ymhme6r9r7B_4GAmE8e96Cikq3unQpZmeakjaF7IkBhNK0Feg_2d2oVY_Axajbk8oXTPqblakrePrDCGxob77bTArXc2ECsNB6gPsW-ybnL_Gz71aGzACOjTbJ5HPbjBfyezmKak0iB6SbCD-FzHvXweGkRua4CNBHPy3iEBuzbzPB5XCMClAjH7sWnedKIc1GYGpusRpzh5N_RQPQmkahuSg7hNfuMn7w2zbx58nLMDxSR_oRxUO4jiI5iJ8msJX2VLqTjdivnQjQ09qnT4yc2fer-re020qWZQA9q4K7SVXOSMRaqd6yR3YABvSFdikiS_yMJZ8dcSLPlAtEa4WT3a8dc2tt3o9Dlhk07S9YZzyKQ7zA-wwzd1u9dUXfTaQ0XJVQZPwvjU-Zl_Is5TRicTKz_SujfrreA9PB8n_9l7K61plhRZQtnkdqdYJUIzIDdb85CXNVR8HjwC_K2Qi0ZUvgwiT03tcTVxNR3UZmU0_YvWga0wJYzkRwSIUbU6vFXPNkL7rTE_D9e0AJKRYlHzwDDhJ2dyveLYYvQAtFL_T-vPX7zp1pO9a8p1hPVYhTDMdYhIe7IWTLCw213n5Acnss2catWq5jTfQq4u2fw06zNRORkGVddLpCp25ftjshQ1r-qhh_Bxf_g5fonqRMy4v9ky-iflpeDNaWwRi0I239MLIj1Nz6UMF1kyurJAbkWAASH2Rxl6gG7syeeaw3a0SDhNkb8j1nwLrSQp1q3xnhrclsBrAWo2gYunwf-rxuwZtm7Uz01M2wVo0H19EdHT1lg9osiwJmJWMwa0vHM6JQg1m0GB5nrPjWevTo4a5pbd2DBBDkmtaH6b-aqRyEb68vJPzRcO-AD6Uh1YWlqDo-xue3oMH9kOdSUPHjKsAr0-UP-95myTlBkzNaCGbwleYr570UtGZJ5yE7vkkR-DKA9RNAtQnMgQONrbhq5kyTGhT1tT7hS5BzTzaBdb1kHLbmSAYaytmOLbvJVkZQrBrCaABAvbu7dHzzm2owVN_VbDDa1GL8cWo8JrDIuCKz1RrSVzhO5_r9m2P9abYkodZBbx1JVIc6h2hkXnM2AA9RF3Qlj-DlMVCKF1Ds3gtrtrXcL-fy18qfNQ7ENtnHEiKvAU1xaAk7M7GbjiYIA"
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

