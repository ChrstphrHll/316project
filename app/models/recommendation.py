from flask import current_app as app
from .game import Game

class Recommendation:
    @staticmethod
    def get(gid):
        rows = app.db.execute('''
WITH game1 AS (SELECT min_players as min1
FROM Games WHERE gid = :gid)
SELECT name, image_url, description
FROM Games
WHERE min_players = game1.min1 AND complexity = 
''',
                              gid=gid)
        return [Games(*row) for row in rows]