from app.lib.db_table import DBTable


class Players(DBTable):
    def __init__(self):
        self.table_name = 'players'
        super().__init__()
