from website import create_app
from flask_restful import Api, Resource
from flask import Flask, request, render_template, send_from_directory
from website.frontend import bp
import requests
from flask_restful import abort
import json
#import datetime

# Testing New Feature
from google.cloud import storage
from oauth2client.service_account import ServiceAccountCredentials
import os

with open('pKey.json', 'r') as pKey:
    data = pKey.read()

obj = json.loads(data)

# credentials_dict = {
#     'type': 'service_account',
#     'client_id': os.environ['BACKUP_CLIENT_ID'],
#     'client_email': os.environ['BACKUP_CLIENT_EMAIL'],
#     'private_key_id': os.environ['BACKUP_PRIVATE_KEY_ID'],
#     'private_key': os.environ['BACKUP_PRIVATE_KEY'],
# }

# credentials_dict = {
#     'type': 'service_account',
#     'client_id': '102375219002406842397',
#     'client_email': 'gcs-uploader@module-registry-ece461.iam.gserviceaccount.com',
#     'private_key_id': '496881a5a8eb3803a3acef26c6d04b2040d6c20f',
#     'private_key': "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCdeBZnl3dOJP+h\nt+ElDAO8JGsdAmcJg32hT6AAy9aXiyJ9wCrePA3ASUQPJ0Nf1ZvEcsZPU31WvciM\nGqnGFc/mxwYB6NUr2ps8kXtD7OglEXwUvM05yYRdUl9P25Ln/JeGBj55HRsb4Wqb\n7IVR1KQL2YTkPHALNXghLeq46JR5hKEVOH/iMLPVYGWGxs1K87jFJDEuZD0z5Bos\njR7kkXH+7wf1ZCsQNFKyALojdsnU/uKruTpfeaRQgYGBRs8IMoaTJvQ/m5tW3ZhU\nxeIzpIQKS2+BH6eTZoqLSzR7eR3WL4XkmihI4iBmBjYfDeMitTFP7UKHvwzL47oG\n8xZ0k7g1AgMBAAECggEAFsd+8jhijV7jzfikLLBKwAZCqn0k+6bWXyX+Hu9d2SlK\n8YcBjImCcb0Hh+ulnvDvKiFyV5pbyNcGcmIPCjUwkJFc6JzObZwflcjz3HUide5M\nFVHknEXvDHL0j8BTRZTwNHalxe50c/mNawXxmU9Z9c7fHwcxLCXtfVs/l8UpaVSQ\nvYyHQffnHak9zFrQa/kDx2n+D8nt6ngxRoFO4qjD5Ew2iEvhZIi+E16pJ8yN/gje\n2ceWxqPhK3uUpzrY8htMp3V6JURZ1aIz6uADJjHDPywRPhA6pFwwSVndvEXxxXw6\n4EmhpU6nFX68SK7YufxjgmcGimssa/OsCXcp0AUGAQKBgQDOutHujlkERp84aASB\nEYZdnM1ZlO/oM1IP5yWQpocDfU+QbGh8MUQA2uGh0OwBQoLb7kkRNk/uEnAMs4tX\nbTp2PvQo5qcZINYPOafxHU+xg0+aVOitiYQ8Oe0Z0PiWv/i8OSmm+l0a7O1pAwT9\n1OYmJG62zv06Kyv00sOicJzNNQKBgQDC/7tEZYnch3DRKNdrg0gSafnHF9db+MAP\nTUKUCQsvtasAcGLNOWvlH8CqYbLSHYMXNSgaMe9E+6JxsJ+OGZQXpzcH6/Hmbq4n\nqgtuQMutQG4xHRuCYwZZx4qMZeWHym4946VFNrHxhwkCsuHhDjbNT+gZ64DKdME4\nu0nXRdefAQKBgB2itIOhTmuJgDvC1Zp3G68B0oJcEoRUDxiOh1kUNliutyA6GkRr\nf5cryZq764lGsqG6qCjag1zasctwVbJjyzS2U6QlZKD6jxVBq6yqCgmljFzQfUab\nZySHHVFNHsXloU/CVhFE5OH+Qw6By05kHdYr9N8qDy0ukS+Yo0j/IctdAoGAed0S\nLnt6fbyTL9PjVMh1uTRLqjXnHA5IEQgKrLM+L3HMTXju9iyFlmqSoKhv9coFy/In\nfr9oNedArOZhwI+RsnqI9MVqpsTSx+0IOb36y+pxMvZq48B5DpCasIVZvdQvszPa\nbHfzGut2IR6j9V9JtmPSvKgmE+CFhKvfSM7YIwECgYEArnmUz8vu/QTia1sE+vFK\nqk5mTP4gRkNQDN1LLsFvtmrYxhnXWlR0N1NkHjCDAcie2w+5m8yMzwB6AKhNGCSH\nOMFQVA5KMlCuWoIwHZoOkw3kuB6AoDMezpDSlKH2tREz7EmOY2r45tXDb+AiTJR7\nQQ6e1sUYqpYeUKJB54nIah4=\n-----END PRIVATE KEY-----\n"
# }

#credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict)

client = storage.Client.from_service_account_json('pKey.json')
bucket = client.get_bucket('bucket-proto1')
blob = bucket.blob('myfile')
blob.upload_from_filename('main.py')



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
