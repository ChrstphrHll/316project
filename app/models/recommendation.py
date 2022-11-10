from flask import current_app as app
from .mechanic import Mechanic
from .game import Game

class Recommendation:
    #returns games that user uid likes
    @staticmethod
    def get_base(uid):
        rows = app.db.execute('''
SELECT g.*
FROM Games as g, LikesGame as L
WHERE L.uid = :uid AND g.gid = L.gid
''',
                              uid=uid)
        return [Game(*row) for row in rows]

    @staticmethod
    def get_pop_mech(uid):
        rows = app.db.execute('''
        SELECT M.*
        FROM LikesGame as L, Implements as I, Mechanics as M
        WHERE L.uid =:uid AND L.gid = I.gid AND I.mech_name = M.mech_name
        GROUP BY M.mech_name, M.description
        ORDER BY COUNT(*) DESC
        ''', uid = uid)
        return [Mechanic(*row) for row in rows]

    @staticmethod
    def get_easy_mech(uid, mech_name):
        rows = app.db.execute('''
        (SELECT G.*
        FROM Implements as I, Games as G
        WHERE I.mech_name =:mech_name AND I.gid = G.gid AND G.complexity <= 2)
        EXCEPT
        (SELECT G.*
        FROM LikesGame as L, Games as G
        WHERE L.uid =:uid AND L.gid=G.gid)        
        ''', uid = uid, mech_name=mech_name)
        return [Game(*row) for row in rows]

    @staticmethod
    def get_hard_mech(uid, mech_name):
        rows = app.db.execute('''
        (SELECT G.*
        FROM Implements as I, Games as G
        WHERE I.mech_name =:mech_name AND I.gid = G.gid AND G.complexity >= 4)
        EXCEPT
        (SELECT G.*
        FROM LikesGame as L, Games as G
        WHERE L.uid =:uid AND L.gid=G.gid)        
        ''', uid = uid, mech_name=mech_name)
        return [Game(*row) for row in rows]

    @staticmethod
    def get(uid, gid):
        rows = app.db.execute('''
    WITH liked_mech AS (SELECT I.mech_name FROM LikesGame as L, Implements as I
    WHERE L.gid = :gid AND L.uid = :uid AND I.gid = L.gid)
    (SELECT DISTINCT g.*
    FROM Games as g, liked_mech as M, Implements as Imp
    WHERE g.gid = Imp.gid AND Imp.mech_name = M.mech_name)
    EXCEPT
    (SELECT DISTINCT g.*
    FROM Games as g, LikesGame as L
    WHERE L.gid = :gid AND L.uid = :uid AND g.gid = L.gid)
    ''',
                                uid=uid, gid=gid)
        return [Game(*row) for row in rows]

    """
    @staticmethod
    def get(uid):
        rows = app.db.execute('''
    WITH liked AS (SELECT * FROM LikesGame WHERE uid = :uid),
    liked_mech AS (SELECT M.mech_name FROM liked as L, Mechanics as M, Implements as I
    WHERE I.gid = L.gid AND I.mech_name = M.mech_name)
    SELECT DISTINCT g.gid, g.name, g.description, g.image_url, g.thumbnail_url, g.complexity, g.length, g.min_players, g.max_players
    FROM Games as g, liked_mech as M, Implements as Imp
    WHERE g.gid = Imp.gid AND Imp.mech_name = M.mech_name
    ''',
                                uid=uid)
        return [Game(*row) for row in rows]
    """
