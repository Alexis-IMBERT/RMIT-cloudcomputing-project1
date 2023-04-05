import base64
from io import BytesIO
import boto3
from flask import Flask, render_template
from PIL import Image
import matplotlib.pyplot as plt
import base64

from flask import Flask, render_template, redirect, request, session, url_for
# from .aws.MusicImageS3 import get_s3_object

from .aws import DB_LOGIN
from .aws.LoginTable import create_login_table
from .aws.LoginTable import fill_login_table
from .aws.MusicTable import creation_music_table
from .aws.MusicTable import fill_music_table
from .aws.MusicImageS3 import creation_bucket
from .aws.MusicImageS3 import fill_bucket
from .aws.MusicImageS3 import get_s3_object
from .aws.cleaning import cleaning_db_login
from .aws.cleaning import cleaning_db_music
from .aws.cleaning import cleaning_bucket_music
from .aws import DB_MUSIC
from .aws import REGION
from .aws import KEY_ID
from .aws import ACCESS_KEY
from .aws import TOKEN
from .aws.LoginTable import add_to_subscription_list
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
    return bool(loggedin)


# Register custom Jinja2 filter
@app.template_filter('b64encode')
def b64encode_filter(s):
    return base64.b64encode(s.encode('utf-8')).decode('utf-8')


@app.route('/')
@app.route('/index/')
@app.route('/home')
def index():
    """ Route index """
    print("In the route index/home/ /")
    if is_connected():
        user_name = session.get("user_name")
        return render_template("index.html", is_connected=True, user_name=user_name)
    return render_template("index.html", is_connected=is_connected())


@app.route("/logout")
def logout():
    """ route logout """
    print("in route logout")
    if (is_connected()):
        session.pop("loggedin", None)
        session.pop("email", None)
        session.pop("user_name", None)
    print("I will leave logout route and redirect to login")
    return redirect("/login")

################# LOGIN #################


@app.route('/login', methods=['POST'])
def login_post():
    """ Route login for the method post """
    print("In route Login with method post")
    # Check of connection
    if is_connected():
        return redirect("/home")

    # Create the client for the dynamoDB table login
    dynamodb = boto3.resource('dynamodb', region_name=REGION,
                              aws_access_key_id=KEY_ID,
                              aws_secret_access_key=ACCESS_KEY,
                              aws_session_token=TOKEN)

    # get the Login table
    table_login = dynamodb.Table(DB_LOGIN)

    # Get the information from the POST
    email = request.form['email']
    password = request.form['password']

    # Process the information
    print("-----------------------")
    print(f"Email is : {email} \t\t password is : {password}")
    print("-----------------------")

    # Check the DB
    response = table_login.get_item(Key={"email": email})
    print("In the loggin with method post, and will try the email in the DB")
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
    print("In login route with post method, creation of session variable")
    session["email"] = email
    session["user_name"] = user_name
    session["loggedin"] = True

    print("Will leave the login route with the post methods")
    return redirect("/home")


@app.route('/login', methods=['GET'])
def login_get():
    """ Route login for the method get """
    print("In the loggin route with get method")
    if is_connected():
        print("user is connected so redirection to home page")
        return redirect("/home")
    print("render the login page")
    return render_template('login.html')

################# REGISTER #################


@app.route("/register", methods=["POST"])
def register_post():
    """ Route register for the method post """
    print("in the register route with the method POST")
    # Check of connection
    if is_connected():
        print("User already connected so redirection to home page")
        return redirect("/home")

    # Get the information from the POST methods
    email = request.form["email"]
    password = request.form['password']
    password_confrimation = request.form["password-confimed"]
    user_name = request.form["username"]

    # Create the client for the dynamoDB table login
    dynamodb = boto3.resource('dynamodb', region_name=REGION,
                              aws_access_key_id=KEY_ID,
                              aws_secret_access_key=ACCESS_KEY,
                              aws_session_token=TOKEN)

    # get the Login table
    table_login = dynamodb.Table(DB_LOGIN)

    print("-----------------------")
    print(f"\n Email is : {email}, user name is :\
    {user_name}, password is : {password} \
    confirmation of password is : {password_confrimation}\n")
    print("-----------------------")

    if password != password_confrimation:
        return render_template('register.html',
                               notvalidpassword=True)

    # Check the DB
    response = table_login.get_item(Key={"email": email})

    if "Item" in response:
        print("email already in the database")
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
    print("In the register route with the method get")
    # Check of connection
    if is_connected():
        print("User already connected so redirection to home page")
        return redirect("/home")

    print("Render the register page ")
    return render_template('register.html')


################# QUERY #################
@app.route('/query-music', methods=['POST'])
def query_music():
    """ Route for search the music in the DB """
    print("In the route for querry method post")
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
    dynamodb = boto3.client('dynamodb', region_name=REGION,
                            aws_access_key_id=KEY_ID,
                            aws_secret_access_key=ACCESS_KEY,
                            aws_session_token=TOKEN)

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

        key = f'{result_title}-{result_artist}-{result_year}.jpg'

        image_data = get_s3_object(key)
        image = f'data:image/jpg;base64,{image_data.hex()}'
        # save the image data to a file for debugging
        with open(f's3989748/static/{key}', 'wb') as f:
            f.write(image_data)

        result.append({
            "title": result_title,
            "year": result_year,
            "artist": result_artist,
            "image": key
        })
        print(
            f'Titre : {result_title},\t\t\t\t Year : {result_year}, \t\t\t\t Artist : {result_artist}')
    print("\n -----------------------")
    return render_template("index.html", is_connected=is_connected(), liste_query=result)


########### SUBSCRIPTION ROUTE #############
@app.route("/subscribe")
def subscribe():
    """ Route for new subscription """
    print("in the route to subscribe to a new artist")

    if not (is_connected()):
        print("user not connected and attempt to subscribe")
        return redirect('/login')

    # Get the title, artist and year from the get method
    title = request.args.get("title")
    artist = request.args.get("artist")
    year = request.args.get("year")

    # Get the user information from the session
    email = session.get("email")

    new_song = {'title': title, 'artist': artist, 'year': year}

    # Add the music to the table to the subscription list of the user
    add_to_subscription_list(email, new_song)

    return f"{title}, {artist}, {year}"


########### REMOVE FROM SUBSCRIPTION ############
@app.route("/remove")
def remove():
    """ Route for remove the subscription """
    print("In the route for remove a music from the subscription")

    if not (is_connected()):
        print("user not connected and attempt to remove a song from his subscription list")
        return redirect('/login')

    # Get the information of the song
    title = request.args.get("title")
    artist = request.args.get("artist")
    year = request.args.get("year")

    # Get the information of the user
    email = session.get("email")
    user_name = session.get("user_name")

    # Creation of the client for the dynamoDB resources
    dynamodb = boto3.resource('dynamodb', region_name=REGION,
                              aws_access_key_id=KEY_ID,
                              aws_secret_access_key=ACCESS_KEY,
                              aws_session_token=TOKEN)

    # get the Login table
    table_login = dynamodb.Table(DB_LOGIN)

    # Remove the music from the subscription list of the user

    return f"{title}, {artist}, {year}"

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
