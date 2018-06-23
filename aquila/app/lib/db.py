import psycopg2
import psycopg2.extras


class DB():
    def __init__(self, host, user, pwd, dbname):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.dbname = dbname
        self.conn_str = "dbname='{}' user='{}' host='{}' password='{}'".format(
                self.dbname, self.user, self.host, self.pwd)
        self.conn = psycopg2.connect(self.conn_str)

    def reconnect(self):
        self.conn.close()
        self.conn = psycopg2.connect(conn_str)

    def execute(self, query, args=''):
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.cur.execute(query, args)
        self.conn.commit()
        return self.cur

    def select(self, table, fields=['*'], joins=[], where='',
                group_by='', order_by='', limit=0, offset=''):
        tail = ''
        if group_by != '':
            tail += "GROUP BY {}".format(group_by)
        if order_by != '':
            tail += "ORDER BY {}".format(order_by)
        if limit != 0:
            tail += "LIMIT {}".format(limit)
        if offset != '':
            tail += "OFFSET {}".format(offset)

        query = "SELECT {} FROM {} {} WHERE {} {}"\
                .format(",".join(fields), table, " ".join(joins),
                        where if where else '1', tail)

        result = self.execute(query).fetchall()
        if result is None:
            return None
        return result

    def insert(self, table, fields, values, ret=None):
        query = "INSERT INTO {} ({}) VALUES %s{}".format(
                table, ", ".join(fields),
                " RETURNING " + ret if ret is not None else "")
        return self.execute(query, (values,)).fetchone()[0]

    def update(self, table, changes, where=''):
        query = "UPDATE {} SET {} WHERE {}".format(
                table, ', '.join(["{}={}".format(k, v)
                                  for k, v in changes.items()]),
                where if where else '1')

        self.execute(query)
