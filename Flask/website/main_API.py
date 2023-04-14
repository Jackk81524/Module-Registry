from flask import Flask, render_template, send_from_directory, request, make_response, jsonify, abort
from flask_restful import Api, Resource, reqparse
from website.models.sql_table import *
from website.components_API import *
import json
import base64


packages = {"lodash" : ["lodash","v2.2.2"]}

class PackagesList(Resource):
    def post(self):
        PackagesToQuery = request.json["PackageQuery"]
        offset = EnumerateOffset(request)
        output = {'value':[]}
        if(len(PackagesToQuery) == 1 and PackagesToQuery[0] == "*"):
            Queried = query_all_packages()
        else:
            for package in PackagesToQuery:
                if 'Version' in package:
                    Query = PackageQuery(package['Name'],package['Version'])
                else:
                    Query = PackageQuery(package['Name'])
                Queried = query_package(Query)
        for data in Queried:
            QueriedMetaData = PackageMetadata(data.NAME,data.VERSION,data.ID)
            output['value'].append(QueriedMetaData.to_dict())
        return json.dumps(output), 200


class RegistryReset(Resource):
    def delete(self):
        reset_all_packages()
        return make_response(jsonify({'description': 'Registry is reset.'}), 200)

class Package(Resource):
    def get(self,id):
        ID = PackageID(id)
        Info = query_byID(ID)[0]
        MetaData = PackageMetadata(Info.NAME,Info.VERSION,Info.ID) 
        ## Need Package Data
        return make_response(jsonify({'value' : {'metadata' : MetaData.to_dict(ID=True)}}),200)

    # Need to access buckets to update     
    # def put(self,id):
    #     ID = PackageID(id)
    #     Packages_update_args = MetaData_reqparse()
    #     ## One more field, but need to ask about package data
    #     args = Packages_update_args.parse_args()
    #     ## Name, Version, and ID must match, update package contents
    #     return {"description" : "Version is updated"}
    def delete(self,id):
        ID = PackageID(id)
        reset_ID_packages(ID)
        return make_response(jsonify({'description': 'Package is deleted.'}), 200)


class PackageCreate(Resource):
    def post(self):
        if "URL" in request.json and request.json["URL"] != None:
            ## Handle URL
            return make_response(jsonify({'description': 'URL success.'}), 200)
        elif "ZipFile" in request.json and request.json["ZipFile"] != None:
            return make_response(jsonify({'Content': request.json["ZipFile"]}), 200)

        return {'description' : 'Not as expected'}


class PackageRate(Resource):
    def get(self,id):
        ID = PackageID(id)
        ## Get ratings of the packages based on id
        # PackageRating = PackageRating(ratings)
        return {'description':'Return the rating. Only use this if each metric was computed successfully.'}

# class CreateAuthToken(Resource):

class PackageHistory(Resource):
    def get(self,Name):
        ## Need to authenticate and retrieve info
        ## Output using PackageHistoryEntry class
        return 200
    def delete(self,Name):
        ## Delete all versions of package with this name
        return 200

class PackageByRegExGet(Resource):
    def post(self,regex):
        ## use regex expression to search database
        ## Return a list of packages metadata
        return 200