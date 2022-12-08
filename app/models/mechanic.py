from flask import current_app as app

class Mechanic:
    def __init__(self, mech_name, description):
        self.mech_name = mech_name
        self.description = description

    #given a game, return all mechanics
    @staticmethod
    def get_mechs(gid):
        try:
            rows = app.db.execute('''
                SELECT M.*
                FROM Mechanics as M, Implements as I
                WHERE M.mech_name = I.mech_name AND I.gid =:gid
                ''', 
                gid=gid)

            return [Mechanic(*row) for row in rows]
        except Exception as e:
            print(str(e))
            return False

    #given a set of games, return the mechanics they share with gid
    def get_shared_mechs_all(gid, games):
        try:
            shared_mechs = []
            for i in range(len(games)):
                mechs = Mechanic.get_shared_mechs(gid, games[i].gid)
                shared_mechs.append(mechs)
            return shared_mechs
        except Exception as e:
            print(str(e))
            return False

    #given two games, return all mechanics they have in common
    def get_shared_mechs(gid1, gid2):
        try:
            rows = app.db.execute('''
                WITH M1 as (SELECT I.* FROM Implements as I WHERE I.gid=:gid1),
                M2 as (SELECT I.* FROM Implements as I WHERE I.gid=:gid2)
                SELECT M.*
                FROM Mechanics as M, M1, M2
                WHERE M.mech_name = M1.mech_name AND M1.mech_name=M2.mech_name
                ''', 
                gid1=gid1, gid2=gid2)

            return [Mechanic(*row).mech_name for row in rows]
        except Exception as e:
            print(str(e))
            return False

    #given a set of games, return all mechanics used, sorted by popularity
    @staticmethod
    def get_games_mechs(games):
        try:
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
        except Exception as e:
            print(str(e))
            return False

    #returns all possible mechanics
    @staticmethod
    def get_all():
        try:
            rows = app.db.execute('''
                SELECT M.*
                FROM Mechanics as M
                ORDER BY M.mech_name
                ''', )

            return [Mechanic(*row) for row in rows]
        except Exception as e:
            print(str(e))
            return False
