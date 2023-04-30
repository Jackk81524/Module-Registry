from Flask.website.main_API import *
from google.cloud.sql.connector import Connector, IPTypes
from Flask.website.models.sql_table import db


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
    api.add_resource(PackageRate,"/package/rate")
    api.add_resource(PackageByRegExGet,"/package/byRegex/<string:rate>")

    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://461-user:461-test@/Module-Registry?unix_socket=/cloudsql/module-registry-ece461:us-central1:ece461-module-registry"

    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "creator": getconn
    }

    db.init_app(app)
    return app
    

