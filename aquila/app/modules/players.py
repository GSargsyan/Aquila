from app.lib.table_view import TableView
from app.lib.utils import is_latin, throw_ve, now
from app import Countries, Levels


class Players(TableView):
    def __init__(self):
        self.table_name = 'players'
        super().__init__()

    def initial_values(self):
        return {
		'balance': 0,
		'demo_balance': 10,
		'level': None,
		'exp': 0,
		'wagered': 0,
		'won': 0,
		'lost': 0,
		'status': 'alive',
		'chat_messages_count': 0,
		'bets_count': 0,
		'bets_won_count': 0,
		'country_id': None,
		'registered_date': now(),
		'settings': None,
		'is_online': True
                }


    def user_exists(self, uname):
        return self.find_by_field('username', uname, fields=['id']) is not None

    def validate_uname(self, uname):
        # Contains valid characters
        if not is_latin(uname):
            throw_ve('Username contains invalid character.')

        # Length checkings
        if len(uname) < 6:
            throw_ve('Username must be at least 6 characters long.')
        if len(uname) > 18:
            throw_ve('Username can be at most 18 characters long.')

        # Other player with the same username
        if self.user_exists(uname):
            throw_ve('Another user with the same username already exists.')


    def validate_pwd(self, pwd):
        # Contains valid characters
        if not is_latin(pwd):
            throw_ve('Password contains invalid character.')

        # Length checkings
        if len(pwd) < 6:
            throw_ve('Password must be at least 6 characters long.')
        if len(pwd) > 18:
            throw_ve('Password can be at most 18 characters long.')


    def register_player(self, uname, pwd):
        self.validate_uname(uname)
        self.validate_pwd(pwd)

        vals = self.initial_values()
        vals['username'] = uname
        vals['password'] = pwd

        pid = self.insert(vals, ret='id')


class PlayerRelations:
    pass


class PlayerBlocks:
    pass


class Feedbacks:
    pass


class ActionLogger:
    pass
