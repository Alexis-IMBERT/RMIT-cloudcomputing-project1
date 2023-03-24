from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route('/')
@app.route('/index/')
def index():
    return "Hello world !"

@app.route('/login')
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