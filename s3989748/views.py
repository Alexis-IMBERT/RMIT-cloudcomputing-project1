import boto3
from flask import Flask, render_template, redirect, request, session
# from .aws.MusicImageS3 import get_s3_object

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
from .aws import DB_MUSIC
from .aws import REGION

app = Flask(__name__)


def is_connected():
    """
    test if you are connected or not 
    :return: True if you are connected
    """
    print("In is_connected()")

    # Check the session
    loggedin = session.get("loggedin")
    print(f"connected ? {loggedin}")

    # Test if you are already connected
    if (loggedin):
        return True
    return False


@app.route('/')
@app.route('/index/')
@app.route('/home')
def index():
    """ Route index """
    if is_connected():
        user_name = session.get("user_name")
        return render_template("index.html", is_connected=True, user_name=user_name)
    return render_template("index.html", is_connected=is_connected())


@app.route("/logout")
def logout():
    """ route logout """
    if (is_connected()):
        session.pop("loggedin", None)
        session.pop("email", None)
        session.pop("user_name", None)
    return redirect("/login")

################# LOGIN #################


@app.route('/login', methods=['POST'])
def login_post():
    """ Route login for the method post """
    # Check of connection
    if is_connected():
        return redirect("/home")

    # Create the client for the dynamoDB table login
    dynamodb = boto3.resource('dynamodb', region_name=REGION)

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

    # Session management
    session["email"] = email
    session["user_name"] = user_name
    session["loggedin"] = True

    return redirect("/home")


@app.route('/login', methods=['GET'])
def login_get():
    """ Route login for the method get """
    if is_connected():
        return redirect("/home")

    return render_template('login.html')

################# REGISTER #################


@app.route("/register", methods=["POST"])
def register_post():
    """ Route register for the method post """
    # Check of connection
    if is_connected():
        return redirect("/home")

    # Get the information from the POST methods
    email = request.form["email"]
    password = request.form['password']
    password_confrimation = request.form["password-confimed"]
    user_name = request.form["username"]

    # Create the client for the dynamoDB table login
    dynamodb = boto3.resource('dynamodb', region_name=REGION)

    # get the Login table
    table_login = dynamodb.Table(DB_LOGIN)

    # print("-----------------------")
    # print(f"\nl'email est : {email}, l'user name est :\
    # {user_name}, le mot de passe est : {password} \
    # et la confirmation est : {password_confrimation}\n")
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
    """ Route register for the method GET  """
    # Check of connection
    if is_connected():
        return redirect("/home")

    return render_template('register.html')


################# QUERY #################
@app.route('/query-music', methods=['POST'])
def query_music():
    """ Route for search the music in the DB """
    # Check of connection
    print("check if connected")
    if (not (is_connected())):
        print("not connected")
        return redirect("/home")
    print("connected")

    # post variable :
    print("get the variable in the post")
    title = request.form["title"]
    year = request.form["year"]
    artist = request.form["artist"]
    print(
        f"the variable are :\n\t - title : {title},\n\t - artist : {artist},\n\t - year : {year}")

    # Creation of the client
    dynamodb = boto3.client('dynamodb', region_name=REGION)

    # Define the table name
    table_name = DB_MUSIC

    scan_params = {
        'TableName': table_name,
        'FilterExpression': '',
        'ExpressionAttributeNames': {},
        'ExpressionAttributeValues': {}
    }

    # Create the scan parameters in function of the result
    if title != "":
        # titre present
        scan_params["FilterExpression"] += '#title = :title'
        scan_params["ExpressionAttributeNames"]['#title'] = 'title'
        scan_params["ExpressionAttributeValues"][":title"] = {'S': title}

    if artist != "":
        #  artist present
        # test if there is already something in the string
        if scan_params["FilterExpression"] != '':
            scan_params["FilterExpression"] += ' and '

        scan_params["FilterExpression"] += '#artist = :artist'
        scan_params["ExpressionAttributeNames"]['#artist'] = 'artist'
        scan_params["ExpressionAttributeValues"][":artist"] = {'S': artist}

    if year != "":
        # artist present
        # test if there is already something in the string
        if scan_params["FilterExpression"] != '':
            scan_params["FilterExpression"] += ' and '

        scan_params["FilterExpression"] += '#year = :year'
        scan_params["ExpressionAttributeNames"]['#year'] = 'year'
        scan_params["ExpressionAttributeValues"][":year"] = {'S': year}

    # Perform the scan
    response = dynamodb.scan(**scan_params)

    # Print the results
    print("\n -----------------------")
    print("result of the query")
    items = response['Items']
    result = []
    for item in items:
        # Extraction of variable :
        result_title = item["title"]['S']
        result_year = item["year"]['S']
        result_artist = item["artist"]['S']
        result_web_url = item["web_url"]['S']
        result_image_url = item["image_url"]['S']
        result.append({
            "title": result_title,
            "year": result_year,
            "artist": result_artist,
            "image_url": result_image_url,
            "web_url": result_web_url
        })
        print(
            f'Titre : {result_title},\t\t\t\t Year : {result_year}, \t\t\t\t Artist : {result_artist}')
    print("\n -----------------------")
    return str(result)


###### TEST #######


@app.route("/test")
def test():
    # s3_image = get_s3_object()
    return render_template("index.html", image="test")
################# ACTION ON TABLE AND BUCKET #################


@app.route("/login/createtable")
def login_create_table():
    """ Route to create the table login """
    create_login_table()
    return "login table created"


@app.route("/login/filltable")
def login_fill_table():
    """ route to fill the table login """
    fill_login_table()
    return "login table is now fill"


@app.route("/music/createtable")
def music_create_table():
    """ Route to create the table music """
    creation_music_table()
    return "music table has been created"


@app.route("/music/filltable")
def music_fill_table():
    """ Route to fill the table music """
    fill_music_table()
    return "Music table has been filled"


@app.route("/music/createbucket")
def music_create_bucket():
    """ Route to create the bucket s3  """
    result = creation_bucket()
    return f"The bucket has been created : {result} "


@app.route("/music/fillbucket")
def music_fill_bucket():
    """ Route to fill the bucket s3 with images of music """
    fill_bucket()
    return "The bucket has been filled"


@app.route("/clean/table/login")
def cleaning_login_table():
    """ Route to clean the login table """
    cleaning_db_login()
    return "Login DB has been deleted"


@app.route("/clean/table/music")
def cleaning_music_table():
    """ route to cean music table """
    cleaning_db_music()
    return "Music DB has been deleted"


@app.route("/clean/bucket")
def cleaning_bucket():
    """ Route to clean the bucket """
    cleaning_bucket_music()
    return "Bucket has been deleted"


@app.route("/clean/all")
def cleaning_all():
    """ Route to clean all """
    cleaning_db_login()
    cleaning_db_music()
    cleaning_bucket_music()
    return "DB login and music has been deleted <br/> Bucket has been deleted"


@app.route("/create/all")
def create_all():
    """ Route to create and fill all the table and bucket """
    create_login_table()
    fill_login_table()
    creation_music_table()
    fill_music_table()
    creation_bucket()
    fill_bucket()
    return "everything has been created and fill !"


app.config.from_object('config')
