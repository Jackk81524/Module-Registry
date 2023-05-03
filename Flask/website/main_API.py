from flask import Flask, render_template, send_from_directory, request, make_response, jsonify, abort
from flask_restful import Api, Resource, reqparse
from website.models.sql_table import *
from website.components_API import *
import datetime
import json
import base64
import io
# from main import storage_client
# import logging


# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)

# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s,  Type: %(type)s, Time: %(time)s')

# console_handler = logging.StreamHandler()
# console_handler.setFormatter(formatter)
# logger.addHandler(console_handler)

# file_handler = logging.FileHandler('app.log')
# file_handler.setLevel(logging.INFO)
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)

class PackagesList(Resource):
    def post(self):
        print(f'Request_log: {request.path},{request.json},{request.method},{datetime.datetime.now()}')
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
        print(f'Request_log: {request.path},{request.method},{datetime.datetime.now()}')
        reset_all_packages()
        return make_response(jsonify({'description': 'Registry is reset.'}), 200)

class Package(Resource):
    def get(self,id):
        print(f'Request_log: {request.path},{request.method},{datetime.datetime.now()}')
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
        print(f'Request_log: {request.path},{request.json},{request.method},{datetime.datetime.now()}')
        MetaData = request.json["metadata"]
        Data = request.json["data"]
        ID = PackageID(id).ID
        Data = request.json["data"]
        response2 = delete_by_id(ID)
        if response2.status_code == 404:
             return make_response(jsonify({'desciption' : 'Package does not exist.'}), 404)
        ret = updatePackage(MetaData,Data,id)
        return {"description" : "Version is updated"}

    def delete(self,id):
        print(f'Request_log: {request.path},{request.method},{datetime.datetime.now()}')
        ID = PackageID(id).ID
        response = delete_by_id(ID)
        if response.status_code == 404:
             return make_response(jsonify({'desciption' : 'Package does not exist.'}), 404)
        return make_response(jsonify({'description': 'Package is deleted.'}), 200)


class PackageCreate(Resource):
    def post(self):
        print(f'Request_log: {request.path},{request.json},{request.method},{datetime.datetime.now()}')
        JS = request.json["JSProgram"]
        if "URL" in request.json and request.json["URL"] != None:
            URL = request.json["URL"]
            MetaData = get_packageJson(URL)
            ratings = rate_Package(URL)
            idx = uploadRatings(MetaData.Name.Name,MetaData.Version.Version,ratings,URL,JS,trusted=True)
            MetaData.ID = idx
            ZipFile = download_fromURL(URL)
            ZipFile = base64.b64encode(ZipFile.read()).decode('utf-8')
            uploadToBucket(ZipFile,MetaData.blob_name(), 'bucket-proto1')
            Data = PackageData(JS,ZipFile)
            return make_response(jsonify({'metadata': MetaData.to_dict(ID=True),"data": Data.to_dict()}), 200)
        elif "Content" in request.json and request.json["Content"] != None:
            ZipFile_bytes = base64.b64decode(request.json["Content"].encode('utf-8'))
            ZipFile_buffer = io.BytesIO(ZipFile_bytes)
            MetaData, URL = extract_packageURL(ZipFile_buffer)
            ratings = rate_Package(URL)
            idx = uploadRatings(MetaData.Name.Name,MetaData.Version.Version,ratings,URL,JS,trusted=True)
            MetaData.ID = idx
            uploadToBucket(request.json["Content"],MetaData.blob_name(), 'bucket-proto1')
            Data = PackageData(JS,request.json["Content"])
            return make_response(jsonify({'metadata': MetaData.to_dict(ID=True),"data": Data.to_dict()}), 200)
        return {'description' : 'Not as expected'}


class PackageRate(Resource):
    def get(self,id):
        print(f'Request_log: {request.path},{request.method},{datetime.datetime.now()}')
        ID = PackageID(id).ID
        Info = query_byID(ID)
        if Info != []:
            Info = Info[0]
        else:
            return make_response(jsonify({'description' : 'Package does not exist.'}),404)
        Rating = PackageRating(Info.RAMPUP,Info.CORRECTNESS,Info.BUSFACTOR,Info.RESPONSIVEMAINTAINER,Info.LICENSESCORE,Info.GOODPINNINGPRACTICE,Info.PULLREQUEST,Info.NETSCORE,Info.URL)
        for key, value in Rating.to_dict().items():
            if value == -1.0:
                return make_response(jsonify({'description' : "The package rating system choked on at least one of the metrics."}),500)
        # PackageRating = PackageRating(ratings)
        return Rating.to_dict()

# class CreateAuthToken(Resource):

class PackageByRegExGet(Resource):
    def post(self,regex):
        print(f'Request_log: {request.path},{request.json},{request.method},{datetime.datetime.now()}')
        ## use regex expression to search database
        ## Return a list of packages metadata
        return 200
