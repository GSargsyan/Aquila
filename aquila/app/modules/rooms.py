from random import randint

from flask import g

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
        return self.find(['id'], order_by='CARDINALITY(player_id_list) DESC').id

    def add_player(self, room_id, pid):
        self.link.execute("UPDATE {} SET player_id_list = array_append"
                          "(player_id_list, %(pid)s)"
                          " WHERE id=%(rid)s".format(self.table_name),
                          {'pid': pid, 'rid': room_id})

        RoomLogger.log_entry(room_id, pid)

    def remove_player(self, room_id, pid):
        self.link.execute("UPDATE {} SET player_id_list = array_remove"
                          "(player_id_list, %(pid)s)"
                          " WHERE id=%(rid)s".format(self.table_name),
                          {'pid': pid, 'rid': room_id})

        RoomLogger.log_leave(room_id, pid)


class ChatMessages:
    pass
