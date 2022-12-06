from flask import current_app as app


class Review:
    def __init__(self, name, rating, description, time_posted):
        self.name = name
        self.description = description
        self.rating = rating
        self.time_posted = time_posted

    @staticmethod
    def get(gid, uid):
        rows = app.db.execute('''
SELECT gid, rating, description, time_posted
FROM ReviewOf
WHERE gid = :gid AND uid = :uid
''',
                              gid=gid, uid=uid)
        return [Review(*row) for row in rows]

    @staticmethod
    def get_top_5(uid):
        rows = app.db.execute('''
SELECT gid, rating, description, time_posted
FROM ReviewOf
WHERE uid = :uid
ORDER BY time_posted
DESC LIMIT 5
''',
                              uid=uid)
        return [Review(*row) for row in rows]

    @staticmethod
    def get_top_5_game(gid):
        rows = app.db.execute('''
SELECT u.name, r.rating, r.description, r.time_posted
FROM ReviewOf as r, Users as u
WHERE r.gid = :gid AND u.uid = r.uid 
ORDER BY time_posted
DESC LIMIT 5
''',
                              gid=gid)
        return [Review(*row) for row in rows]
    
    @staticmethod
    def create(uid, gid, rating, description, time_posted):
      try:
        rows = app.db.execute("""
          INSERT INTO ReviewOf
          VALUES(:uid, :gid, :rating, :description, :time_posted)
          """,
          uid=uid, gid=gid, rating=rating, description=description, time_posted=time_posted
        )
      except Exception as e:
        print(str(e))
        return None
    @staticmethod
    def delete(uid, gid):
      try:
        rows = app.db.execute("""
          DELETE FROM ReviewOf
          WHERE uid = :uid AND gid = :gid
          """,
          uid=uid, gid=gid)
      except Exception as e:
        print(str(e))
        return None
    
    @staticmethod
    def get_all_user(uid):
        rows = app.db.execute('''
SELECT g.name, r.rating, r.description, r.time_posted
FROM ReviewOf as r, Games as g
WHERE r.uid = :uid AND g.gid = r.gid 
ORDER BY time_posted
DESC
''',
                              uid=uid)
        return [Review(*row) for row in rows]

    @staticmethod
    def get_avg_rating(gid):
        rows = app.db.execute('''
SELECT AVG(rating)
FROM ReviewOf
WHERE gid=:gid 
''',
                              gid=gid)
        return rows[0][0]
