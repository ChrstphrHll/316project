from flask import current_app as app
from sqlalchemy import null
import html
from app.models.mechanic import Mechanic

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
    def get_some(mechanic = None, page = 0, per_page = 10, search=None):
        offset = page * per_page
        query = '''
SELECT Games.*
FROM Games
'''
        query_back = '''
LIMIT :per_page OFFSET :offset
'''
        conditions = []

        if mechanic and mechanic != "None":
            conditions.append(":mechanic in (SELECT mech_name FROM Implements WHERE Implements.gid = Games.gid)")

        if search:
            conditions.append(f"LOWER(Games.name) LIKE :search")

        if len(conditions) > 0:
            full_query = query + " WHERE " + " AND ".join(conditions) + query_back
        else:
            full_query = query + query_back

        game_raw = app.db.execute(full_query, per_page=per_page, offset=offset, mechanic=mechanic, search=f"%{search}%")
        return [Game(*row) for row in game_raw]

    @staticmethod
    def get_by_name(name):
        rows = app.db.execute('''
            SELECT * FROM Games
            WHERE Games.name = :name
            ''',
            name=name)
        return Game(*rows[0])

    @staticmethod
    def get_random():
        game_raw = app.db.execute('''
SELECT * FROM Games
ORDER BY RANDOM()
LIMIT 1
''')
        return Game(*game_raw[0]) if game_raw else null

    def get_mechanics(gid):
        rows = app.db.execute('''
SELECT m.*
FROM Mechanics m, Implements i
WHERE :gid = i.gid and i.mech_name = m.mech_name
''', gid=gid)
        return [Mechanic(*row) for row in rows]
