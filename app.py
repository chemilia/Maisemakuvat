import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db
import photos

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    all_photos = photos.get_photos()
    return render_template("index.html",photos = all_photos)

@app.route("/find_photo")
def find_photo():
    query = request.args.get("query")
    print(query)
    if query:
        results = photos.find_photo(query)
    else:
        query = ""
        results = []
    return render_template("find_photo.html", query=query, results = results)

@app.route("/photo/<int:photo_id>")
def show_photo(photo_id):
    photo = photos.get_photo(photo_id)
    return render_template("show_photo.html", photo = photo)


@app.route("/new_photo")
def new_photo():
	return render_template("new_photo.html")

@app.route("/create_photo", methods=["POST"])
def create_photo():
    seasons = request.form["seasons"]
    era = request.form["era"]
    description = request.form["description"]
    #scenery = request.form["scenery"]
    user_id = session["user_id"]

    photos.add_photo(seasons,era, description, user_id)

    return redirect("/")

@app.route("/edit_photo/<int:photo_id>")
def edit_photo(photo_id):
    photo = photos.get_photo(photo_id)
    return render_template("edit_photo.html", photo = photo)

@app.route("/update_photo", methods=["POST"])
def update_photo():
    photo_id = request.form["photo_id"]
    seasons = request.form["seasons"]
    era = request.form["era"]
    description = request.form["description"]
    #scenery = request.form["scenery"]

    photos.update_photo(photo_id, seasons, era, description)
    return redirect("/photo/" + str(photo_id))

@app.route("/remove_photo/<int:photo_id>" , methods=["GET", "POST"])
def remove_photo(photo_id):
    if request.method =="GET":
        photo = photos.get_photo(photo_id)
        return render_template("remove_photo.html", photo = photo)

    if request.method == "POST":
        if "remove" in request.form:
            photos.remove_photo(photo_id)
            return redirect("/")
        else:
            return redirect("/photo/" + str(photo_id))


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":    
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result ["id"]
        password_hash = result["password_hash"]

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")