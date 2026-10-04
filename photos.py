import db

def add_photo(seasons, era, description, scenery, user_id, mime_type, landscape_type_id):
    sql = "INSERT INTO photos (seasons, era, description, scenery, user_id, mime_type, landscape_type_id) VALUES (?, ?, ?, ?, ?, ?, ?)"
    db.execute(sql, [seasons, era, description, scenery, user_id, mime_type, landscape_type_id])

def get_photos():
    sql = "SELECT id, description FROM photos ORDER BY id DESC"
    return db.query(sql)

def get_photo(photo_id):
    sql = """SELECT photos.id,
                    photos.seasons,
                    photos.era,
                    photos.description,
                    photos.scenery,
                    photos.landscape_type_id,
                    landscape_types.name landscape_type,
                    users.id user_id,
                    users.username

                FROM photos
                JOIN users ON photos.user_id = users.id
                LEFT JOIN landscape_types ON photos.landscape_type_id = landscape_types.id
                WHERE  photos.id = ?"""
    result= db.query(sql, [photo_id])
    return result[0] if result else None

def update_photo(photo_id, seasons,era, description, landscape_type_id):
    sql = """UPDATE photos SET seasons = ?,
                                era = ?,
                                description = ?,
                                landscape_type_id =?
                            WHERE id = ?"""

    db.execute(sql, [seasons, era, description, landscape_type_id, photo_id])

def remove_photo(photo_id):
    sql = "DELETE FROM photos WHERE id = ?"
    db.execute(sql, [photo_id])

def find_photo(query, seasons, era, landscape_type):
    sql = """SELECT photos.id, photos.description
         FROM photos
         LEFT JOIN landscape_types
         ON photos.landscape_type_id = landscape_types.id"""

    conditions = []
    params = []

    if query:
        conditions.append("photos.description LIKE ?")
        params.append("%" + query + "%")

    if seasons:
        conditions.append("photos.seasons = ?")
        params.append(seasons)

    if era:
        conditions.append("photos.era = ?")
        params.append(era)

    if landscape_type:
        conditions.append("photos.landscape_type_id = landscape_types.id")
        conditions.append("landscape_types.name = ?")
        params.append(landscape_type)

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    sql += " ORDER BY photos.id DESC"

    return db.query(sql, params)

def get_image(photo_id):
    sql = "SELECT scenery, mime_type FROM photos WHERE id = ?"

    return db.query(sql, [photo_id])[0]