from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = Flask(__name__)
db = SQLAlchemy(app)
app.confg["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tushar_database.db"
app.config["SECRET_KEY"] = "tusharsecretkey"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")


if __name__=='__main__':
    app.run(debug=True)