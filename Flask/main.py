from website import create_app
from flask_restful import Api, Resource
from website.frontend import bp

app = create_app()


if __name__ == "__main__":
    app.register_blueprint(bp)
    app.run(debug=True)