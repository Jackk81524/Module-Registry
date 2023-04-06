from flask import Flask, render_template, send_from_directory, request, make_response, jsonify, abort
from flask_restful import Api, Resource, reqparse
from website.models.sql_table import add_package, query_package
from website.components_API import *
import json


packages = {"lodash" : ["lodash","v2.2.2"]}

class PackagesList(Resource):
    def post(self):
        # Packages_list_args = reqparse.RequestParser()
        # Packages_list_args.add_argument("Name",type = str,help = "Name of package is required",required = True)
        # Packages_list_args.add_argument("Version",type = str,required = False)
        # args = Packages_list_args.parse_args()
        abort(400,message = "Error here")
        PackagesToQuery = request.json["packages"]
        offset = EnumerateOffset(request)
        output = {'value':[]}
        if(len(PackagesToQuery) == 1 and PackagesToQuery[0] == "*"):
            ## Query all
            i = 1
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
        ## Clear sql and buckets
        del packages['lodash']
        print({'data' : 'here'})
        return '', 204
        # return(make_response(jsonify({'message':'Registry is Reset'})),200)

class Package(Resource):
    def get(self,id):
        ## Get package info
        request_type = 'get'
        ID = PackageID(id)
        ## Retrieve info 
        # Need to ask about format of packagedata union type
        # data = PackageData(insert info)
        # package = Package(Name,Version,data)
        return {'test' : id}
    def put(self,id):
        ID = PackageID(id)
        Packages_update_args = MetaData_reqparse()
        ## One more field, but need to ask about package data
        args = Packages_update_args.parse_args()
        ## Name, Version, and ID must match, update package contents
        return {"description" : "Version is updated"}
    def delete(self,id):
        ID = PackageID(id)
        ## Delete package with this id
        return {'description' : 'Package is deleted'}


class PackageCreate(Resource):
    def post(self):
        args = MetaData_reqparse()
        ## Create package in regsiry based on input
        ## Need to update packagedata'
        return {'description' : 'Success. Check the ID in the returned metadata for the official ID.'}


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