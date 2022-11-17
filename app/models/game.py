from flask import current_app as app
from sqlalchemy import null
import html

class Game:
    def __init__(self, gid, name, description, image_url, thumbnail_url, complexity, length, min_players, max_players):
        self.gid = gid
        self.name = name
        self.description = html.unescape(description)
        self.image_url = image_url
        self.thumbnail_url = thumbnail_url
        self.complexity = round(complexity,2)
        self.length = length
        self.min_players = min_players
        self.max_players = max_players

    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT *
FROM Games
''')
        return [Game(*row) for row in rows]

    @staticmethod
    def get(gid):
        query = '''
SELECT *
FROM Games
WHERE Games.gid = :gid
'''
        game_raw = app.db.execute(query, gid=gid)
        return Game(*game_raw[0]) if game_raw else null

    @staticmethod
    def get_random():
        game_raw = app.db.execute('''
SELECT * FROM Games
ORDER BY RANDOM()
LIMIT 1
''')
        return Game(*game_raw[0]) if game_raw else null
