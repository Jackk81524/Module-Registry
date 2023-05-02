from flask import Flask, render_template, send_from_directory, request, abort
from flask_restful import Api, Resource, reqparse
import re
from enum import Enum
import subprocess
import os
from website.models.sql_table import *
import json
import tempfile
import zipfile
import requests 
import base64
import io
from google.cloud import storage
from google.cloud.storage import Bucket
from dotenv import load_dotenv
import tempfile
# ONLY for testing purposes on local machine. Private Key Grab and Authentication ONLY required to test on local machine. You need to have pKey.json in directory for below code to run.
# storage_client = storage.Client.from_service_account_json('pKey.json')

# Authentication Step for Google Cloud Storage Services
# storage_client = storage.Client()

def updatePackage(MetaData,Data,ID):
    if "URL" in Data and Data["URL"] != None:
        URL = Data["URL"]
        ratings = rate_Package(URL)
        add_package(MetaData["Name"],MetaData["Version"],ratings,URL,ID=ID,JS=Data["JSProgram"])
        ZipFile = download_fromURL(URL)
        ZipFile = base64.b64encode(ZipFile.read()).decode('utf-8')
        MetaDataObj = PackageMetadata(MetaData["Name"],MetaData["Version"])
        uploadToBucket(ZipFile,MetaDataObj.blob_name(), 'bucket-proto1')
        return make_response(jsonify({'description': 'Version is updated.'}), 200)
    elif "Content" in Data and Data["Content"] != None:
        ZipFile_bytes = base64.b64decode(Data["Content"].encode('utf-8'))
        ZipFile_buffer = io.BytesIO(ZipFile_bytes)
        MetaDatax, URL = extract_packageURL(ZipFile_buffer)
        ratings = rate_Package(URL)
        MetaDataObj = PackageMetadata(MetaData["Name"],MetaData["Version"])
        add_package(MetaData["Name"],MetaData["Version"],ratings,URL,ID=ID,JS=Data["JSProgram"])
        uploadToBucket(Data["Content"],MetaDataObj.blob_name(), 'bucket-proto1')
        #Data = PackageData(JS,request.json["ZipFile"])
        return make_response(jsonify({'description': 'Version is updated.'}), 200)

def OffsetReturn(output,offset):
    perPage = 15
    length = len(output)
    if(length < perPage and offset > 1):
        return []
    elif length < perPage:
        return output
    else:
        startIndex = (offset-1) * perPage
        endIndex = (startIndex) + perPage
        if startIndex > (length-1):
            return []
        elif endIndex > (length-1):
            endIndex = length - 1
    if(startIndex==endIndex):
        return [output[startIndex]]
    return output[startIndex:endIndex]

def downloadFromBucket(moduleName, bucketName='bucket-proto1'):
    # storage_client = storage.Client.from_service_account_json('pKey.json')
    storage_client = storage.Client()
    # exists = Bucket(storage_client, moduleName).exists()
    bucket = storage_client.bucket(bucketName)
    blob = bucket.blob(moduleName)
    if blob.exists():
        # address = "https://storage.googleapis.com/"
        # address += bucketName + '/'
        # address += moduleName
        # # address = 'https://storage.googleapis.com/bucket-proto1/lodash-5.0.0'
        # return address
        b = blob.download_as_string()
        string = b.decode('utf-8')
        ZipFile_bytes = base64.b64decode(string.encode('utf-8'))
        ZipFile = io.BytesIO(ZipFile_bytes)
        MetaData, URL = extract_packageURL(ZipFile)
        return PackageData(None,string, URL)

    else:
        print("Error: Module not found")
        return 0

def uploadToBucket(contents, destination_blob_name, bucket_name='bucket-proto1'):
    # storage_client = storage.Client.from_service_account_json('pKey.json')
    storage_client = storage.Client()
    # destination_blob_name = "storage-object-name"
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(contents)

    #Ensure upload is succesful
    exists = Bucket(storage_client, bucket_name).exists()
    if exists:
        # print(f"{destination_blob_name} with contents {contents} uploaded to {bucket_name}.")
        return 1
    else:
        print("Error: Module not updated")
        return 0

