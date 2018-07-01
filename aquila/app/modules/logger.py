from app.lib.table_view import TableView
from app.lib.utils import now


class RoomLogger(TableView):
    def __init__(self):
        self.table_name = 'room_log'
        super().__init__()

    def log_entry(self, room_id, pid):
        self.insert({'room_id': room_id,
                     'player_id': pid,
                     'entry_date': now(),
                     'leave_date': None})

    def log_leave(self, room_id, pid):
        last_entry_id = self.find(['id'],
                'room_id=%(rid)s AND player_id=%(pid)s',
                {'rid': room_id, 'pid': pid}, order_by='entry_date DESC').id

        self.update_by_id({'leave_date': now()}, last_entry_id)


class ActionLogger:
    pass
