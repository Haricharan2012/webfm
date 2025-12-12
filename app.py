from flask import Flask, render_template, request, send_file
import dropbox
import os
from datetime import datetime

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

# ---------- SET YOUR DROPBOX ACCESS TOKEN HERE ----------
DROPBOX_ACCESS_TOKEN = "sl.u.AGKSVcBgszsCp9voLcZHm9psMWPHZMOEJF_O1o63vZyaMgb0M5_rcCqln2_Qr6YHJWJRYh-56c_0JfRfSvC_A3fWK6XgJEBfpjB6t8ixtY2YL6Ll_Cn_PnWEaVuUL-9zcmoU8uziISgnjGPP_0uTMig9CHg8RjWtVJUDuvAV1vpwk_8WIq9GWS0KZLKdYbP0GSUJJcoz9s-TC5OosfZNChtOOemzhm1FRBn6EE0gyY53vEjikslMyAthQ9IrIqfuXY9D-8Wc5AOgzLziU4jvjxi6X6E0lKmnYQuQ-UHX2S0DDDRskqmTbpfj87BWhX5622Q4yz_ZgNx-EIZBe52eRk7UNqhvuSHVQduPg_-WA4ZYFIu8_Q35W2rw3RotZ646OyLUrvn3om2leIxSfrOeFaO670V2j_pMGU9R1i4ycIC6FABTkbokMzuuuRjoc3dHYQGk4HVE8b2GckVQHSv8op21pAHot70LIMEOvvCyss8CfB3V4TRCA-dhOmAhEOD2PJR_PPXJccGsBGI8Idg1HZiMOCT90wAT5rnvR4WmpR7-eGK9ofcCsh9M53bWfmzH1YRQaBzaefWBfaT91KPa4GEY0C3n5ODU1M_vi7LRkbLIoaiYxQM7ghWUh9-72sNg-dIjLc3lI0PWkLSL6Wvj2J01fmUkU7RrmGmakR4Z00JIzniqXdE9KwAwDFuef2e8HeoX6ZkTFTwBmbhTLCdXwqivjoLVf4vJ8XkGjcQb8HFV6UToAYthwJBMYSPRn7ZFzuBkfmqT4XM5dn8G3HXkFDAityxf5HH9Z8bUm52U0Hr-7yTnV_rM1xKYLhBU85Vd1sNggOZBoPdjMNxjCZ7-etNo1zspNzPSIXRyiIgVdXsSIE5BuLSU52vrQS23tiyCYoMsjpICu8pNtwZ2BU6TQSpOBDYC1e3FOXT0mmIWkI6rXMk5M4nVM39qAXd3Jc-xSypuXvAuRxNbOSLjaovuJD2oCEN8Q9CwWockdyNuEm9Zr8Lnw5RpnoDA91UW_4B-xAFjfALG2LTub2CKDwdgVpfJSKBNCkdLgKeGu-2jRqU4cFe3D3ckxFP2Snxi2ivYjZfBUabf3o6LbLA-GjrgBKu4DLexMcDrqfl-QKFZl-7vF4w-oZ914sU_olUN9px5psFtoCRrRNZiH9VtD0IR72GAkQl-mQZ0aeL8PAIPeml0YAxedC-3oq3gO37dE_eKcpbg3Nx6rvAKWw1Y2p0k4MXzHJuazvLxkC9_cDUTnI92aueloe5fBbbW7gP3dpkWUTWA4IIMLQRBM0hTIQ94ThYFQQN75ODcWYIkkWgqa-bq6TKWqNkfshBoDnEp8sBw7xFdgyKB1tKkOZ1kT-Cqptv4FV4yf3AkAATo2EbknZqzT-lO65Bv0tj2sFBEmtlhmJ7idaUxVF8OFC3Zw4BctUKW34t71qzPRXMiV9N4D-kEAA"
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

