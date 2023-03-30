from flask import Flask, render_template, send_from_directory, request
from flask_restful import Api, Resource, reqparse
from website.models.sql_table import add_pacakage


packages = {"lodash" : ["lodash","v2.2.2"]}

class Packages(Resource):
    def post(self):
        data = request.form.get("Query")
        ## Need to figure out the format of input and format to be able to pass in below
        toQuery = PackageQuery(Name,Version)
        ## Retrieve data from database GCP
        # return data
    def get(self):
        return send_from_directory('templates','packages.html')


class Package(Resource):
    def get(self):
        return send_from_directory('templates','package.html')



