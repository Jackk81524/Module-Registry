from flask import Flask
from flask_restful import Api, Resource
from website.main_API import PackagesList, RegistryReset
import pymysql
from flask_sqlalchemy import SQLAlchemy
from google.cloud.sql.connector import Connector, IPTypes
from website.models.sql_table import db, Packages_table

def getconn():
    with Connector() as connector:
        conn = connector.connect(
           ## get from sql into doc, need to configure to env file
        )
        return conn


def create_app():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(PackagesList,"/packages")
    api.add_resource(RegistryReset,"/reset")
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://461-user:461-test@/Module-Registry?unix_socket=/cloudsql/module-registry-ece461:us-central1:ece461-module-registry"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "creator": getconn
    }
    db.init_app(app)
    return app
    

