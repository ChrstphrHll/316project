from flask import current_app as app
from .mechanic import Mechanic
from .game import Game
from .collection import Collection
from .user import User

class Recommendation:

    #only a game that has been liked before can be recommended to the user

    #returns the 5 most liked games
    @staticmethod
    def get_pop_games():
        rows = app.db.execute('''
        SELECT G.*
        FROM LikesGame as L, Games as G
        WHERE L.gid = G.gid
        GROUP BY G.gid, G.name, G.description, G.image_url, G.thumbnail_url, G.complexity, G.length, G.min_players, G.max_players
        ORDER BY COUNT(*) DESC
        ''')
        return [Game(*row) for row in rows[:5]]

    #returns 5 most popular collections
    @staticmethod
    def get_pop_coll():
        rows = app.db.execute('''
        SELECT C.*
        FROM Collections as C, LikesCollection as LC
        WHERE C.cid = LC.cid
        GROUP BY C.cid, C.title, C.description
        ORDER BY COUNT(*) DESC
        ''')
        return [Collection(*row) for row in rows[:5]]
  
    #returns the most common mechanic of the games liked
    @staticmethod
    def get_fav_mech(uid):
        rows = app.db.execute('''
        SELECT M.*
        FROM LikesGame as L, Implements as I, Mechanics as M
        WHERE L.uid =:uid AND L.gid = I.gid AND I.mech_name = M.mech_name
        GROUP BY M.mech_name, M.description
        ORDER BY COUNT(*) DESC
        ''', uid = uid)
        return Mechanic(*rows[0])

    # returns the designer who created the most games liked by uid
    @staticmethod
    def get_fav_designer(uid):
        rows = app.db.execute('''
        SELECT U.uid, U.name, U.email, U.about, U.image_url
        FROM LikesGame as L, DesignedBy as D, Users as U
        WHERE L.uid =:uid AND L.gid = D.gid AND U.uid = D.uid AND U.uid !=:uid
        GROUP BY U.uid, U.name, U.email, U.about, U.image_url
        ORDER BY COUNT(*) DESC
        ''', uid = uid)
        return User(*(rows[0])) if rows else None

    # returns additional games made by favorite designer
    @staticmethod
    def get_w_designer(uid, did):
        rows = app.db.execute('''
        WITH DG as
        (SELECT G.*
        FROM DesignedBy as D, Games as G
        WHERE D.uid =:did AND D.gid = G.gid)
        SELECT DG.*
        FROM LikesGame as L, DG
        WHERE L.uid !=:uid AND L.gid=DG.gid
        GROUP BY DG.gid, DG.name, DG.description, DG.image_url, DG.thumbnail_url, 
        DG.complexity, DG.length, DG.min_players, DG.max_players
        ORDER BY COUNT(*) DESC       
        ''', uid = uid, did=did)
        return [Game(*row) for row in rows[:5]]

    # returns low-complexity games that implement mech_name
    @staticmethod
    def get_w_easy_mech(uid, mech_name):
        rows = app.db.execute('''
        WITH IG as 
        (SELECT G.*
        FROM Implements as I, Games as G
        WHERE I.mech_name =:mech_name AND I.gid = G.gid AND G.complexity <= 2)
        (SELECT IG.*
        FROM LikesGame as L, IG
        WHERE L.uid !=:uid AND L.gid=IG.gid
        GROUP BY IG.gid, IG.name, IG.description, IG.image_url, IG.thumbnail_url, IG.complexity, IG.length, IG.min_players, IG.max_players
        ORDER BY COUNT(*) DESC)    
        ''', uid = uid, mech_name=mech_name)
        return [Game(*row) for row in rows[:5]] if rows else []

    # returns high-complexity games that implement mech_name
    @staticmethod
    def get_w_hard_mech(uid, mech_name):
        rows = app.db.execute('''
        WITH IG as
        (SELECT G.*
        FROM Implements as I, Games as G
        WHERE I.mech_name =:mech_name AND I.gid = G.gid AND G.complexity >= 4)
        SELECT IG.*
        FROM LikesGame as L, IG
        WHERE L.uid !=:uid AND L.gid=IG.gid
        GROUP BY IG.gid, IG.name, IG.description, IG.image_url, IG.thumbnail_url, 
        IG.complexity, IG.length, IG.min_players, IG.max_players
        ORDER BY COUNT(*) DESC            
        ''', uid = uid, mech_name=mech_name)
        return [Game(*row) for row in rows[:5]] if rows else []

    # returns new (never-liked) games that implement mech_name
    @staticmethod
    def get_new_games(mech_name):
        rows = app.db.execute('''
        WITH SM as (SELECT G.* FROM Games as G, Implements as I WHERE I.gid=G.gid AND I.mech_name=:mech_name),
        liked as (SELECT G.* FROM Games as G, LikesGame as L WHERE L.gid=G.gid)
        (SELECT * FROM SM) EXCEPT (SELECT * FROM liked)
        ''', mech_name=mech_name)
        return [Game(*row) for row in rows[:5]] if rows else []

    # returns collections that implements the user's favorite mechanic the most
    def get_sim_coll(mech):
        rows = app.db.execute('''
        SELECT C.*
        FROM Collections as C, HasGame as HG, Implements as I
        WHERE C.cid = HG.cid AND HG.gid=I.gid AND I.mech_name=:mech
        GROUP BY C.cid, C.title, C.description
        ORDER BY COUNT(*) DESC
        ''', mech=mech)
        return [Collection(*row) for row in rows[:5]] if rows else []

    #returns the top 5 games with the most similar mechanics to gid
    @staticmethod
    def get_sim_games(gid):
        rows = app.db.execute('''
        WITH GI AS (SELECT * FROM Games as G, Implements as I WHERE G.gid=I.gid AND G.gid=:gid),
        all_imp AS (SELECT I.gid FROM GI, Implements as I WHERE GI.mech_name=I.mech_name AND I.gid!=:gid)
        SELECT G.*
        FROM Games as G, all_imp as I
        WHERE G.gid=I.gid       
        GROUP BY G.gid, G.name, G.description, G.image_url, G.thumbnail_url, G.complexity, G.length, G.min_players, G.max_players
        ORDER BY COUNT(*) DESC
        ''', gid=gid)
        return [Game(*row) for row in rows[:10]]

    #returns games with similar mechs to those in the collection
    @staticmethod
    def get_new_coll(cid, mech):
        rows = app.db.execute('''
        (SELECT G.*
        FROM Games as G, Implements as I
        WHERE G.gid = I.gid AND I.mech_name =:mech)
        EXCEPT
        (SELECT G.*
        FROM Games as G, HasGame as H
        WHERE G.gid = H.gid and H.cid =:cid)    
        ''', mech=mech, cid = cid)
        return [Game(*row) for row in rows]