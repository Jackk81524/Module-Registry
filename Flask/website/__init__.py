from flask import Flask
from flask_restful import Api, Resource
from website.main_API import PackageQuery

def create_app():
    app = Flask(__name__)
    api = Api(app)

    # from .views import views
    api.add_resource(PackageQuery,"/packages")
    # app.register_blueprint(views, url_prefix = '/')

    return app