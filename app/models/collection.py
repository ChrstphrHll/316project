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
    def create(title, description, uid):
      try:
        rows = app.db.execute("""
          INSERT INTO Collections(title, description)
          VALUES(:title, :description)
          RETURNING cid
          """,
          title=title,
          description=description
        )
        
        cid = rows[0][0]
        
        app.db.execute("""
          INSERT INTO CreatedBy(cid, uid)
          VALUES(:cid, :uid)
          """,
          cid=cid,
          uid=uid
        )
        
        return Collection.get(cid)
      except Exception as e:
        print(str(e))
        return None

    @staticmethod
    def delete(cid):
      try:
        app.db.execute('''
          DELETE FROM CreatedBy
          WHERE cid=:cid
          ''',
          cid=cid,
          )

        app.db.execute('''
          DELETE FROM HasGame
          WHERE cid=:cid
          ''',
          cid=cid,
          )

        app.db.execute('''
          DELETE FROM Collections
          WHERE cid=:cid
          ''',
          cid=cid,
          )

        return True 
      except Exception as e:
        print(str(e))
        return None
      
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

    def get_liked_status(uid, cid):
      rows = app.db.execute("""
SELECT * FROM LikesCollection WHERE LikesCollection.uid = :uid AND LikesCollection.cid = :cid
""", uid=uid, cid=cid)
      if len(rows) != 0:
            return True
      return False

    def toggle_like_collection(uid, cid):
        updated = app.db.execute("""
DELETE FROM LikesCollection WHERE uid = :uid AND cid = :cid;        
""", uid=uid, cid=cid)

        if updated == 0:
            app.db.execute("""
INSERT INTO LikesCollection (cid, uid) VALUES (:cid, :uid)        
""", uid=uid, cid=cid)

    def get_liked_collections(uid):
      rows = app.db.execute("""
SELECT Collections.*
FROM Collections, LikesCollection
WHERE Collections.cid = LikesCollection.cid AND LikesCollection.uid = :uid
""", uid=uid)
      return [Collection(*row) for row in rows]
    @staticmethod
    def add_game(cid, gid):
      try:
        rows = app.db.execute("""
            SELECT * FROM HasGame
            WHERE gid=:gid AND cid=:cid
            """,
            cid=cid,
            gid=gid
            )

        if not len(rows):
          app.db.execute("""
              INSERT INTO HasGame(cid, gid)
              VALUES(:cid, :gid)
              """,
              cid=cid,
              gid=gid,
            )
          return Collection.get(cid)
      except Exception as e:
        print(str(e))
        return None

    # TODO
    def remove_game(cid, gid):
      return None
