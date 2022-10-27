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
      rows = app.db.execute('''
        SELECT cid
        FROM CreatedBy
        WHERE uid=:uid
        ''',
        uid=uid)
      return [Collection.get(cid) for cid in rows]

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
