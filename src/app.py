from flask import Flask, request, jsonify
import json
import requests
import shutil
import logging
import boto3
from botocore.exceptions import ClientError
import os
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__)
# example mysql connection string: mysql://scott:tiger@localhost/foo
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["MYSQL_Connection"]
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    original_url = db.Column(db.String(128))
    path = db.Column(db.String(128))
    timestamp = db.Column(db.String(128))


@app.route("/")
def index():
    return "FriendsChallenge!"

@app.route("/api/image",methods=["POST"])
def save_image():
    image_url = request.get_json().get("image")

    print("[+] downloading image")
    image_file = requests.get(image_url, stream=True)
    image_name = image_url.split("/")[-1]

    s3_client = boto3.client("s3")
    print("[+] saving image locally")
    with open(image_name,"wb") as f:
        image_file.raw.decode_content = True
        shutil.copyfileobj(image_file.raw, f)

    print("[+] Sending to s3")
    s3_client.upload_file(image_name,os.environ["S3_BUCKET"],image_name)

    os.remove(image_name)
    return jsonify({"message":"task completed!"}), 200 


@app.route("/api/image",methods=["GET"])
def get_images():

    return jsonify({"message":"task completed!"}), 200 


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")