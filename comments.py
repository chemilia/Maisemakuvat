import db

def add_comment(content, photo_id, user_id):
    sql = """INSERT INTO comments
             (content, photo_id, user_id)
             VALUES (?, ?, ?)"""

    db.execute(sql, [content, photo_id, user_id])

def get_comments(photo_id):
    sql = """SELECT comments.id,
                    comments.content,
                    comments.photo_id,
                    comments.user_id,
                    users.username

             FROM comments
             JOIN users ON comments.user_id = users.id
             WHERE comments.photo_id = ?
             ORDER BY comments.id DESC"""

    return db.query(sql, [photo_id])