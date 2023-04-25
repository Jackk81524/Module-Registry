from decouple import config
from website import create_app
from flask import Flask, request, render_template, send_from_directory
import requests
from flask_restful import abort
import json
from google.cloud import storage
from google.oauth2 import service_account
import base64
import zipfile
import os
from dotenv import load_dotenv
load_dotenv()

#Private Key Grab and Authentication
#pKey = os.environ.get('P_KEY')
gcp_json_credentials_dict = json.loads('/gcs-key')
credentials = service_account.Credentials.from_service_account_info(gcp_json_credentials_dict)
client = storage.Client(project=gcp_json_credentials_dict['project_id'], credentials=credentials)

#Storing File called myfile# onto Storage Bucket
bucket = client.get_bucket('bucket-proto1')
blob = bucket.blob('myfileTest')
blob.upload_from_filename('main.py')


app = create_app()
BASE = 'https://module-registry-website-4a33ebcq3a-uc.a.run.app/'
BASE = 'http://localhost:8000/'
@app.route("/")
def defaultPage():
    return render_template('mainPage.html')

@app.route("/upload")
def uploadPage():
    return render_template('upload.html')


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
        Zip2 = ZipFile
        with zipfile.ZipFile(ZipFile, mode="r") as archive:
            for info in archive.infolist():
                print(info.filename)
                if info.filename.endswith('.json'):
                    print('Match: ', info.filename)
                    archive.extract(info.filename, info.filename)
        ZipFile_string = base64.b64encode(ZipFile.read()).decode('utf-8')
        response = requests.post(BASE + 'package',json = {'URL' : None,'ZipFile' : ZipFile_string},headers = headers)
    else:
        abort(501)
    return response.json(), response.status_code


if __name__ == "__main__":
    # app.register_blueprint(bp)
    app.run(host="localhost",port = 8000, debug=True)
