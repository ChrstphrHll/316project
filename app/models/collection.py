from flask import current_app as app
from app.models.game import Game
from app.models.user import User

class Collection:
    def __init__(self, cid, title, description):
        self.cid = cid
        self.title = title
        self.description = description
        self.creator = Collection.get_creator(cid)

    @staticmethod
    def get(cid):
      rows = app.db.execute('''
        SELECT *
        FROM Collections
        WHERE cid = :cid
        ''',
        cid=cid)
      return Collection(*(rows[0])) if rows else None

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
        SELECT Collections.*
        FROM CreatedBy, Collections
        WHERE uid=:uid AND CreatedBy.cid=Collections.cid
        ''',
        uid=uid)
      return [Collection(*row) for row in rows]

    @staticmethod
    def get_creator(cid):
      rows = app.db.execute('''
        SELECT Users.uid, name, email, about, image_url
        FROM Users, CreatedBy
        WHERE cid=:cid AND CreatedBy.uid=Users.uid
        ''',
        cid=cid)
      return User(*(rows[0])) if rows else None

    @staticmethod
    def get_games(cid):
      rows = app.db.execute('''
        SELECT Games.*
        FROM HasGame, Games
        WHERE cid=:cid AND HasGame.gid=Games.gid
        ''',
        cid=cid
        )
      return [Game(*row) for row in rows]
