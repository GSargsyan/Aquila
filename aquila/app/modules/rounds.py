from app.lib.table_view import TableView
from app import Players, Rooms


class Rounds(TableView):
    def __init__(self):
        self.table_name = 'rounds'
        super().__init__()

    def checkup(self):
        pid = g.player.id

    def curr_by_room_id(self, room_id):
        return self.find(where='room_id = %(rid)s',
                vals={'rid': room_id}, order_by='start_date DESC')

# Methods in Round class assume 'player' is in g
class Round(TableView):
    def __init__(self):
        self.table_name = 'rounds'
        super().__init__()
