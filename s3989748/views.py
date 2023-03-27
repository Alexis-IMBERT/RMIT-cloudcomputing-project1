import boto3
from flask import Flask, render_template, redirect, request, make_response

from .aws import DB_LOGIN
from .aws.LoginTable import create_login_table
from .aws.LoginTable import fill_login_table
from .aws.MusicTable import creation_music_table
from .aws.MusicTable import fill_music_table
from .aws.MusicImageS3 import creation_bucket
from .aws.MusicImageS3 import fill_bucket
from .aws.cleaning import cleaning_db_login
from .aws.cleaning import cleaning_db_music
from .aws.cleaning import cleaning_bucket_music

app = Flask(__name__)


IS_CONNECTED = False


def is_connected(request):
    """
    test if you are connected or not 
    :param request: the request receive
    :return: True if you are connected
    """
    # Check the cookies
    email = request.cookies.get("email")
    user_name = request.cookies.get("user_name")
    # Test if you are already connected
    if (email != None) & (user_name != None):
        return True
    return False


@app.route('/')
@app.route('/index/')
@app.route('/home')
def index():
    if is_connected(request):
        user_name = request.cookies.get("user_name")
        return render_template("index.html",is_connected=True,user_name=user_name)
    return render_template("index.html",is_connected=is_connected(request=request))

@app.route("/logout")
def logout():
    response = make_response(redirect("/login"))
    response.delete_cookie('email')
    response.delete_cookie('user_name')
    return response
    
@app.route('/login', methods=['POST'])
def login_post():
    # Check of connection
    if (is_connected(request)):
        return redirect("/home")

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
        return render_template("login.html",
                               creadential_not_valid=True)

    # get the real password
    real_password = item["password"]
    user_name = item["user_name"]

    if password != real_password:
        return render_template("login.html",
                               creadential_not_valid=True)

    # Cookie assurant la connexion
    response = make_response(redirect("/home"))
    response.set_cookie('email', email)
    response.set_cookie('user_name', user_name)

    return response


@app.route('/login', methods=['GET'])
def login_get():
    if (is_connected(request)):
        return redirect("/home")

    return render_template('login.html')


@app.route("/register", methods=["POST"])
def register_post():
    # Check of connection
    if (is_connected(request)):
        return redirect("/home")

    # Get the information from the POST methods
    email = request.form["email"]
    password = request.form['password']
    password_confrimation = request.form["password-confimed"]
    user_name = request.form["username"]

    # Create the client for the dynamoDB table login
    dynamodb = boto3.resource('dynamodb')

    # get the Login table
    table_login = dynamodb.Table(DB_LOGIN)

    # print("-----------------------")
    # print(f"\nl'email est : {email}, l'user name est : {user_name}, le mot de passe est : {password} et la confirmation est : {password_confrimation}\n")
    # print("-----------------------")

    if password != password_confrimation:
        return render_template('register.html',
                               notvalidpassword=True)

    # Check the DB
    response = table_login.get_item(Key={"email": email})

    if "Item" in response:
        return render_template("register.html",
                               email_already_exist=True)

    value = {
        "email": email,
        "user_name": user_name,
        "password": password
    }

    # sending to the DynamoDB
    table_login.put_item(Item=value)

    return redirect('/login')


@app.route('/register', methods=['GET'])
def register_get():
    # Check of connection
    if (is_connected(request)):
        return redirect("/home")

    return render_template('register.html')


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
    result = creation_bucket()
    return f"The bucket has been created : {result} "


@app.route("/music/fillbucket")
def music_fill_bucket():
    fill_bucket()
    return "The bucket has been filled"


@app.route("/clean/table/login")
def cleaning_login_table():
    cleaning_db_login()
    return "Login DB has been deleted"


@app.route("/clean/table/music")
def cleaning_music_table():
    cleaning_db_music()
    return "Music DB has been deleted"


@app.route("/clean/bucket")
def cleaning_bucket():
    cleaning_bucket_music()
    return "Bucket has been deleted"


@app.route("/clean/all")
def cleaning_all():
    cleaning_db_login()
    cleaning_db_music()
    cleaning_bucket_music()
    return "DB login and music has been deleted <br/> Bucket has been deleted"


app.config.from_object('config')

# if __name__ == "__main__":
#     app.run()
