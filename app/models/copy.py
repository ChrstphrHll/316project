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
    def create(gid, comment, lid, borrower_id):
      try:
        rows = app.db.execute("""
          INSERT INTO Copies(comment)
          VALUES(:comment)
          RETURNING cpid
          """,
          comment=comment,
        )
        
        cpid = rows[0][0]
        
        app.db.execute("""
          INSERT INTO CopyOf(cpid, gid)
          VALUES(:cpid, :gid)
          """,
          cpid=cpid,
          gid=gid,
        )

        app.db.execute("""
          INSERT INTO HasCopy(lid, cpid)
          VALUES(:lid, :cpid)
          """,
          lid=lid,
          cpid=cpid,
        )

        print(borrower_id)
        if borrower_id:
          app.db.execute("""
            INSERT INTO CheckedOutBy(cpid, uid)
            VALUES(:cpid, :uid)
            """,
            cpid=cpid,
            uid=borrower_id,
          )

        return Copy.get(cpid)
      except Exception as e:
        print(str(e))
        return None

    @staticmethod
    def get(cpid):
      rows = app.db.execute('''
        SELECT *
        FROM Copies
        WHERE cpid = :cpid
        ''',
        cpid=cpid)
      return Copy(*(rows[0])) if rows else None

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
    def checkout_copy(cpid, uid):
      try:
        app.db.execute("""
            INSERT INTO CheckedOutBy(cpid, uid)
            VALUES(:cpid, :uid)
            """,
            cpid=cpid,
            uid=uid
          )
        return True
      except Exception as e:
        print(str(e))
        return None

    def return_copy(cpid, uid):
      try:
        app.db.execute('''
          DELETE FROM CheckedOutBy
          WHERE cpid=:cpid AND uid=:uid
          ''',
          cpid=cpid,
          uid=uid)
        return True
      except Exception as e:
        print(str(e))
        return None

    @staticmethod
    def user_borrowed_copies(uid):
      rows = app.db.execute('''
      SELECT Copies.*
      FROM CheckedOutBy, Copies
      WHERE uid=:uid AND Copies.cpid=CheckedOutBy.cpid
      ''',
      uid=uid)
      return [Copy(*row) for row in rows]

    # Get all libraries owned by user
    # Get all copies in those libraries
    @staticmethod
    def user_owned_copies(uid):
      rows = app.db.execute('''
      SELECT Copies.*
      FROM Libraries, HasCopy, Owns, Copies
      WHERE Owns.uid=:uid AND Owns.lid = Libraries.lid AND HasCopy.lid = Libraries.lid AND Copies.cpid=HasCopy.cpid
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
      return User(*(rows[0])) if rows else None
