from flask import current_app as app

class Mechanic:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    @staticmethod
    def get(gid):
        rows = app.db.execute('''
            SELECT M.mech_name, M.description
            FROM Mechanics as M, Implements as I
            WHERE M.mech_name = I.mech_name AND I.gid =:gid
            ''', 
            gid=gid)

        return [Mechanic(*row) for row in rows]

    @staticmethod
    def get_all():
        rows = app.db.execute('''
            SELECT *
            FROM Mechanics as M
            ORDER BY M.mech_name
            ''', )

    #forms are part of html

        return [Mechanic(*row) for row in rows]

    @staticmethod
    def get_desc(name):
        rows = app.db.execute('''
            SELECT mech_name, description
            FROM Mechanics 
            WHERE mech_name = :name''', 
            name=name)

        return [Mechanic(*row) for row in rows]
    
    @staticmethod
    def get_games(name):
        rows = app.db.execute('''
            SELECT g.gid, g.name, g.description, g.image_url, g.complexity, g.length, g.min_players, g.max_players
            FROM Implements as I, Games as g
            WHERE I.mech_name = :name and g.gid = I.gid''', 
            name=name)

        return [Mechanic(*row) for row in rows]