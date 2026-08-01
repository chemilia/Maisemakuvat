import db

def add_photo(seasons, era, description, user_id):
    sql = "INSERT INTO photos (seasons, era, description,user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [seasons, era, description, user_id])

def get_photos():
    sql = "SELECT id, description FROM photos ORDER BY id DESC"
    return db.query(sql)

def get_photo(photo_id):
    sql = """SELECT photos.id,
                    photos.seasons,
                    photos.era,
                    photos.description,
                    users.id user_id,
                    users.username
                FROM users, photos
                WHERE photos.user_id = users.id AND photos.id = ?"""
    return db.query(sql, [photo_id])[0]

def update_photo(photo_id, seasons,era, description):
    sql = """UPDATE photos SET seasons = ?,
                                era = ?,
                                description = ?
                            WHERE id = ?"""

    db.execute(sql, [seasons, era, description, photo_id])

def remove_photo(photo_id):
    sql = "DELETE FROM photos WHERE id = ?"
    db.execute(sql, [photo_id])