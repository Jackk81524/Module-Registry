from website import create_app
from flask_restful import Api, Resource
from flask import Flask, request, render_template
from website.frontend import bp
import datetime
from google.cloud import storage


app = create_app()

@app.get("/")
def defaultPage():
    return render_template('mainPage.html')

@app.get("/upload")
def uploadPage():

    key =
    storage_client = storage.Client()
    policy = storage_client.generate_signed_post_policy_v4(
        "bucket-proto1",
        "blob_name2",
        expiration=datetime.timedelta(minutes=10),
        fields={
            'x-goog-meta-test': 'data'
        }
    )

    # Create an HTML form with the provided policy
    header = "<form action='{}' method='POST' enctype='multipart/form-data'>\n"
    form = header.format(policy["url"])

    # Include all fields returned in the HTML form as they're required
    for key, value in policy["fields"].items():
        form += f"  <input name='{key}' value='{value}' type='hidden'/>\n"

    form += "  <input type='file' name='file'/><br />\n"
    form += "  <input type='submit' value='Upload File' /><br />\n"
    form += "</form>"

    print(form)

    return form
    #return render_template('upload.html')


if __name__ == "__main__":
    app.register_blueprint(bp)
    app.run(host="localhost",port = 8080, debug=True)
