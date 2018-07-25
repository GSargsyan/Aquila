from random import randint

from app.lib.table_view import TableView
from app import RoomLogger


class Rooms(TableView):
    def __init__(self):
        self.table_name = 'rooms'
        self.count = 1000
        self.max_players = 9

        super().__init__()

    def rand_room(self):
        return self.find_by_id(randint(1, self.count))

    def id_by_max_players(self):
        return self.find(['id'],
                         order_by='CARDINALITY(player_id_list) DESC').id

    def add_player(self, room_id, pid):
        vals = {'player_id_list': "array_append(player_id_list, %(pid)s)"}
        self.update_by_existing(vals, 'id=%(rid)s',
                                {'pid': pid, 'rid': room_id})

        RoomLogger.log_entry(room_id, pid)

    def remove_player(self, room_id, pid):
        vals = {'player_id_list': "array_remove(player_id_list, %(pid)s)"}
        self.update_by_existing(vals,
                                'id=%(rid)s',
                                {'rid': room_id, 'pid': pid})

        RoomLogger.log_leave(room_id, pid)

    def run_awaiting(self):
        return self.update({'is_running': True},
                           "is_running = FALSE AND "
                           "ARRAY_LENGTH(player_id_list, 1) > 0")

    def all_running(self):
        return self.all(['id'], 'is_running = TRUE')

    def close_empty(self):
        self.update({'is_running': False}, "is_running = TRUE AND "
                    "ARRAY_LENGTH(player_id_list, 1) IS NULL")


class ChatMessages:
    pass
