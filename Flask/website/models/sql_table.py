from flask_sqlalchemy import SQLAlchemy
from flask import make_response,jsonify
from sqlalchemy import text
import sqlalchemy
from google.cloud.sql.connector import Connector, IPTypes
import pymysql
from google.cloud import storage

def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    instance_connection_name = "module-registry-ece461:us-central1:ece461-module-registry"
    # db_user = "461-user"  # e.g. 'my-db-user'
    # db_pass = "461-test"  # e.g. 'my-db-password'
    # db_name = "Module-Registry"  # e.g. 'my-database'
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]

    ip_type = IPTypes.PUBLIC

    connector = Connector(ip_type)

    def getconn() -> pymysql.connections.Connection:
        conn: pymysql.connections.Connection = connector.connect(
            instance_connection_name,
            "pymysql",
            user=db_user,
            password=db_pass,
            db=db_name,
        )
        return conn

    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn
        # ...
    )
    return pool

db = SQLAlchemy()

class Packages_table(db.Model):
    ID = db.Column(db.Integer, primary_key=True, nullable=False,autoincrement=True)
    NAME = db.Column(db.String(255), unique=True, nullable=True)
    VERSION = db.Column(db.String(50), nullable=True)
    RAMPUP = db.Column(db.Float, nullable=True)
    CORRECTNESS = db.Column(db.Float, nullable=True)
    BUSFACTOR = db.Column(db.Float, nullable=True)
    RESPONSIVEMAINTAINER = db.Column(db.Float, nullable=True)
    LICENSESCORE = db.Column(db.Float, nullable=True)
    GOODPINNINGPRACTICE = db.Column(db.Float, nullable=True)
    PULLREQUEST = db.Column(db.Float, nullable=True)
    NETSCORE = db.Column(db.Float, nullable=True)
    URL = db.Column(db.String(99),nullable = True)
    JS = db.Column(db.String(1000),nullable = True)


def add_package(Name,Version,ratings,URL,JS,ID = None):
    if ID == None:
        new_package = Packages_table(
            NAME = Name,VERSION = Version,
            NETSCORE = ratings["NetScore"],
            RAMPUP = ratings["RampUp"],
            CORRECTNESS = ratings["Correctness"],
            BUSFACTOR = ratings["BusFactor"],
            RESPONSIVEMAINTAINER = ratings["ResponsiveMaintainer"],
            LICENSESCORE = ratings["License"],
            URL = URL,
            JS = JS
            )
    else:
        new_package = Packages_table(
            NAME = Name,VERSION = Version,
            NETSCORE = ratings["NetScore"],
            RAMPUP = ratings["RampUp"],
            CORRECTNESS = ratings["Correctness"],
            BUSFACTOR = ratings["BusFactor"],
            RESPONSIVEMAINTAINER = ratings["ResponsiveMaintainer"],
            LICENSESCORE = ratings["License"],
            URL = URL,
            JS = JS,
            ID = ID
            )
    db.session.add(new_package)
    db.session.commit()
    Q = db.session.query(Packages_table).filter_by(NAME=Name,VERSION=Version)[0]
    return (Q.ID)

def query_package(Query):
    Name = Query.Name.Name
    Version = Query.Version.Version
    if Version == None:
        result = db.session.query(Packages_table).filter_by(NAME = Name).all()
    else:
        result = db.session.query(Packages_table).filter_by(NAME = Name,VERSION=Version).all()
    return result

def query_byID(ID):
    return db.session.query(Packages_table).filter_by(ID = ID).all()

def query_all_packages():
    return db.session.query(Packages_table).all()

def delete_by_id(ID):
    Exists = db.session.query(Packages_table).filter_by(ID=ID).all()
    if Exists != []:
        db.session.query(Packages_table).filter_by(ID=ID).delete()
        db.session.commit()
    else:
        return make_response(jsonify({'desciption' : 'Package does not exist.'}), 404)
    return make_response(jsonify({'desciption' : 'Success.'}), 200)

def reset_all_packages():
    storage_client = storage.Client()
#     storage_client = storage.Client.from_service_account_json('pKey.json')
    bucket = storage_client.bucket('bucket-proto1')
    for blob in bucket.list_blobs():
        blob.delete()
    db.session.query(Packages_table).delete()
    db.session.commit()
    # pool = connect_with_connector()
    # with pool.connect() as conn:
    #     conn.execute(text("TRUNCATE TABLE packages_table"))

def reset_ID_packages(PackageID):
    ID = PackageID.ID
    db.session.query(Packages_table).filter_by(ID=ID).delete()
    db.session.commit()

def query_ratings(PackageID):
    ID = PackageID.ID
    return db.session.query(Packages_table).filter_by(ID=ID).all()

    


