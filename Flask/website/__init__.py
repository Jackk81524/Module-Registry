from flask import Flask
from flask_restful import Api, Resource
import sqlalchemy
from website.main_API import *
from flask_sqlalchemy import SQLAlchemy
from google.cloud.sql.connector import Connector, IPTypes
from website.models.sql_table import db, Packages_table, add_package
import requests
import os
import pymysql


def getconn():
    with Connector() as connector:
        conn = connector.connect(
            "module-registry-ece461:us-central1:ece461-module-registry",
            "pymysql",
            user="461-user",
            password="461-test",
            db="Module-Registry",
            ip_type=IPTypes.PUBLIC
        )
        return conn


def create_app():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(PackagesList,"/packages")
    api.add_resource(RegistryReset,"/reset")
    api.add_resource(Package,"/package/<string:id>")
    api.add_resource(PackageCreate,"/package")
    api.add_resource(PackageRate,"/package/<string:id>/rate")
    api.add_resource(PackageByRegExGet,"/package/byRegex/<string:rate>")

    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://461-user:461-test@/Module-Registry?unix_socket=/cloudsql/module-registry-ece461:us-central1:ece461-module-registry"

    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "creator": getconn
    }

    db.init_app(app)
    return app
    

