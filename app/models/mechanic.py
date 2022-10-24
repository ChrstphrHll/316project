class Mechanic:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    @staticmethod
    def get():
        rows = app.db.execute('''
            SELECT *
            FROM Mechanics''',)

        return Mechanic(*(rows[0])) if rows is not None else None

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