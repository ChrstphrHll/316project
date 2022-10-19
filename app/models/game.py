from flask import current_app as app

class Game:
    def __init__(self, gid, name, description, image_url, complexity, length, min_players, max_players):
        self.id = id
        self.name = name
        self.description = description
        self.image_url = image_url
        self.complexity = complexity
        self.length = length
        self.min_players = min_players
        self.max_players = max_players