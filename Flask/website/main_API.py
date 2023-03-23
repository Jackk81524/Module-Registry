from flask import Flask, render_template, send_from_directory, request
from flask_restful import Api, Resource


packages = {"lodash" : ["lodash","v2.2.2"]}

class PackageQuery(Resource):
    def post(self):
        data = request.form.get("Query")
        return {"data":packages[data]}
    def get(self):
        return send_from_directory('templates','packages.html')

