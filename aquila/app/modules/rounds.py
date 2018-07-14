from app.lib.table_view import TableView
from app import Players, Rooms


class Rounds(TableView):
    def __init__(self):
        self.table_name = 'rounds'
        super().__init__()

    def curr_by_room_id(self, room_id):
        return self.find(['id'], where='room_id = %(rid)s',
                values={'rid': room_id}, order_by='start_date DESC')
