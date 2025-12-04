from flask import Flask, render_template, request, send_file
import dropbox
import os
from datetime import datetime

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

# ---------- SET YOUR DROPBOX ACCESS TOKEN HERE ----------
DROPBOX_ACCESS_TOKEN = "sl.u.AGI2OLzeVYf84onXjlf2UZrqTmbcxAXJfcAV1TZUaIor92fPoF8hj7hZodeLuwZ9kEe40IPOikSpvie9oWFzJNJ8W4eQ0q1r89cVziltKUrAAuupon8Ign7-57JNMazVyveuH8zfe7urBGzGHV8w5J1DJfPvk1INFpkcqgNvnzpvBtlrx2qbut8415pmQvr8KKBFKKc1gwMpi5ZBCUTYfpKNz-RTla-_N4gWs0acjEeX_B85k4nk8pToE6JMIEKqi_wAzOXd8a6vFO3lSYgB_GrKUSo60gS9Rhn8axZ_YMmLEV1-qJhDzraHHMTR4HrjM0nlYSZ_cR8dIKRNhegNA0vEBPomaMOqq-vPHVFnOG3Zt1KaFWdsKxcNh3OMfJPj7l2pXQzn2Ipw9yrSjU7c_H7kpA5FCSaqCoZCl9ZcOZfkyagXDNWbiwHHIC3pDkodo8Z1prT67AXbfCGTWJvSxpDLiFPXRbVVLooA_9sB1kgKNPkh45PDaTNXtnozf28OlLuoTLyLtPu0TWIOAT2-gOgSEkd1RpLkymNS94Mzw8FX-JMjt9aXy79qw2pad8hI0WmBDVAXhE0cMYZQqw-xBNlGaUY0ufsV3pfvByqAW3pIWB-cwiju8-BfepF7GmILow6ya7nHoCdKel_x0Epqyk36V3TgXMDr94iPQa2VJqXU-tZzvFiVvi1wZjLWeZeCcEvsGNh6p_4KmJyVB1sjWeESFLqG11ee7JqkqqxLHEDpCDHqmzadOngUbg9HikTV9UGrI3Py7nHgbtNnU4z9cZwuT87Mk5yB7gaR1Zh9-33dobsn_Z-ZKp0T0Lw9YpBDl4S6xuoubbBGbTp9a38AZ-_bvTULFZ56E03aFTrj42VUK101WT2hfFSsQMzNFmizwARxuRdgUldkSQUHzVZqIoH0rhmYZaPNjPeoQL1STqRSpzxF9cNSU36QyWyTS0kSE2sQsEUjifFSAXvrOn42mtxH2WlBhOE6UvqLzPtgZdtK_KM4tr2eTYWhjDHY-68SKPcwF6euOTpo2Mp-Xls4v-jYnekzBtgrD-1K26ONEcaABM4Y31y2tqzFHYOblryT2yVcqd7aLr4GwCBDfH5IoXFWW_CghdzLpl7OOlEmmpfaD-vNKdVPwoPF0e6BOzoiejakdmueW_SXAm6pqo4RzYNS1xoA3XS3swvGAu0A35I_X2oxqMzyxZ2My9IzU39L0uts6GLrZlADGCkU-37uEPLnl-aba9B5KfKYnOPoODtyuFKqfGyl8rdHCGZ_q2JV_GURYU5-QNxzn4c5RN4pd-YI7LdJqeQ51VB34n5rwXhtkVSMfrybyzqHW37L0UDa3Nwv_eYJj4nJOTYTiLJN232H3FP9Y7nQh6vag8sWQqZkG55c9dYoARiYqeyU253nm1-b2No0E02KznGPUnvfTSSpEp-bDxDY82xDsHggc3-gIg"
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

