import secrets
import sqlite3
from flask import Flask
from flask import redirect, render_template, flash, request, session, Response, abort
import config
import markupsafe
import db
import photos
import users
import comments
import likes

app = Flask(__name__)
app.secret_key = config.secret_key
app.jinja_env.globals["likes"] = likes

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in session:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

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

    results = photos.find_photo( query, seasons, era, landscape_type)
    return render_template( "find_photo.html", query=query, seasons=seasons, era=era, landscape_type=landscape_type, results=results, searched=True )

@app.route("/photo/<int:photo_id>")
def show_photo(photo_id):
    photo = photos.get_photo(photo_id)

    if not photo:
        flash("Kuva on poistettu pois, voit katso muita kuvia.")
        return redirect("/")

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
        flash("Käyttäjää ei löytynyt.")
        return redirect("/")
    photos = users.get_photos(user_id)
    return render_template("show_user.html", user = user, photos = photos)


@app.route("/new_photo")
def new_photo():
    require_login()
    return render_template("new_photo.html")

@app.route("/create_photo", methods=["POST"])
def create_photo():
    require_login()
    check_csrf()

    seasons = request.form["seasons"]
    era = request.form["era"]
    description = request.form["description"]
    landscape_type = request.form["landscape_type"]

    image = request.files["scenery"]
    if image.filename == "":
        flash("Et valinnut kuvaa")
        return redirect("/new_photo")
    if image.mimetype not in ["image/png", "image/jpeg"]:
        flash("VIRHE: kuvan pitää olla PNG- tai JPG-kuva")
        return redirect("/new_photo")

    scenery = image.read()
    if len(scenery) > 5* 1024 * 1024:
        flash("VIRHE: kuvan maksimikoko on 5 MB")
        return redirect("/new_photo")

        
    mime_type = image.mimetype

    user_id = session["user_id"]

    result = db.query(
        "SELECT id FROM landscape_types WHERE name = ?",
        [landscape_type]
    )
    landscape_type_id = result[0]["id"]

    photos.add_photo(seasons, era, description, scenery, user_id, mime_type, landscape_type_id)

    photo_id = db.last_insert_id()
    return redirect("/photo/" + str(photo_id))

@app.route("/edit_photo/<int:photo_id>")
def edit_photo(photo_id):
    require_login()

    photo = photos.get_photo(photo_id)
    if not photo:
            flash("Kuvaa ei löytynyt")
            return redirect("/")
    if photo["user_id"] != session["user_id"]:
        flash("Et voi muokata tämä kuvaa, koska et ole kuvan lähettäjä.")
        return redirect("/photo/" + str(photo_id))

    return render_template("edit_photo.html", photo = photo)

@app.route("/update_photo", methods=["POST"])
def update_photo():
    require_login()
    check_csrf()

    photo_id = request.form["photo_id"]
    photo = photos.get_photo(photo_id)
    if not photo:
        flash("Kuvaa ei löytynyt")
        return redirect("/")
    if photo["user_id"] != session["user_id"]:
        flash("Et voi muokata tämä kuvaa, koska et ole kuvan lähettäjä.")
        return redirect("/photo/" + str(photo_id))

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
        flash("Kuvaa ei löytynyt.")
        return redirect("/")

    if photo["user_id"] != session["user_id"]:
        flash("Et voi poistaa kuvan, koska et ole kuvan lähettäjä")
        return redirect("/photo/"+ str(photo_id))

    if request.method =="GET":
        return render_template("remove_photo.html", photo = photo)

    if request.method == "POST":
        check_csrf()

        if "remove" in request.form:
            photos.remove_photo(photo_id)
            return redirect("/")
        else:
            return redirect("/photo/" + str(photo_id))

@app.route("/add_comment", methods=["POST"])
def add_comment():
    require_login()
    check_csrf()

    photo_id = request.form["photo_id"]
    content = request.form["content"]

    comments.add_comment(
        content,
        photo_id,
        session["user_id"]
    )

    return redirect("/photo/" + str(photo_id))

@app.route("/like", methods=["POST"])
def like():
    require_login()
    check_csrf()

    photo_id = request.form["photo_id"]
    photo = photos.get_photo(photo_id)

    if not photo:
        flash("Kuvaa ei löytynyt.")
        return redirect("/")

    user_id = session["user_id"]

    if likes.has_liked(user_id, photo_id):
        likes.remove_like(user_id, photo_id)
    else:
        likes.add_like(user_id, photo_id)

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
        flash("VIRHE: Anna käyttäjätunnus.")
        return redirect("/register")
    if not password1:
        flash("VIRHE: Anna salasana.")
        return redirect("/register")
    if password1 != password2:
        flash("VIRHE: salasanat eivät täsmää.")
        return redirect("/register")
    
    try:
        users.create_user(username,password1)
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu")
        return redirect("/register")
    flash("Tunnus luotu, nyt voit kirjautua sisään.")
    return redirect("/")

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
            session["csrf_token"] = secrets.token_hex(16)
            flash("Olet kirjautunut onnistuneesti sisään.")
            return redirect("/")
        else:
            return redirect("/login")
        
@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")