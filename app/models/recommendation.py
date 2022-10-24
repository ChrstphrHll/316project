from flask import current_app as app
from .mechanic import Mechanic
from .game import Game

class Recommendation:
    @staticmethod
    def get(uid):
        rows = app.db.execute('''
    WITH liked AS (SELECT * FROM LikesGame WHERE uid = :uid),
    liked_mech AS (SELECT M.mech_name FROM liked as L, Mechanics as M, Implements as I
    WHERE I.gid = L.gid AND I.mech_name = M.mech_name)
    SELECT g.gid, g.name, g.description, g.image_url, g.complexity, g.length, g.min_players, g.max_players
    FROM Games as g, liked_mech as M, Implements as Imp
    WHERE g.gid = Imp.gid AND Imp.mech_name = M.mech_name
    ''',
                                uid=uid)
        return [Game(*row) for row in rows]

    