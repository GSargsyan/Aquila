from flask import request, session, g

from app.lib.table_view import TableView
from app.lib.utils import is_latin, throw_ve, now, hash_pwd, verify_pwd, \
        random_alphanum
from app import Countries, Rooms, LoginLogger, game_conf, sec_conf


class Players(TableView):
    def __init__(self):
        self.table_name = 'players'
        super().__init__()

    def initial_values(self):
        """ Get the initial Player values for registration

        Returns
        -------
        dict
            Initial values
        """
        return {
            'username': None,
            'password': None,
            'balance': 0,
            'token': None,
            'demo_balance': game_conf['initial_demo_bal'],
            'level_id': None,
            'exp': 0,
            'wagered': 0,
            'won': 0,
            'lost': 0,
            'status': 'alive',
            'chat_messages_count': 0,
            'bets_count': 0,
            'bets_won_count': 0,
            'country_id': Countries.iso2_from_ip(request.remote_addr),
            'registered_date': now(),
            'settings': None,
            'room_id': None,
            'last_checkup': None,
            'is_online': True
        }

    def user_exists(self, uname):
        """
        Returns
        -------
        bool
            True if username exists in the database, False otherwise
        """
        return self.find_by_field('username', uname, fields=['id']) is not None

    def _session_login(self, pid):
        """ Logs in the player in session and in g

        Parameters
        ----------
        pid : int
            player's id to login in session
        """
        session['pid'] = pid
        session.permanent = True
        g.player = self.find_by_id(session['pid'])

    def login_player(self, uname, pwd):
        """ Check if player exists, and password matches with username.
        If yes login the player into session

        Parameters
        ----------
        uname : str
            Username of the player.
        pwd : str
            Plain password typed by the player.

        Returns
        ------
        bool
            True if login was successful, False otherwise.
        """
        player = self.find(['id', 'password'],
                           'username=%(uname)s',
                           {'uname': uname})

        if player is None or not verify_pwd(pwd, player.password):
            return False

        self._session_login(player.id)
        LoginLogger.log_login(player.id)
        return True

    def validate_uname(self, uname):
        """ Check new username to be valid in length and charset.

        Parameters
        ----------
        uname : str
            Username to check against.

        Raises
        ------
        ValidationError
            If the username doesn't satisfy at least one condition.
        """
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
        """ Check new password to be valid in length and charset.

        Parameters
        ----------
        pwd : str
            Password to check against.

        Raises
        ------
        ValidationError
            If the password doesn't satisfy at least one condition.
        """
        # Contains valid characters
        if not is_latin(pwd):
            throw_ve('Password contains invalid character.')

        # Length checkings
        if len(pwd) < 6:
            throw_ve('Password must be at least 6 characters long.')
        if len(pwd) > 18:
            throw_ve('Password can be at most 18 characters long.')

    def register_player(self, uname, pwd):
        """ Try to register a new player. If successful login the player.
        Hashes password, generates random alphanumeric as token.

        Parameters
        ----------
        uname : str
            Username of the player.
        pwd : str
            Plain password typed by the player.

        Raises
        ------
        ValidationError
            If the password and/or the username are not valid.
        """
        self.validate_uname(uname)
        self.validate_pwd(pwd)

        vals = self.initial_values()
        vals['username'] = uname
        vals['password'] = hash_pwd(pwd)

        tokens_res = self.all(['token'])
        tokens_set = {rec.token for rec in tokens_res}
        vals['token'] = random_alphanum(sec_conf['token_len'], tokens_set)

        pid = self.insert(vals, ret='id')
        self._session_login(pid)
        LoginLogger.log_login(pid)

    def remove_afks(self):
        """ Remove players from rooms that didn't send 'checkout' request
        in the past x seconds
        """
        afks = self.all(['id', 'room_id'],
                        "is_online = TRUE AND "
                        "NOW() - last_checkup > INTERVAL '%(tout)s SECONDS'"
                        "AND room_id IS NOT NULL",
                        {'tout': game_conf['player_timeout']})

        for afk in afks:
            Rooms.remove_player(afk.room_id, afk.id)
            self.update_by_id({'room_id': None}, afk.id)

    def change_balance(self, pid, which, op, val):
        """ Change players balance

        Parameters
        ----------
        pid : int
            Players id
        which : str
            Which balance to change - demo_balance or balance
        op : str
            Operation to perform - '+' or '-'
        val : str
            Value to add or substract
        """

        vals = {which: which + op + str(val)}
        self.update_by_existing(vals, "id={}".format(pid))

    def change_bet_stats(self, pid, amount, won):
        """ Change players statistics
        based on the outcome and amount of the bet

        Parameters
        ----------
        pid : int
            Players id
        amount : int
            Amount of the bet player did.
        won : bool
            If the bet was won by the player
        """
        amt_str = str(amount)
        vals = {}

        vals['wagered'] = 'wagered + ' + amt_str
        vals['bets_count'] = 'bets_count + 1'
        if won:
            vals['won'] = 'won + ' + amt_str
            vals['bets_won_count'] = 'bets_won_count + 1'
        else:
            vals['lost'] = 'lost + ' + amt_str

        self.update_by_existing(vals, "id={}".format(pid))


class Player(TableView):
    """ Methods in this class assume 'player' is in g """
    def __init__(self):
        self.table_name = 'players'
        super().__init__()

    def quit_any_room(self):
        """ Quit the room currently in """
        room_id = g.player.room_id
        pid = g.player.id

        if room_id is not None:
            Rooms.remove_player(room_id, pid)
            self.update_by_id({'room_id': None}, pid)

    def join_some_room(self):
        """ Quit any room first, if inside one.
        Join the room with the most players playing currently
        """
        self.quit_any_room()

        pid = g.player.id
        room_id = Rooms.id_by_max_players()
        self.update_by_id({'room_id': room_id, 'last_checkup': now()}, pid)

        Rooms.add_player(room_id, pid)

        return room_id

    def is_logged_in(self):
        """
        Returns
        -------
        bool
            True if the player is logged in in session.
        """
        return 'pid' in session

    def are_bets_real(self):
        """
        Returns
        -------
        bool
            True if the next bets of the player will use the real balance,
            False if - demo_balance
        """
        return False

    def get_balance(self):
        """
        Returns
        -------
        int
            The balance or the demo_balance of the player.
        """
        return g.player.balance if self.are_bets_real() \
            else g.player.demo_balance

    def get_token(self):
        """
        Returns
        -------
        int
            Token of the player
        """
        return self.find_by_id(g.player.id, ['token']).token


class PlayerRelations:
    pass


class PlayerBlocks:
    pass


class Feedbacks:
    pass
