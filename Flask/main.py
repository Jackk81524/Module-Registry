from website import create_app
from flask import Flask, request, render_template, send_from_directory, jsonify
import requests
from flask_restful import abort
import json
from google.cloud import storage
from google.cloud.storage import Bucket
import base64
import zipfile
import os
from dotenv import load_dotenv
import ast
load_dotenv()


app = create_app()
BASE = 'https://module-registry-website-4a33ebcq3a-uc.a.run.app/'
# BASE = 'http://localhost:8000/'

@app.route("/")
def defaultPage():
    return render_template('mainPage.html')

### START FROTNEND FOR /packages ENDPOINT
@app.route("/packagesListInput")
def packagesListInput():
    return send_from_directory('templates', 'packages.html')


# Post request that retrieves array from /pacakgesListInput, called under action in html file
@app.route("/packagesList", methods=["POST"])
def packagesListDisplay():
    data = request.form.get("Query")
    offset = request.form.get("Offset")
    headers = {'Content-Type': 'application/json'}
    if data == "[*]":
        response = requests.post(BASE + f'packages?offset={offset}', json=["*"], headers=headers)
    else:
        response = requests.post(BASE + f'packages?offset={offset}', json=json.loads(data), headers=headers)
    items = ast.literal_eval(response.json())
    if response.status_code == 413:
        return response.json()
    return render_template('return_packages.html',items=items)
    # return 'test'
## END FRONTEND FOR /packages ENDPOINT

@app.route("/toResetRegistry")
def checkReset():
    return send_from_directory('templates', 'reset.html')


@app.route("/RegistryReset", methods=["POST", "DELETE"])
def ResetRegistry():
    delete = requests.delete(BASE + 'reset')
    return delete.json(), delete.status_code

@app.route("/getPackageID")
def getID():
    return send_from_directory('templates', 'packageID.html')


@app.route("/packageIDQuery", methods=["POST", "GET"])
def displayID():
    ID = request.form.get("ID")
    data = requests.get(BASE + 'package/' + ID)
    return data.json(), data.status_code

@app.route("/packageIDUpdate")
def upadteID():
    return send_from_directory('templates', 'update.html')

@app.route("/packageUpdate",methods = ["POST"])
def updateStatus():
    ID = request.form.get("ID")
    Name = request.form.get("Name")
    Version = request.form.get("Version")
    URL = request.form.get("URL")
    ZipFile = request.files.get("File")
    JS = request.form.get("JSProgram")
    if len(JS) == 0:
        JS = None
    headers = {'Content-Type': 'application/json'}
    if len(URL) != 0 and ZipFile.read() != b"":
        abort(400)
    elif URL != "":
        response = requests.put(BASE + 'package/' + ID, json={"metadata" : {"Name" : Name,"Version" : Version}, "data" : {"Content" : None,"URL" : URL,"JSProgram":JS}}, headers=headers)
    elif ZipFile != None:
        ZipFile_string = base64.b64encode(ZipFile.read()).decode('utf-8')
        response = requests.put(BASE + 'package/' + ID, json={"metadata" : {"Name" : Name,"Version" : Version}, "data" : {"Content" : ZipFile_string,"URL" : None,"JSProgram":JS}}, headers=headers)
    else:
        abort(501)
    return response.json(), response.status_code

@app.route("/packageIDDelete", methods=["POST", "DELETE"])
def deleteID():
    ID = request.form.get("ID")
    data = requests.delete(BASE + 'package/' + ID)
    return data.json(), data.status_code


@app.route("/packageRateID")
def getRateID():
    return send_from_directory('templates', 'rateID.html')


@app.route("/packageRatings", methods=["GET","POST", "DELETE"])
def RateID():
    ID = request.form.get("Rate")
    data = requests.get(BASE + 'package/' + ID + "/rate")
    return data.json(), data.status_code


@app.route("/upload")
def uploadPage():
    return render_template('upload.html')

@app.route("/uploadContent", methods=["POST"])
def handleUploaded():
    URL = request.form.get("URL")
    ZipFile = request.files.get("File")
    JS = request.form.get("JSProgram")
    if len(JS) == 0:
        JS = None
    headers = {'Content-Type': 'application/json'}
    if len(URL) != 0 and ZipFile.read() != b"":
        abort(400)
    elif URL != "":
        response = requests.post(BASE + 'package', json={'URL': URL, 'Content': None, 'JSProgram': JS}, headers=headers)
    elif ZipFile != None:
        ZipFile_string = base64.b64encode(ZipFile.read()).decode('utf-8')
        response = requests.post(BASE + 'package', json={'URL': None, 'Content': ZipFile_string, 'JSProgram': JS}, headers=headers)
    else:
        abort(501)
    return response.json(), response.status_code


if __name__ == "__main__":
    # app.register_blueprint(bp)
    app.run(host="localhost", port=8080, debug=True)
    # app.run()
