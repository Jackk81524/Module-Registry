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

#ONLY for testing purposes on local machine. Private Key Grab and Authentication ONLY required to test on local machine. You need to have pKey.json in directory for below code to run.
# client = storage.Client.from_service_account_json('pKey.json')
# def uploadToBucket():
#     bucket = client.get_bucket('bucket-proto1')
#     blob = bucket.blob('myfileTest2')
#     blob.upload_from_string("testingggg pls work")

#Storing Files from memory onto Storage Bucket
def uploadToBucket(contents, destination_blob_name, bucket_name='bucket-proto1'):
    # destination_blob_name = "storage-object-name"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(contents)
    print(
        f"{destination_blob_name} with contents {contents} uploaded to {bucket_name}."
    )

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
