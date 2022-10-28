from flask import current_app as app
from app.models.game import Game
from app.models.user import User

class Copy:
    def __init__(self, cpid, comment):
        self.cpid = cpid
        self.comment = comment
        self.game = Copy.copy_of(cpid)
        self.borrower = Copy.checked_out_by(cpid)

    @staticmethod
    def copy_of(cpid):
      rows = app.db.execute('''
        SELECT Games.*
        FROM Games, CopyOf
        WHERE cpid=:cpid AND Games.gid=CopyOf.gid
        ''',
        cpid=cpid)
      return Game(*(rows[0])) if rows else None

    @staticmethod
    def user_borrowed_copies(uid):
      rows = app.db.execute('''
      SELECT Copies.*
      FROM CheckedOutBy, Copies
      WHERE uid=:uid AND Copies.cpid=CheckedOutBy.cpid
      ''',
      uid=uid)
      return [Copy(*row) for row in rows]

    @staticmethod
    def checked_out_by(cpid):
      rows = app.db.execute('''
        SELECT Users.uid, name, email, about, image_url
        FROM Users, CheckedOutBy
        WHERE cpid=:cpid AND CheckedOutBy.uid=Users.uid
        ''',
        cpid=cpid)
      print(rows)
      return User(*(rows[0])) if rows else None
