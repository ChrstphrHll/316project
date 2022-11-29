from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login
from .game import Game

class User(UserMixin):
    def __init__(self, uid, name, email, about, image_url):
        self.uid = uid
        self.name = name
        self.email = email
        self.about = about
        self.image_url = image_url

    def get_id(self):   # override mixin default of reading "id" field because we call it uid
        return self.uid

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, uid, name, email, about, image_url
FROM Users
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(name, email, password):
        try:
            rows = app.db.execute("""
INSERT INTO Users(name, email, password)
VALUES(:name, :email, :password)
RETURNING uid
""",
                                  name=name,
                                  email=email,
                                  password=generate_password_hash(password))
            uid = rows[0][0]
            return User.get(uid)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    @login.user_loader
    def get(uid):
        rows = app.db.execute("""
SELECT uid, name, email, about, image_url
FROM Users
WHERE uid = :uid
""",
                              uid=uid)
        return User(*(rows[0])) if rows else None
    
    @staticmethod
    def get_liked_games(uid):
        rows = app.db.execute("""
SELECT Games.*
FROM Games, LikesGame
WHERE uid = :uid AND LikesGame.gid = Games.gid
""",
                            uid=uid)
        return [Game(*row) for row in rows]

    @staticmethod
    def get_play_count(uid, gid):
        rows = app.db.execute("""
SELECT PlayCount.count
FROM PlayCount
Where uid = :uid AND gid = :gid
        """, uid=uid, gid=gid)
        if len(rows) != 1:
            return None
        return rows[0][0]

    def increment_play_count(uid, gid):
        updated = app.db.execute("""
UPDATE PlayCount
SET count = count + 1
WHERE gid = :gid AND uid = :uid
        """, uid=uid, gid=gid)
        print(updated)

        if updated == 0:
            app.db.execute("""
INSERT INTO PlayCount (gid, uid, count)
VALUES (:gid, :uid, 1)
""", gid=gid, uid=uid)
