from flask import Flask, render_template, send_from_directory, request, make_response
from flask_restful import Api, Resource, reqparse
from website.models.sql_table import add_pacakage
from website.components_API import PackageQuery, EnumerateOffset


packages = {"lodash" : ["lodash","v2.2.2"]}

class PackagesList(Resource):
    def post(self):
        data = request.form.get("Query")
        Name = 'jack'
        Version = '1.1.1'
        ## Need to figure out the format of input and format to be able to pass in below, using example
        # Return all if * imputted
        toQuery = PackageQuery(Name,Version)
        offset = EnumerateOffset(request)
        ## Retrieve data from database GCP
        ## Depending on how data is retrieved, pass into a dict using MetaData class 
        dict = {
            'value': []
        }
        ''' Need to create dict of this format, depending on format of querried data, here is a potential outline
        count = numPerPage * offset
        for i in range(count, count * 2):
            MetaData = PackageMetadata(Name,Version)
            dict['value'].append(Metadata.jsonify())
        '''
        ## Add autorization 400 error, interpret 413 error once data querried
        return data
    def get(self):
        return send_from_directory('templates','packages.html')


class RegistryReset(Resource):
    def delete(self):
        ## Clear sql and buckets
        del packages['lodash']
        return '', 204
        # return(make_response(jsonify({'message':'Registry is Reset'})),200)

class Package(Resource):
    def get(self):
        return send_from_directory('templates','package.html')



