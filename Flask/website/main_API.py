from flask import Flask, render_template, send_from_directory, request, make_response, jsonify, abort
from flask_restful import Api, Resource, reqparse
from website.models.sql_table import *
from website.components_API import *
import json
import base64
import io
# from main import storage_client


### /packages endpoint
class PackagesList(Resource):
    def post(self):
        PackagesToQuery = request.json
        if(len(PackagesToQuery) > 100):
            return json.dumps({'message' : 'Too many packages returned.'}), 413
        offset = EnumerateOffset(request).offset
        output = []
        if(len(PackagesToQuery) == 1 and PackagesToQuery[0] == "*"):
            Queried = query_all_packages()
            for data in Queried:
                QueriedMetaData = PackageMetadata(data.NAME,data.VERSION,data.ID)
                output.append(QueriedMetaData.to_dict())
        else:
            for package in PackagesToQuery:
                if 'Version' in package:
                    Query = PackageQuery(package['Name'],package['Version'])
                else:
                    Query = PackageQuery(package['Name'])
                Queried = query_package(Query)
                for data in Queried:
                    QueriedMetaData = PackageMetadata(data.NAME,data.VERSION,data.ID)
                    output.append(QueriedMetaData.to_dict())
        ret = OffsetReturn(output,int(offset))
        return json.dumps(ret), 200


class RegistryReset(Resource):
    def delete(self):
        reset_all_packages()
        return make_response(jsonify({'description': 'Registry is reset.'}), 200)

class Package(Resource):
    def get(self,id):
        ID = PackageID(id).ID
        Info = query_byID(ID)
        if Info != []:
            Info = Info[0]
        else:
            return make_response(jsonify({'description' : 'Package does not exist.'}),404)
        MetaData = PackageMetadata(Info.NAME,Info.VERSION,Info.ID) 
        Data = downloadFromBucket(MetaData.blob_name())
        return make_response(jsonify({'value' : [{'metadata' : MetaData.to_dict(ID = True)},{'data' : Data.to_dict(URL_check=True)}]}),200)
    
    def put(self,id):
        ID = PackageID(id).ID
        MetaData = request.json["MetaData"]
        MetaData = request.json["metadata"]
        Data = request.json["data"]
        response2 = delete_by_id(ID)
        if response2.error_status == 404:
            return response2.json()
        update = requests.post(BASE + 'package',json=jsonify(Data), headers=headers)
        return {"description" : "Version is updated"}

    def delete(self,id):
        ID = PackageID(id)
        reset_ID_packages(ID)
        return make_response(jsonify({'description': 'Package is deleted.'}), 200)


class PackageCreate(Resource):
    def post(self):
        JS = request.json["JSProgram"]
        if "URL" in request.json and request.json["URL"] != None:
            print("here url")
            URL = request.json["URL"]
            MetaData = get_packageJson(URL)
            ratings = rate_Package(URL)
            uploadRatings(MetaData.Name.Name,MetaData.Version.Version,ratings,URL,JS,trusted=True)
            ZipFile = download_fromURL(URL)
            ZipFile = base64.b64encode(ZipFile.read()).decode('utf-8')
            uploadToBucket(ZipFile,MetaData.blob_name(), 'bucket-proto1')
            Data = PackageData(JS,ZipFile)
            return make_response(jsonify({'metadata': MetaData.to_dict(),"data": Data.to_dict()}), 200)
        elif "ZipFile" in request.json and request.json["ZipFile"] != None:
            print("here zip")
            ZipFile_bytes = base64.b64decode(request.json["ZipFile"].encode('utf-8'))
            ZipFile_buffer = io.BytesIO(ZipFile_bytes)
            MetaData, URL = extract_packageURL(ZipFile_buffer)
            ratings = rate_Package(URL)
            uploadRatings(MetaData.Name.Name,MetaData.Version.Version,ratings,URL,JS,trusted=True)
            uploadToBucket(request.json["ZipFile"],MetaData.blob_name(), 'bucket-proto1')
            Data = PackageData(JS,request.json["ZipFile"])
            return make_response(jsonify({'metadata': MetaData.to_dict(),"data": Data.to_dict()}), 200)
        return {'description' : 'Not as expected'}


class PackageRate(Resource):
    def get(self,id):
        ID = PackageID(id)
        uploadRatings(rate_Package('testfile.txt'))
        # PackageRating = PackageRating(ratings)
        return {'description':'Return the rating. Only use this if each metric was computed successfully.'}

# class CreateAuthToken(Resource):

class PackageByRegExGet(Resource):
    def post(self,regex):
        ## use regex expression to search database
        ## Return a list of packages metadata
        return 200
