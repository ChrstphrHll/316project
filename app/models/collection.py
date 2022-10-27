from flask import current_app as app
from app.models.game import Game

class Collection:
    def __init__(self, cid, title, description):
        self.cid = cid
        self.title = title
        self.description = description

    @staticmethod
    def get(cid):
      rows = app.db.execute('''
        SELECT *
        FROM Collections
        WHERE cid = :cid
        ''',
        cid=cid)
      return Collection(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all():
      rows = app.db.execute('''
        SELECT *
        FROM Collections
        ''',
        )
      return [Collection(*row) for row in rows]

    @staticmethod
    def get_user_collections(uid):
      print("got here" + uid)
      rows = app.db.execute('''
        SELECT Collections.*
        FROM CreatedBy, Collections
        WHERE uid=:uid AND CreatedBy.cid=Collections.cid
        ''',
        uid=uid)
      print(rows)
      return [row for row in rows]

    @staticmethod
    def get_games(cid):
      rows = app.db.execute('''
        SELECT Games.*
        FROM HasGame, Games
        WHERE cid=:cid AND HasGame.gid=Games.gid
        ''',
        cid=cid
        )
      return [row for row in rows]
