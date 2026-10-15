import db

def add_like(user_id, photo_id):
    sql = """INSERT INTO likes(user_id, photo_id) VALUES (?,?)"""
    db.execute(sql,[user_id, photo_id])

def remove_like(user_id, photo_id):
    sql = """DELETE FROM likes WHERE user_id = ? AND photo_id = ?"""
    db.execute(sql, [user_id, photo_id])

def has_liked(user_id, photo_id):
    sql = """SELECT id FROM likes WHERE user_id = ? AND photo_id = ?"""
    result = db.query(sql, [user_id, photo_id])
    return bool(result)

def count_likes(photo_id):
    sql = """  SELECT COUNT(*) AS count FROM likes WHERE photo_id = ?"""
    result = db.query(sql, [photo_id])
    return result[0]["count"]