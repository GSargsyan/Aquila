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
        # TODO: find a way to concat in pscyopg2
        players_list = self.find_by_id(room_id,
                fields=['player_id_list']).player_id_list
        players_list.append(pid)
        self.update_by_id(
                {'player_id_list': players_list},
                room_id)

        # RoomLogger.log_entry(room_id, pid)
        RoomLogger.log_leave(room_id, pid)

    def remove_player():
        pass


class ChatMessages:
    pass
