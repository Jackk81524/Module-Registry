from flask import Flask
from flask_restful import Api, Resource
import sqlalchemy
from website.main_API import *
from flask_sqlalchemy import SQLAlchemy
from google.cloud.sql.connector import Connector, IPTypes
from website.models.sql_table import Packages_table, add_package
import requests
import os
import pymysql

#
# def getconn():
#     with Connector() as connector:
#         conn = connector.connect(
#             "module-registry-ece461:us-central1:ece461-module-registry",
#             "pymysql",
#             user="461-user",
#             password="461-test",
#             db="Module-Registry",
#             ip_type= IPTypes.PUBLIC
#         )
#         return conn

def get_connect_url():
    db_user = os.environ["DB_USER"]  # e.g. 'my-database-user'
    db_pass = os.environ["DB_PASS"]  # e.g. 'my-database-password'
    db_name = os.environ["DB_NAME"]  # e.g. 'my-database'
    if "INSTANCE_UNIX_SOCKET" in os.environ:
        unix_socket_path = os.environ["INSTANCE_UNIX_SOCKET"]  # e.g. '/cloudsql/project:region:instance'
        return f"postgresql+pg8000://{db_user}:{db_pass}@/{db_name}?unix_sock={unix_socket_path}/.s.PGSQL.5432"
    else:
        # Local test
        db_host=os.environ["DB_HOST"]
        db_port=os.environ["DB_PORT"]
        return f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

# def connect_with_connector() -> sqlalchemy.engine.base.Engine:
#     """
#     Initializes a connection pool for a Cloud SQL instance of MySQL.
#
#     Uses the Cloud SQL Python Connector package.
#     """
#     # Note: Saving credentials in environment variables is convenient, but not
#     # secure - consider a more secure solution such as
#     # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
#     # keep secrets safe.
#
#     instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]  # e.g. 'project:region:instance'
#     db_user = os.environ["DB_USER"]  # e.g. 'my-db-user'
#     db_pass = os.environ["DB_PASS"]  # e.g. 'my-db-password'
#     db_name = os.environ["DB_NAME"]  # e.g. 'my-database'
#
#     ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC
#
#     connector = Connector(ip_type)
#
#     def getconn() -> pymysql.connections.Connection:
#         conn: pymysql.connections.Connection = connector.connect(
#             instance_connection_name,
#             "pymysql",
#             user=db_user,
#             password=db_pass,
#             db=db_name,
#         )
#         return conn
#
#     pool = sqlalchemy.create_engine(
#         "mysql+pymysql://",
#         creator=getconn,
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

    app.config["SQLALCHEMY_DATABASE_URI"] = get_connect_url()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    #app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://461-user:461-test@/Module-Registry?unix_socket=/cloudsql/module-registry-ece461:us-central1:ece461-module-registry"

    #app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        #"creator": getconn
    #}
    db.init_app(app)
    return app
    