def download_fromURL(URL):
    token = os.getenv('GITHUB_TOKEN')
    urls = URL.split("/")
    api_url = urls[0] + '//api.' + urls[2] + '/repos/' + urls[3] + "/" + urls[4]
    filename = urls.pop()
    response = requests.get(api_url, headers = {'Authorization': 'token ' + token})
    default_branch = response.json()["default_branch"]
    zip_url = f"{URL}/archive/{default_branch}.zip"
    response = requests.get(zip_url)
    stream = io.BytesIO(response.content)
    return stream



def get_packageJson(url):
    urls = url.split("/")
    api_url = urls[0] + '//api.' + urls[2] + '/repos/' + urls[3] + "/" + urls[4] + "/contents/package.json"
    response = requests.get(api_url)
    file_content = json.loads(response.content)["content"]
    content = base64.b64decode(file_content)
    content = json.loads(content)
    MetaData = PackageMetadata(content["name"],content["version"])
    return MetaData


def extract_packageURL(ZipFile):
    with zipfile.ZipFile(ZipFile, mode="r") as archive:
        for info in archive.infolist():
            if info.filename.endswith('package.json'):
                # print('Match: ', info.filename)
                if '/' in info.filename: # handle subdirectories
                    # create a temporary directory
                    with tempfile.TemporaryDirectory() as tmp_dir:
                        archive.extractall(tmp_dir)
                        sub_dir, file_name = os.path.split(info.filename)
                        file_path = os.path.join(tmp_dir, sub_dir, file_name)
                        with open(file_path, 'r') as f:
                            data = json.loads(f.read())
                            # print(contents)
                else:
                    with archive.open(info.filename) as f:
                        data = json.loads(f.read())
    if "homepage" in data:
        return PackageMetadata(data["name"],data["version"]),data["homepage"]
    else:
        return PackageMetadata(data["name"],data["version"]), None

def uploadRatings(Name,Version,ratings,URL,JS = None,trusted = False):
    if trusted:
        try:
            ID = add_package(Name,Version,ratings,URL,JS)
        except:
            abort(409, "Package exists already")
        # ID = add_package(Name,Version,ratings,URL,JS)
        return ID
    else:
        for metric,score in ratings.items():
            if metric != "URL":
                if float(score) < 0.5:
                    return abort(424, "Package is not uploaded due to the disqualified rating.")
        ID =  add_package(Name,Version,ratings,URL,JS)
    return ID
    


def rate_Package(URL):
    default = {"URL":URL,"NetScore":-1,"RampUp":-1,"Correctness":-1,"BusFactor":-1,"ResponsiveMaintainer":-1,"License":-1}
    # if URL == None:
    #     return default
    # print(os.getcwd())
    # # os.chdir('/home/shay/a/knox36/Documents/Module-Reg-withSwagger/Module-Registry/')
    # with tempfile.NamedTemporaryFile(mode='w') as f:
    #     f.write(URL)
    #     subprocess.run(['./run','build'])
    #     result = subprocess.run(['./run', f.name],capture_output = True, text = True)
    #     output = result.stdout
    #     print('out',output)
    # # os.chdir("/home/shay/a/knox36/Documents/Module-Reg-withSwagger/Module-Registry/Flask/")
    # if output != '' and output != None:
    #     print('out',output)
    #     return json.loads(output)
    # else:
    return default


def MetaData_reqparse():
    args = reqparse.RequestParser()
    args.add_argument("Name",type = str,help = "Name of package is required",required = True)
    args.add_argument("Version",type = str,help = "Version is required",required = True)
    return args

class Error:
    def __init__(self,code,message):
        self.code = code
        self.message = message

    def abort_check(self):
        if(self.code == 200 or self.code == 201):
            return
        if(self.code == 400):
            abort(self.code,'There is missing field(s) in the PackageID/AuthenticationToken\
            \ or it is formed improperly, or the AuthenticationToken is invalid.')
        if(self.code == 413):
            abort(self.code,'Too many packages returned.')   
        if(self.code == 401):
            abort(self.code,'You do not have permission to reset the registry.')
        if(self.code == 404):
            abort(self.code,'Package does not exist.')
        if(self.code == 424):
            abort(self.code,'Package is not uploaded due to the disqualified rating.') 
        if(self.code == 500):
            abort(self.code,'The package rating system choked on at least one of the metrics.')
        else:
            abort(self.code,self.message)
        

