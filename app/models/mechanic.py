class Mechanic:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    @staticmethod
    def get_desc(name):
        rows = app.db.execute('''
            SELECT mech_name, description
            FROM Mechanics 
            WHERE mech_name = :name''', 
            name=name)

        return Product(*(rows[0])) if rows is not None else None
    
    @staticmethod
    def get_from_game(gid):
        rows = app.db.execute('''
            SELECT mech_name, gid
            FROM Implements
            WHERE gid = :gid''', 
            gid=gid)

        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all_from_game(gid):
        rows = app.db.execute('''
            SELECT mech_name, gid
            FROM Implements
            WHERE gid = :gid''', 
            gid=gid)

        return Product(*row) for row in rows

    @staticmethod
    def get_all(name):
        rows = app.db.execute('''
            SELECT mech_name, gid
            FROM Implements 
            WHERE mech_name = :name''', 
            name=name)

        return Product(*row) for row in rows
