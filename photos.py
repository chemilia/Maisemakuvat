import db

def add_photo(seasons, era, description, scenery, user_id, mime_type):
    sql = "INSERT INTO photos (seasons, era, description, scenery, user_id, mime_type) VALUES (?, ?, ?, ?, ?, ?)"
    db.execute(sql, [seasons, era, description, scenery, user_id, mime_type])

def get_photos():
    sql = "SELECT id, description FROM photos ORDER BY id DESC"
    return db.query(sql)

def get_photo(photo_id):
    sql = """SELECT photos.id,
                    photos.seasons,
                    photos.era,
                    photos.description,
                    photos.scenery,
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

def find_photo(query):
    sql = """SELECT id, description
                FROM photos
                WHERE description LIKE ?
                ORDER BY id DESC"""
    return db.query(sql, ["%" + query + "%"])

def get_image(photo_id):
    sql = "SELECT scenery, mime_type FROM photos WHERE id = ?"

    return db.query(sql, [photo_id])[0]