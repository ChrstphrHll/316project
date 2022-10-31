from flask import current_app as app
from sqlalchemy import null

class Game:
    def __init__(self, gid, name, description, image_url, thumbnail_url, complexity, length, min_players, max_players):
        self.gid = gid
        self.name = name
        self.description = description
        self.image_url = image_url
        self.thumbnail_url = thumbnail_url
        self.complexity = complexity
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
