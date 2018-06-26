import psycopg2
import psycopg2.extras


class DB(object):
    insert = "INSERT INTO %s(%s) VALUES (%s) %s"
    update = "UPDATE %s SET %s WHERE %s"
    select = "SELECT %s FROM %s %s WHERE %s %s"
    select_count = "SELECT SUM(src.count) as count FROM (%s) as src"
    delete = "DELETE FROM %s WHERE %s"

    def __init__(self, host, user, pwd, dbname):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.dbname = dbname
        self.transaction = False
        self.conn = psycopg2.connect(
            "dbname='{}' user='{}' host='{}' password='{}'".format(
                self.dbname, self.user, self.host, self.pwd))

        super().__init__()

    def reconnect(self):
        self.conn.close()
        self.conn = psycopg2.connect(
            "dbname='{}' user='{}' host='{}' password='{}'".format(
                self.dbname, self.user, self.host, self.pwd))

    def execute(self, query, args={}):
        if self.conn.closed != 0:
            self.reconnect()

        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

        try:
            cur.execute(query, args)
            if not self.transaction:
                self.conn.commit()
        except Exception as ex:
            self.conn.rollback()
            raise ex
        return cur

    def commit(self):
        if self.transaction:
            self.conn.commit()
            self.transaction = False

    def rollback(self):
        self.conn.rollback()
        self.transaction = False
