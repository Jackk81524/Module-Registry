from flask import Flask
from flask_restful import Api, Resource
from website.main_API import *
import pymysql
from flask_sqlalchemy import SQLAlchemy
from google.cloud.sql.connector import Connector, IPTypes
from website.models.sql_table import db, Packages_table, add_package
import requests
import sqlalchemy

def getconn():
    with Connector() as connector:
        conn = connector.connect(
            "module-registry-ece461:us-central1:ece461-module-registry",
            "pymysql",
            user="461-user",
            password="461-test",
            db="Module-Registry",
            ip_type= IPTypes.PUBLIC 
        )
        return conn
# def connect_with_connector() -> sqlalchemy.engine.base.Engine:
#     """
#     Initializes a connection pool for a Cloud SQL instance of MySQL.

#     Uses the Cloud SQL Python Connector package.
#     """
#     # Note: Saving credentials in environment variables is convenient, but not
#     # secure - consider a more secure solution such as
#     # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
#     # keep secrets safe.

#     instance_connection_name = "module-registry-ece461:us-central1:ece461-module-registry"
#     db_user = "461-user"  # e.g. 'my-db-user'
#     db_pass = "461-test"  # e.g. 'my-db-password'
#     db_name = "Module-Registry"  # e.g. 'my-database'

#     ip_type = IPTypes.PUBLIC

#     connector = Connector(ip_type)

#     def getconn() -> pymysql.connections.Connection:
#         conn: pymysql.connections.Connection = connector.connect(
#             instance_connection_name,
#             "pymysql",
#             user=db_user,
#             password=db_pass,
#             db=db_name,
#         )
#         return conn

#     pool = sqlalchemy.create_engine(
#         "mysql+pymysql://",
#         creator=getconn
#         # ...
#     )
#     return pool


def create_app():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(PackagesList,"/packages")
    api.add_resource(RegistryReset,"/reset")
    api.add_resource(Package,"/package/<string:id>")
    api.add_resource(PackageCreate,"/package")
    api.add_resource(PackageRate,"/package/rate")
    api.add_resource(PackageHistory,"/package/byName/<string:name>")
    api.add_resource(PackageByRegExGet,"/package/byRegex/<string:rate>")
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://461-user:461-test@/Module-Registry?unix_socket=/cloudsql/module-registry-ece461:us-central1:ece461-module-registry"

    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "creator": getconn
    }
    db.init_app(app)
    return app
    

