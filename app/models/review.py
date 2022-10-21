from flask import current_app as app


class Review:
    def __init__(self, uid, gid, rating, description, time_posted):
        self.gid = gid
        self.uid = uid
        self.description = description
        self.rating = rating
        self.time_posted = time_posted

    @staticmethod
    def get(gid, uid):
        rows = app.db.execute('''
SELECT gid, uid, rating, description, time_posted
FROM ReviewOf
WHERE gid = :gid
AND uid = :uid
''',
                              gid=gid, uid=uid)
        return Review(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_top_5(uid):
        rows = app.db.execute('''
SELECT uid, gid, rating, description, time_posted
FROM ReviewOf
WHERE uid = :uid
ORDER BY time_posted
DESC LIMIT 5
''',
                              uid=uid)
        return [Review(*row) for row in rows]
