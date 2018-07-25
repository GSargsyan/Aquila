from random import randint
from app.lib.table_view import TableView
from app.lib.utils import now
from app import Rooms, game_conf


class Rounds(TableView):
    def __init__(self):
        self.table_name = 'rounds'
        super().__init__()

    def current_by_room_id(self, room_id):
        """ Remove player from player_id_list of the room

        Parameters
        ----------
        room_id : int
            Id of the room to remove the player from
        pid : int
            Id of the player to remove from room
        """
        return self.find(['id', 'start_date', 'outcome'],
                         where='room_id = %(rid)s',
                         values={'rid': room_id}, order_by='start_date DESC')

    def initial_values(self):
        """ Get the initial Round values

        Returns
        -------
        dict
            Initial values
        """
        return {
                'room_id': None,
                'player_id_list': [],
                'outcome': None,
                'start_date': now(),
                'end_date': None
                }

    def init_in_room(self, room_id):
        """ Insert new round.

        Parameters
        ----------
        room_id : int
            The room id in which round is initialized
        """
        vals = self.initial_values()
        player_ids = Rooms.find_by_id(room_id,
                                      ['player_id_list']).player_id_list
        vals['room_id'] = room_id
        vals['player_id_list'] = player_ids
        self.insert(vals)

    def awaiting_rounds(self):
        """ Get the list of rounds that didn't end
        and x seconds have passed from starting time

        Returns
        -------
        list
            List of awaiting rounds
        """
        passed = game_conf['rounds_interval'] + game_conf['bet_timeout']
        return self.all(['id', 'outcome'], "end_date IS NULL AND "
                        "NOW() - start_date > INTERVAL '%(passed)s SECONDS'",
                        {'passed': passed})

    def end_round(self, round_id):
        """ Generate random number as outcome and end the round """
        self.update_by_id({'outcome': randint(0, 36),
                           'end_date': now()}, round_id)

    def has_room_running(self, room_id):
        """
        Parameters
        ----------
        room_id : int
            The id of the room to check against

        Returns
        -------
        bool
            True if the room has running round, False otherwise.
        """
        running = self.find(['id'], "room_id=%(rid)s "
                            "AND (end_date IS NULL OR NOW() - end_date < "
                            "INTERVAL '%(max_anim)s SECONDS')",
                            {'rid': room_id,
                             'max_anim': game_conf['max_anim_time']},
                            order_by='start_date DESC')

        return running is not None
