from flask import Flask, render_template, request, send_file
import dropbox
import os
from datetime import datetime

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

# ---------- SET YOUR DROPBOX ACCESS TOKEN HERE ----------
DROPBOX_ACCESS_TOKEN = "sl.u.AGKdd7hrGYkBho3v9uMiLRDcL5xYf2e1rYRuI1cHdLo5C9qyixKV-G2Gsz6gsZ_ZijaMF4QpZ9uTjuadJczu7uW-N0NIyUYgW3ydKtyLAXWQR53l2DXq0do9SK28NXwQfK7-_ePYcm0NodBssrcNuEz_MZt3zykSENm-d4R1e_9-bMhBkoohKVvODoug7RRcjL8jmPoNxy2bfyRp_XahgtlNzeH8Z84XALpNxE7Kc1AjoV6eeIFJqbBW80Eq0L2-HyEggSMZKrXSL_42uEvtOmHNrk85kwgggYVuKUQ9KdpBtD1CcoeMybaVdPIvRWBz0-RdXRYvbXAugOG-C5TrrrO9JFvzCtAZUuaVAIX3VSxvcRj5xH8tadu6aXUNxsyjCLn7OchoAm7b6fhsMpUuR8qi0O79WFXix2R4BR3oPby1g43T6ofOMQZ7TE05haGMvYLeF2_YcONzX8EgSDpkDIQ19Hby1o2ZLtVZVfjmfuN0tCcuV9LGt1JGJ-OnCHWABoE-kgjs1GwOzIUohl3rbYeXIF7HuDdf14fYEYpXkKRwVBQMI9g-nTV5jNkvMaTCQxKcbhZgWTYqi3SuuenrGx7Ua2_Q6clTHKQrKcPPbABgkCY88TnhkLbg3DdTX2znOpxM_2eQJqfr46BwpbU_1eFz98qwtejO1luvrddx2XE3v1WgrOBZKSJty-GR00N0CrMCmS0dXGVqpJRmI18HuQRgMbE-mzlH8EpqVxlGEqMDrUxv9-qFEBbuBmYUzd3yL0ZP-exMfGQdWpeh13vt3ZE4zMRABe0WE23h9FRgU_P77Rca_8rmZ6VHn7NuBTWt4KKHYPU7l7P61_a1nJGatRwgDLMVly4KRlMM8Z0QAHI4PMoIyQbQpl084AshojIshd_hGYfD_-N9AtEAyY6rdGlT9WjB1VyDaO5IKWVKiRyRau4kAC60Z6UuYbNeiECBwEDWdwuBHbTPdvSPBkfVhbePZ1Z_iI3mjNE5jFWoKhD3Wb9T4rZvv6xfkwFqqwyCHUni_owQQ6gmP_aVdpe5eEKdkTYd5ZGF_h3WFtgQmdvVkPA8w0AfED0krPeWMyVFWk0BG3x6Zn-0gNjWDJdrBlzqfhrZJkPkSvTeI6ugc1UBLKJlhw9DxLqDA9icMkIihbvbGkHTVfbOfqB_0c2iwFdIzrFu0Yll6WtxW9wlEyRrbun-NCDuh4Zycgsirzp335-LiqPhTwIwPcvzZn57B80m-Xfy_76HNm-Cx8MlzeoGTCJB36Ln_IP4mqpIbir1q2wm1rJhnOzObMTKLP-FpSzf4q_m6CMevTTmAneUbuP3JF-MJXShLBPiJ4TrUkj90uSyns9YjJ4fhYeWQSz28eFodQFHQ5B_U4NMYjiEWHTrIP-R0C-483QT8Zvb6jhSL09eUY86Igp4kNn0mwTBhlNd6JsV_-4uXgZologaQX_y6Q"
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

