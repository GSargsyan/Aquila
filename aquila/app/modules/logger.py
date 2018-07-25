from flask import request

from app.lib.table_view import TableView
from app.lib.utils import now


class RoomLogger(TableView):
    """ Class to insert/handle data in 'room_log' table.
    Responsible for logging room entries and leaves.
    """
    def __init__(self):
        self.table_name = 'room_log'
        super().__init__()

    def log_entry(self, room_id, pid):
        """ Log in db, that player has joined some room

        Parameters
        ----------
        room_id : int
            Id of the room player has joined
        pid : int
            Id of the player joining the room
        """
        self.insert({'room_id': room_id,
                     'player_id': pid,
                     'entry_date': now(),
                     'leave_date': None})

    def log_leave(self, room_id, pid):
        """ Log in db, that player has left the room he joined previously

        Parameters
        ----------
        room_id : int
            Id of the room the player has left
        pid : int
            Id of the player that has left the room
        """
        last_entry_id = self.find(['id'],
                                  'room_id=%(rid)s AND player_id=%(pid)s',
                                  {'rid': room_id, 'pid': pid},
                                  order_by='entry_date DESC').id

        self.update_by_id({'leave_date': now()}, last_entry_id)


class LoginLogger(TableView):
    """ Class to insert/handle data in 'login_logger' table.
    Responsible for logging player login and logout dates, ips
    """
    def __init__(self):
        self.table_name = 'login_log'
        super().__init__()

    def _log(self, pid, action, ip=None):
        """ Abstract function to be called by 'log_login' or 'log_logout' below

        Parameters
        ----------
        action : str
            Must be 'logout' or 'login'
        """
        self.insert({'player_id': pid,
                     'action': action,
                     'ip': ip,
                     'date': now()})

    def log_login(self, pid):
        """ Log in db, that the player has logged in.
        Should be called upon login.

        Parameters
        ----------
        pid : int
            Id of the player that logged in.
        """
        self._log(pid, 'login', request.remote_addr)

    def log_logout(self, pid):
        """ Log in db, that the player has logged out.
        Should be called upon logout.

        Parameters
        ----------
        pid : int
            Id of the player that logged out.
        """
        self._log(pid, 'logout')
