from app import db

class DBTable():
    def __init__(self):
        self.link = db

    def find_by_field(self, field, val):
        return self.link.select(self.table_name,
                where='{}={}'.format(field, val), limit=1)[0]

    def find_by_id(self, item_id):
        return self.find_by_field('id', item_id)
