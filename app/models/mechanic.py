from flask import current_app as app
from app.models.game import Game

class Mechanic:
    def __init__(self, mech_name, description):
        self.mech_name = mech_name
        self.description = description

    #given a game, return all mechanics
    @staticmethod
    def get_mechs(gid):
        rows = app.db.execute('''
            SELECT M.*
            FROM Mechanics as M, Implements as I
            WHERE M.mech_name = I.mech_name AND I.gid =:gid
            ''', 
            gid=gid)

        return [Mechanic(*row) for row in rows]

    #given a set of games, return all mechanics used, sorted by popularity
    @staticmethod
    def get_games_mechs(games):
        rows = app.db.execute('''
            SELECT M.*
            FROM Mechanics as M, Implements as I
            WHERE M.mech_name = I.mech_name AND I.gid IN :games
            ''', 
            games=games)

        return [Mechanic(*row) for row in rows]

    @staticmethod
    def get_all():
        rows = app.db.execute('''
            SELECT M.*
            FROM Mechanics as M
            ORDER BY M.mech_name
            ''', )

        return [Mechanic(*row) for row in rows]
    
    #get all games that use a given mechanic
    @staticmethod
    def get_games(name):
        rows = app.db.execute('''
            SELECT g.*
            FROM Implements as I, Games as g
            WHERE I.mech_name = :name and g.gid = I.gid''', 
            name=name)

        return [Game(*row) for row in rows]