class PackageMetadata:
    def __init__(self,Name,Version,ID=None):
        self.Name = PackageName(Name)
        self.Version = SemverRange(Version)
        self.ID = ID
    
    def to_dict(self,ID = False):
        resource_fields = {
            'Version': self.Version.Version,
            'Name': self.Name.Name
        }
        if ID == True:
            resource_fields["ID"] = self.ID
        return resource_fields
    
    def blob_name(self):
        return self.Name.Name + '-' + self.Version.Version

class PackageID:
    def __init__(self, ID):
        id_format = (r'\d+')
        if re.match(id_format, ID):
            self.ID = ID
        else:
            abort(404,"Package does not exist.")
class PackageQuery:
    def __init__(self,Name,Version=None):
        self.Name = PackageName(Name)
        self.Version = SemverRange(Version)
        
class SemverRange:
    def __init__(self,Version):
        version_format = (r'(\^|\~)?(\d+\.\d+\.\d+)(\-\d+\.\d+\.\d+)?')
        if Version == None:
            self.Version = None
        elif re.match(version_format, Version):
            self.Version = Version
        else:
            self.Version = None 
            abort(404,"Package does not exist.")
            ## log incorrect version format

class PackageName:
    def __init__(self,Name):
        name_format = (r'[ -~]+')
        search = re.search(r'\*', Name)
        if Name == None:
            abort(404,"Package does not exist.")
        elif (search != None and len(Name) != 1):
            abort(404,"Package does not exist.")
        elif re.match(name_format, Name):
            self.Name = Name
        else:
            abort(404,"Package does not exist.")

class EnumerateOffset:
    def __init__(self,request):
        self.offset = str(request.args.get('offset',default = 1, type = int))


class Package:
    def __init__(self,Name,Version,Data):
        self.MetaData = MetaData(Name,Version)
        self.PackageData = Data

class PackageData:
    def __init__(self,JSProgram, content = None,URL = None):
        self.content = content
        self.URL = URL
        self.JSProgram = JSProgram

    def to_dict(self,URL_check = False):
        resource_fields = {
            'Content': self.content
        }
        if self.JSProgram != None:
            resource_fields["JSProgram"] = self.JSProgram
        if URL_check == True and self.URL != None:
            resource_fields["URL"] = self.URL 
        return resource_fields


class PackageRating:
    def __init__(self,RampUp,Correctness,BusFactor,ResponsiveMaintainer,LicenseScore,GoodPinningPractice,PullRequest,NetScore,URL):
        self.RampUp = RampUp
        self.Correctness = Correctness
        self.BusFactor = BusFactor
        self.ResponsiveMaintainer = ResponsiveMaintainer
        self.LicenseScore = LicenseScore
        self.GoodPinningPractice = GoodPinningPractice
        self.PullRequest = PullRequest
        self.NetScore = NetScore
        self.URL = URL

    def to_dict(self):
        ret = {
            "URL":self.URL,
            "NET_SCORE":self.NetScore,
            "RAMP_UP_SCORE":self.RampUp,
            "CORRECTNESS_SCORE":self.Correctness,
            "BUS_FACTOR_SCORE": self.BusFactor,
            "RESPONSIVE_MAINTAINER_SCORE": self.ResponsiveMaintainer,
            "LICENSE_SCORE":self.LicenseScore,
            "GOOD_PINNING_PRACTICE_SCORE": self.GoodPinningPractice,
            "PULL_REQUEST_SCORE":self.PullRequest
        }
        return ret


class PackageHistoryEntry:
    def __init__(self,User,Date,PackageMetadata,Action):
        self.User = User
        self.Date = Date
        self.PackageMetadata = PackageMetadata
        self.Action = Action

class User:
    def __init__(self,Name,isAdmin):
        self.Name = Name
        self.isAdmin = isAdmin

class Action(Enum):
    CREATE = 'CREATE'
    UPDATE = 'UPDATE'
    DOWNLOAD = 'DOWNLOAD'
    RATE = 'RATE'



