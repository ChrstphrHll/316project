from flask import current_app as app
from .mechanic import Mechanic

class Recommendation:
    @staticmethod
    def get(uid):
        rows = app.db.execute('''
    WITH liked_gid AS (SELECT gid FROM LikesGame WHERE uid = :uid),
    all_mech AS (SELECT mech_name
    FROM Implements as I, liked_gid as LG WHERE I.gid = LG.gid)
    SELECT g.name, g.image_url, g.description
    FROM Games as g, all_mech as M, Implements as I
    WHERE I.mech_name=M.mech_name AND g.gid=I.gid
    ''',
                                uid=uid)
        return [Games(*row) for row in rows]
    