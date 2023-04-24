from website import create_app
from flask_restful import Api, Resource
from flask import Flask, request, render_template, send_from_directory
from website.frontend import bp
import requests
from flask_restful import abort
import json
#import datetime
#from google.cloud import storage


app = create_app()
BASE = 'https://module-registry-website-4a33ebcq3a-uc.a.run.app/' 
@app.route("/")
def defaultPage():
    return render_template('mainPage.html')

@app.route("/upload")
def uploadPage():
    return render_template('upload.html')
    #
    # storage_client = storage.Client()
    # policy = storage_client.generate_signed_post_policy_v4(
    #     "bucket-proto1",
    #     "blob_name2",
    #     expiration=datetime.timedelta(minutes=10),
    #     fields={
    #         'x-goog-meta-test': 'data'
    #     }
    # )
    #
    # # Create an HTML form with the provided policy
    # header = "<form action='{}' method='POST' enctype='multipart/form-data'>\n"
    # form = header.format(policy["url"])
    #
    # # Include all fields returned in the HTML form as they're required
    # for key, value in policy["fields"].items():
    #     form += f"  <input name='{key}' value='{value}' type='hidden'/>\n"
    #
    # form += "  <input type='file' name='file'/><br />\n"
    # form += "  <input type='submit' value='Upload File' /><br />\n"
    # form += "</form>"
    #
    # print(form)
    #
    # return form

@app.route("/packagesListInput")
def packagesListInput():
    return send_from_directory('templates','packages.html')

# Post request that retrieves array from /pacakgesListInput, called under action in html file
@app.route("/packagesList",methods = ["POST"])
def packagesListDisplay():
    data = request.form.get("Query")
    headers = {'Content-Type': 'application/json'}
    if data == "[*]":
        response = requests.post(BASE + 'packages',json = {'PackageQuery' : ["*"]},headers = headers)
    else:
        response = requests.post(BASE + 'packages',json = {'PackageQuery' : json.loads(data)},headers = headers)
    # print(response)
    return response.json(), response.status_code
    # return 'test'

@app.route("/toResetRegistry")
def checkReset():
    return send_from_directory('templates','reset.html')

@app.route("/RegistryReset",methods=["POST","DELETE"])
def ResetRegistry():
    delete = requests.delete(BASE + 'reset')
    return delete.json(), delete.status_code

@app.route("/getPackageID")
def getID():
    return send_from_directory('templates','packageID.html')

@app.route("/packageIDQuery",methods=["POST","GET"])
def displayID():
    ID = request.form.get("ID")
    data = requests.get(BASE + 'package/'+ID)
    return data.json(), data.status_code

@app.route("/packageIDDelete",methods=["POST","DELETE"])
def deleteID():
    ID = request.form.get("ID")
    data = requests.delete(BASE + 'package/'+ID)
    return data.json(), data.status_code

@app.route("/packageRateID")
def getRateID():
    return send_from_directory('templates','rateID.html')

@app.route("/packageIDRate",methods=["POST","DELETE"])
def RateID():
    ID = request.form.get("Rate")
    data = requests.get(BASE + 'package/' + ID + "/rate")
    return data.json(), data.status_code

#@bp.get("/upload")
#def toUpload():
    #print("testing file")
    #return render_template('mainPage.html')
    #return send_from_directory('templates','upload.html')

@app.route("/uploadContent", methods = ["POST"])
def handleUploaded():
    URL = request.form.get("URL")
    ZipFile = request.files.get("File")
    headers = {'Content-Type': 'application/json'}
    if len(URL) != 0 and ZipFile.read() != b"":
        abort(400)
    elif URL != "":
        response = requests.post(BASE + 'package',json = {'URL' : URL,'ZipFile' : None},headers = headers)
    elif ZipFile != None:
        ZipFile_string = base64.b64encode(ZipFile.read()).decode('utf-8')
        response = requests.post(BASE + 'package',json = {'URL' : None,'ZipFile' : ZipFile_string},headers = headers)
    else:
        abort(501)
    return response.json(), response.status_code


if __name__ == "__main__":
    # app.register_blueprint(bp)
    app.run(host="localhost",port = 8000, debug=True)
