from random import randint
from app.lib.table_view import TableView
from app.lib.utils import now, pp
from app import Players, Rooms, game_conf


class Rounds(TableView):
    def __init__(self):
        self.table_name = 'rounds'
        super().__init__()

    def current_by_room_id(self, room_id):
        return self.find(['start_date'], where='room_id = %(rid)s',
                values={'rid': room_id}, order_by='start_date DESC')

    def initial_values(self):
        return {
                'room_id': None,
                'player_id_list': [],
                'outcome': None,
                'start_date': now(),
                'end_date': None
                }

    def init_in_room(self, room_id):
        vals = self.initial_values()
        player_ids = Rooms.find_by_id(room_id, ['player_id_list']).player_id_list
        vals['room_id'] = room_id
        vals['player_id_list'] = player_ids
        self.insert(vals)

    def end_late_rounds(self):
        passed = int(game_conf['rounds_interval']) + int(game_conf['bet_timeout'])
        late_rounds = self.all(['id'], "end_date IS NULL AND "
                "NOW() - start_date > INTERVAL '{} SECONDS'".format(passed))

        for rnd in late_rounds:
            self.end_round(rnd.id)

    def end_round(self, round_id):
        self.update_by_id({'outcome': randint(0, 36),
            'end_date': now()}, round_id)

    def has_room_running(self, room_id):
        running = self.find(['id'], "room_id=%(rid)s "
            "AND (end_date IS NULL OR NOW() - end_date < "
            "INTERVAL '{} SECONDS')".format(game_conf['max_anim_time']),
                {'rid': room_id}, 'start_date DESC')
        return running is not None
