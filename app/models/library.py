from flask import current_app as app

from app.models.copy import Copy
from app.models.user import User

class Library:
    def __init__(self, lid, title, description):
        self.lid = lid
        self.title = title
        self.description = description
        self.owner = Library.get_owner(lid)

    @staticmethod
    def get(lid):
      rows = app.db.execute('''
        SELECT *
        FROM Libraries
        WHERE lid = :lid
        ''',
        lid=lid)
      return Library(*(rows[0])) if rows else None

    @staticmethod
    def get_all():
      rows = app.db.execute('''
        SELECT *
        FROM Libraries
        ''',
        )
      return [Library(*row) for row in rows]

    @staticmethod
    def get_user_libraries(uid):
      rows = app.db.execute('''
        SELECT Libraries.*
        FROM Owns, Libraries
        WHERE uid=:uid AND Owns.lid=Libraries.lid
        ''',
        uid=uid)
      return [Library(*row) for row in rows]

    @staticmethod
    def get_owner(lid):
      rows = app.db.execute('''
        SELECT Users.uid, name, email, about, image_url
        FROM Users, Owns
        WHERE lid=:lid AND Owns.uid=Users.uid
        ''',
        lid=lid)
      return User(*(rows[0])) if rows else None

    @staticmethod
    def get_copies(lid):
      rows = app.db.execute('''
        SELECT Copies.*
        FROM HasCopy, Copies
        WHERE HasCopy.lid=:lid AND HasCopy.cpid=Copies.cpid
        ''',
        lid=lid
        )
      return [Copy(*row) for row in rows]
