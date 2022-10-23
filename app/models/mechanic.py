class Mechanic:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def get(name):
        rows = app.db.execute('''
            SELECT mech_name, description
            FROM Mechanics 
            WHERE mech_name = :name''', 
            name=name)

        return Product(*(rows[0])) if rows is not None else None

    def get_all(name):
        rows = app.db.execute('''
            SELECT mech_name, gid
            FROM Implements 
            WHERE mech_name = :name''', 
            name=name)

        return Product(*row) for row in rows
