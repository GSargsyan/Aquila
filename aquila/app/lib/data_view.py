from app import db


class DataView(object):

    #
    # Object initialization
    # Should contain table name assignment (self.table_name = "table")
    #
    # @return object
    #
    def __init__(self):
        self.link = db
        self.joins = []
        self.join_fields = []
        self.result = None

    #
    # Add join to table
    #
    # @param    string    table               name of table to join to
    # @param    string    on                  join condition
    # @param    string    fields              list
    # @param    string    type                join type
    # @return bool
    #
    def join(self, table, on, fields, type='LEFT'):
        self.joins.append(" " . join((type, "JOIN", table, "ON", on)))
        self.join_fields.extend(fields)

    #
    # Clears table joins
    #
    # @return bool
    #
    def clear_joins(self):
        self.joins = []
        self.join_fields = []

    #
    # Clears SQL result object
    #
    # @return bool
    #
    def clear(self):
        if not (self.result is None):
            self.result.close()
            self.result = None
        return True

    #
    # Begins SQL transaction
    #
    # @return nothing
    #
    def begin(self):
        self.link.transaction = True

    #
    # Commits previously begun SQL transaction
    #
    # @return nothing
    #
    def commit(self):
        self.link.commit()

    #
    # Rollback previously begun SQL transaction
    #
    # @return nothing
    #
    def rollback(self):
        self.link.rollback()

    #
    # Locking itself
    #
    # @return query result
    #
    def lock(self):
        return self.link.execute('LOCK TABLE {}'.format(self.table_name))

    #
    # SQL select function
    #
    # @param  string  where     query conditions, eg. id=%(id)s
    # @param  dict    values    dictionary of condition values, eg. {"id": 1}
    # @param  string  group_by  query expression
    # @param  string  order_by  query expression
    # @param  int     limit     limit of query result
    # @throws Exception         on query fail
    # @return object            query result
    #
    def select(self, fields=['*'], where='', values={}, group_by='',
               order_by='', limit=-1, offset=-1, count=False):

        query_tail = []
        if len(group_by) > 0:
            query_tail.append('GROUP BY %s' % group_by)
        if len(order_by) > 0:
            query_tail.append('ORDER BY %s' % order_by)
        if limit > 0:
            query_tail.append('LIMIT %(limit)s')
            values['limit'] = limit
        if offset > 0:
            query_tail.append('OFFSET %(offset)s')
            values['offset'] = offset
        if len(where) == 0:
            where = True

        if count:
            fields += ['count(*) OVER () as all_count']

        query = self.link.select % \
            (", " . join(fields), self.table_name, " " . join(self.joins),
             where, " " . join(query_tail))

        self.result = self.link.execute(query, values)

        return self.result

    #
    # Select first occurrence of record by specified conditions
    #
    # @param  string   where     query conditions, eg. id=%(id)s
    # @param  dict     values    dictionary of condition values, eg. {"id": 1}
    # @param  string   order_by  query expression
    # @return object             database record
    #
    def find(self, fields=['*'], where='', values={}, order_by=''):
        res = self.select(fields, where, values, '', order_by, 1).fetchone()
        self.clear()
        return res

    #
    # SQL insert function
    #
    # @param  dict      values        dictionary of insertion, eg. {"id": 1}
    # @return bool
    #
    def insert(self, values, ret=''):
        field_list = {key: "%%(%s)s" % key for key in values}
        query_tail = ''
        if (len(field_list) == 0):
            return False
        if len(ret) > 0:
            query_tail = 'RETURNING %s' % ret

        query = self.link.insert % \
            (self.table_name, ", " . join(field_list.keys()),
             ", " . join(field_list.values()), query_tail)

        self.result = self.link.execute(query, values)
        if (self.result is None or self.result.rowcount != 1):
            return False
        else:
            res = self.result.fetchone()[0] if query_tail else True
            self.clear()
            return res

    #
    # SQL update function
    #
    # @param  dict    values  dictionary of values to be updated, eg. {"id": 1}
    # @param  string  where   query conditions
    # @return bool
    #
    def update(self, values, where=True, condition={}):
        field_list = ["%s=%%(%s)s" % (key, key) for key in values]
        values = {**values, **condition}

        query = self.link.update % \
            (self.table_name, ", " . join(field_list), where)

        self.result = self.link.execute(query, values)
        if (self.result is None):
            return False
        else:
            self.clear()
            return True

    #
    # SQL update function which can use existing values. eg. a = a + 1
    #
    # @param  dict    values  dictionary of values to be updated, eg. {"id": 1}
    # @param  string  where   query conditions
    #
    def update_by_existing(self, values, where=True, condition={}):
        field_list = ', '.join([k + '=' + v for k, v in values.items()])
        values = {**values, **condition}
        self.link.execute(self.link.update %
                          (self.table_name, field_list, where), values)

    #
    # SQL delete function
    #
    # @param  string    where         query conditions
    # @param  dict      values        dictionary, eg. {"id": 1}
    # @return bool
    #
    def delete(self, where=True, values={}):
        query = self.link.delete % \
            (self.table_name, where)

        self.result = self.link.execute(query, values)
        if (self.result is None) or self.result.rowcount == 0:
            return False
        else:
            count = self.result.rowcount
            self.clear()
            return count

    #
    # Select all records
    #
    # @param  string    where      query conditions, eg. id=%(id)s
    # @param  dict      values     dictionary of condition values
    # @param  string    group_by   query expression
    # @param  string    order_by   query expression
    # @return list                 list of records
    #
    def all(self, fields=['*'], where='', values={},
            group_by='', order_by='', limit=-1, offset=-1):
        all = self.select(fields, where, values, group_by, order_by, limit,
                          offset).fetchall()
        self.clear()
        return all

    #
    # Exception throw function
    #
    # @param    string    message        exception message
    # @throws Exception                    always
    #
    def throw(self, message):
        raise Exception("DB error [%s]" % message)
