import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, Response, abort
import config
import db
import photos
import users
import comments

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_photos = photos.get_photos()
    return render_template("index.html",photos = all_photos)

@app.route("/find_photo")
def find_photo():
    query = request.args.get("query")
    seasons = request.args.get("seasons", "") 
    era = request.args.get("era", "") 
    landscape_type = request.args.get("landscape_type", "")

    results = photos.find_photo( query, seasons, era, landscape_type ) 
    return render_template( "find_photo.html", query=query, seasons=seasons, era=era, landscape_type=landscape_type, results=results, searched=True )

@app.route("/photo/<int:photo_id>")
def show_photo(photo_id):
    photo = photos.get_photo(photo_id)
    if not photo:
            abort(404)

    comments_list = comments.get_comments(photo_id)

    return render_template("show_photo.html", photo = photo, comments = comments_list)

@app.route("/image/<int:photo_id>")
def image(photo_id):
    image = photos.get_image(photo_id)
    return Response(image["scenery"], mimetype=image["mime_type"])

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
            abort(404)
    photos = users.get_photos(user_id)
    return render_template("show_user.html", user = user, photos = photos)


@app.route("/new_photo")
def new_photo():
    require_login()
    return render_template("new_photo.html")

@app.route("/create_photo", methods=["POST"])
def create_photo():
    require_login()

    seasons = request.form["seasons"]
    era = request.form["era"]
    description = request.form["description"]
    landscape_type = request.form["landscape_type"]

    image = request.files["scenery"]
    if image.filename == "":
        return "Et valinnut kuvaa"
    if image.mimetype not in ["image/png", "image/jpeg"]:
        return render_template("new_photo.html",error="VIRHE: kuvan pitää olla PNG- tai JPG-kuva")
    scenery = image.read()
    if len(scenery) > 5* 1024 * 1024:
        return render_template("new_photo.html",error="VIRHE: kuvan maksimikoko on 5 MB")
        
    mime_type = image.mimetype

    user_id = session["user_id"]

    result = db.query(
        "SELECT id FROM landscape_types WHERE name = ?",
        [landscape_type]
    )
    landscape_type_id = result[0]["id"]

    photos.add_photo(seasons, era, description, scenery, user_id, mime_type, landscape_type_id)

    return redirect("/")

@app.route("/edit_photo/<int:photo_id>")
def edit_photo(photo_id):
    require_login()

    photo = photos.get_photo(photo_id)
    if not photo:
            abort(404)
    if photo["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_photo.html", photo = photo)

@app.route("/update_photo", methods=["POST"])
def update_photo():
    require_login()

    photo_id = request.form["photo_id"]
    photo = photos.get_photo(photo_id)
    if not photo:
            abort(404)
    if photo["user_id"] != session["user_id"]:
        abort(403)

    seasons = request.form["seasons"]
    era = request.form["era"]
    description = request.form["description"]
    landscape_type = request.form["landscape_type"]

    #scenery = request.files["scenery"].read()

    result = db.query(
            "SELECT id FROM landscape_types WHERE name = ?",
            [landscape_type]
        )
    landscape_type_id = result[0]["id"]

    photos.update_photo(photo_id, seasons, era, description, landscape_type_id)
    return redirect("/photo/" + str(photo_id))

@app.route("/remove_photo/<int:photo_id>" , methods=["GET", "POST"])
def remove_photo(photo_id):
    require_login()

    photo = photos.get_photo(photo_id)
    if not photo:
            abort(404)
    if photo["user_id"] != session["user_id"]:
        abort(403)

    if request.method =="GET":
        return render_template("remove_photo.html", photo = photo)

    if request.method == "POST":
        if "remove" in request.form:
            photos.remove_photo(photo_id)
            return redirect("/")
        else:
            return redirect("/photo/" + str(photo_id))

@app.route("/add_comment", methods=["POST"])
def add_comment():

    require_login()

    photo_id = request.form["photo_id"]
    content = request.form["content"]

    comments.add_comment(
        content,
        photo_id,
        session["user_id"]
    )

    return redirect("/photo/" + str(photo_id))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if not username:
        return render_template("register.html",error="VIRHE: Anna käyttäjätunnus.")
    if not password1:
        return render_template("register.html",error="VIRHE: Anna salasana.")
    
    if password1 != password2:
        return render_template("register.html",error="VIRHE: salasanat eivät täsmää.")
    
    try:
        users.create_user(username,password1)
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

        user_id = users.check_login(username, password)

        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        
@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")