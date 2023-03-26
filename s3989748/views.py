from flask import Flask, render_template, redirect

app = Flask(__name__)


@app.route('/')
@app.route('/index/')
def index():
    return "Hello world !"


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    # Perform authentication logic with email and password here
    # ...
    # Return response to the client
    return 'Login successful'


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html', is_connected=False)


@app.route('/register')
def register():
    return render_template('register.html', is_connected=False)


@app.route('/home')
def home():
    return redirect('/')


app.config.from_object('config')

# if __name__ == "__main__":
#     app.run()
