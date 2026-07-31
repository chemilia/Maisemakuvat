import db

def add_photo(seasons, era, description, scenery, user_id):
    sql = "INSERT INTO photos (seasons, era, description, scenery,user_id) VALUES (?, ?, ?, ?, ?)"
    db.execute(sql, [seasons, era, description,scenery, user_id])