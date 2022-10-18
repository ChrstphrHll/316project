from flask import current_app as app


class Review:
    def __init__(self, gid, uid, rating, desc, time):
        self.gid = gid
        self.uid = uid
        self.desc = desc
        self.rating = rating
        self.time = time

    @staticmethod
    def get(gid, uid):
        rows = app.db.execute('''
SELECT gid, uid, rating, desc, time
FROM ReviewOf
WHERE gid = :gid
AND uid = :uid
''',
                              gid=gid, uid=uid)
        return Review(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_top_5(uid):
        rows = app.db.execute('''
SELECT gid, rating, desc, time
FROM ReviewOf
WHERE uid = :uid
ORDER BY time
LIMIT 5
''',
                              uid=uid)
        return [Review(*row) for row in rows]
