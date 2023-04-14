from website import create_app
from flask_restful import Api, Resource
from flask import Flask, request
from website.frontend import bp

app = create_app()

@app.get("/")
def hello():
    """Return a friendly HTTP greeting."""
    who = request.args.get("who", default="World")
    return f"Hello {who}!\n"

if __name__ == "__main__":
    app.register_blueprint(bp)
    app.run(host="localhost", port=8080, debug=True)
