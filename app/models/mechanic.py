from flask import current_app as app

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

        for row in rows:
            print(row)

        return [Mechanic(*row) for row in rows]

    #given a set of games, return all mechanics used, sorted by popularity
    @staticmethod
    def get_games_mechs(games):
        mech_counts = {}

        for gid in games:            
            rows = app.db.execute('''
                SELECT M.*
                FROM Mechanics as M, Implements as I
                WHERE M.mech_name = I.mech_name AND I.gid =:gid
                ''', 
                gid=gid)

            for row in rows:
                mech = Mechanic(*row)
                if mech_counts[mech.mech_name] is NULL:
                    mech_counts[mech.mech_name] = 0
                mech_counts[mech.mech_name] = mech_counts[mech.mech_name] + 1

        return mech_counts

    @staticmethod
    def get_all():
        rows = app.db.execute('''
            SELECT M.*
            FROM Mechanics as M
            ORDER BY M.mech_name
            ''', )

        return [Mechanic(*row) for row in rows]
