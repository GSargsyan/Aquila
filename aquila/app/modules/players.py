from app.lib.table_view import TableView


class Players(TableView):
    def __init__(self):
        self.table_name = 'players'
        super().__init__()
