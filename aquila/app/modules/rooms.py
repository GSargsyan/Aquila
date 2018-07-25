from app.lib.table_view import TableView
from app import RoomLogger


class Rooms(TableView):
    def __init__(self):
        self.table_name = 'rooms'
        self.count = 1000
        self.max_players = 9

        super().__init__()

    def id_by_max_players(self):
        """ Get a room with max players playing and is not full

        Returns
        -------
        int
            Id of the room found
        """
        # TODO: check if not full
        return self.find(['id'],
                         order_by='CARDINALITY(player_id_list) DESC').id

    def add_player(self, room_id, pid):
        """ Add player into player_id_list of the room

        Parameters
        ----------
        room_id : int
            Id of the room to add the player in
        pid : int
            Id of the player to add in room
        """
        vals = {'player_id_list': "array_append(player_id_list, %(pid)s)"}
        self.update_by_existing(vals, 'id=%(rid)s',
                                {'pid': pid, 'rid': room_id})

        RoomLogger.log_entry(room_id, pid)

    def remove_player(self, room_id, pid):
        """ Remove player from player_id_list of the room

        Parameters
        ----------
        room_id : int
            Id of the room to remove the player from
        pid : int
            Id of the player to remove from room
        """
        vals = {'player_id_list': "array_remove(player_id_list, %(pid)s)"}
        self.update_by_existing(vals,
                                'id=%(rid)s',
                                {'rid': room_id, 'pid': pid})

        RoomLogger.log_leave(room_id, pid)

    def run_awaiting(self):
        """ Run rooms that have players inside but are not running yet """
        self.update({'is_running': True},
                    "is_running = FALSE AND "
                    "ARRAY_LENGTH(player_id_list, 1) > 0")

    def all_running(self):
        """ Get the list of running rooms
        Returns
        -------
        list
            List of running rooms
        """
        return self.all(['id'], 'is_running = TRUE')

    def close_empty(self):
        """ Close rooms that are running but have no players inside """
        self.update({'is_running': False}, "is_running = TRUE AND "
                    "ARRAY_LENGTH(player_id_list, 1) IS NULL")


class ChatMessages:
    pass
