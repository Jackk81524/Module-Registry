from website import create_app
from flask_restful import Api, Resource
from flask import Flask, request, render_template
from website.frontend import bp

app = create_app()

@app.get("/")
def defaultPage():
    return render_template('mainPage.html')



if __name__ == "__main__":
    app.register_blueprint(bp)
    app.run(host="localhost", port=8080, debug=True)
