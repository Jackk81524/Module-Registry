from website import create_app
from flask_restful import Api, Resource
from flask import Flask, request, render_template
from website.frontend import bp

app = create_app()
app.register_blueprint(bp)

@app.get("/")
def defaultPage():
    return render_template('mainPage.html')

# @app.get("/upload")
# def uploadPage():
#     return render_template('upload.html')


if __name__ == "__main__":
    app.register_blueprint(bp)
    app.run(host="localhost",port = 8080, debug=True)
