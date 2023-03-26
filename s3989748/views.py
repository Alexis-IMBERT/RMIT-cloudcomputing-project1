import boto3
from flask import Flask, render_template, redirect, request

from .aws import DB_LOGIN
from .aws.LoginTable import create_login_table
from .aws.LoginTable import fill_login_table
from .aws.MusicTable import creation_music_table
from .aws.MusicTable import fill_music_table
from .aws.MusicImageS3 import creation_bucket
from .aws.MusicImageS3 import fill_bucket

app = Flask(__name__)


IS_CONNECTED = False


@app.route('/')
@app.route('/index/')
@app.route('/home')
def index():
    return render_template("index.html", is_connected=IS_CONNECTED)


@app.route('/login', methods=['POST'])
def login_post():
    # Create the client for the dynamoDB table login
    dynamodb = boto3.resource('dynamodb')

    # get the Login table
    table_login = dynamodb.Table(DB_LOGIN)

    # Get the information from the POST
    email = request.form['email']
    password = request.form['password']

    # # Process the information
    # print("-----------------------")
    # print(f"l'email est : {email} et le mot de passe est : {password}")
    # print("-----------------------")

    # Check the DB
    response = table_login.get_item(Key={"email": email})
    try:
        item = response["Item"]
    except KeyError:
        return render_template("login.html",creadential_not_valid=True, is_connected=IS_CONNECTED)
    
    # get the real password
    real_password = item["password"]

    if password != real_password:
        return render_template("login.html",creadential_not_valid=True, is_connected=IS_CONNECTED)

    return redirect("/home")


@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html', is_connected=IS_CONNECTED)


@app.route("/register", methods=["POST"])
def register_post():
    # Get the information from the POST methods
    email = request.form["email"]
    password = request.form['password']
    password_confrimation = request.form["password-confimed"]
    user_name = request.form["username"]

    print("-----------------------")
    print(f"\nl'email est : {email}, l'user name est : {user_name}, le mot de passe est : {password} et la confirmation est : {password_confrimation}\n")
    print("-----------------------")

    if password != password_confrimation:
        return render_template('register.html', is_connected=IS_CONNECTED, notvalidpassword=True)

    return render_template('register.html', is_connected=IS_CONNECTED, notvalidpassword=False)


@app.route('/register', methods=['GET'])
def register_get():
    return render_template('register.html', is_connected=IS_CONNECTED)


@app.route("/login/createtable")
def login_create_table():
    create_login_table()
    return "login table created"


@app.route("/login/filltable")
def login_fill_table():
    fill_login_table()
    return "login table is now fill"


@app.route("/music/createtable")
def music_create_table():
    creation_music_table()
    return "music table has been created"


@app.route("/music/filltable")
def music_fill_table():
    fill_music_table()
    return "Music table has been filled"


@app.route("/music/createbucket")
def music_create_bucket():
    creation_bucket()
    return "The bucket has been created"


@app.route("/music/fillbucket")
def music_fill_bucket():
    fill_bucket()
    return "The bucket has been filled"


app.config.from_object('config')

# if __name__ == "__main__":
#     app.run()
