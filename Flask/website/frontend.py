from website.__init__ import create_app
import json
from flask import Blueprint, send_from_directory, render_template,  request,jsonify
from website.main_API import *
import requests
from flask_restful import abort


app = create_app()
bp = Blueprint('my_blueprint', __name__)
BASE = 'http://127.0.0.1:5000/'
# Get request that renders html file that takes array as package input
@bp.route("/packagesListInput")
def packagesListInput():
    return send_from_directory('templates','packages.html')

# Post request that retrieves array from /pacakgesListInput, called under action in html file
@bp.route("/packagesList",methods = ["POST"])
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

@bp.route("/toResetRegistry")
def checkReset():
    return send_from_directory('templates','reset.html')

@bp.route("/RegistryReset",methods=["POST","DELETE"])
def ResetRegistry():
    delete = requests.delete(BASE + 'reset')
    return delete.json(), delete.status_code

@bp.route("/getPackageID")
def getID():
    return send_from_directory('templates','packageID.html')

@bp.route("/packageIDQuery",methods=["POST","GET"])
def displayID():
    ID = request.form.get("ID")
    data = requests.get(BASE + 'package/'+ID)
    return data.json(), data.status_code

@bp.route("/packageIDDelete",methods=["POST","DELETE"])
def deleteID():
    ID = request.form.get("ID")
    data = requests.delete(BASE + 'package/'+ID)
    return data.json(), data.status_code

@bp.route("/packageRateID")
def getRateID():
    return send_from_directory('templates','rateID.html')

@bp.route("/packageIDDelete",methods=["POST","DELETE"])
def RateID():
    ID = request.form.get("Rate")
    data = requests.get(BASE + 'package/' + ID + "/rate")
    return data.json(), data.status_code

#@bp.get("/upload")
#def toUpload():
    #print("testing file")
    #return render_template('mainPage.html')
    #return send_from_directory('templates','upload.html')

@bp.route("/uploadContent", methods = ["POST"])
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
