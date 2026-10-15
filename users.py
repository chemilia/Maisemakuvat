import db
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash


def get_user(user_id):
    sql = """SELECT id, username FROM users WHERE id = ?"""
    result= db.query(sql, [user_id])
    return result[0] if result else None

def get_photos(user_id):
    sql = """SELECT id, 
                    description,
                    (SELECT COUNT(*)FROM likes WHERE likes.photo_id == photos.id) AS like_count 
                FROM photos WHERE user_id = ? ORDER BY id DESC"""
    return db.query(sql, [user_id])

def create_user(username,password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    
    if not result:
        flash("VIRHE: Käyttäjätunnusta ei löydy.")
        return None
    
    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]

    if check_password_hash(password_hash, password):
        return user_id
    else:
        flash("VIRHE: Käyttäjätunnus tai salasana on väärin.")
        return None
    