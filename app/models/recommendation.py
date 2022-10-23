from flask import current_app as app
from mechanic import Mechanic

class Recommendation:
    @staticmethod
    def get(gid):
        rows = app.db.execute('''
WITH all_mech AS (SELECT mech_name
FROM Implements WHERE gid = :gid)
SELECT g.name, g.image_url, g.description
FROM Games g, all_mech M, Implements I
WHERE I.mech_name=M.mech_name AND g.gid=I.gid
''',
                              gid=gid)
        return [Games(*row) for row in rows]