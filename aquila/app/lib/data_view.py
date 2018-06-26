import json
from app import db


class DataView(object):

    #
    # Object initialization
    # Should contain table name assignment (self.table_name = "table")
    # Should contain declaration of table's fields (self.fields = {})
    # {"id": {"rdonly": True, "alias": "number", "json": False}}
    #
    # @return object
    #
    def __init__(self):
        self.link = db
        self.joins = []
        self.join_fields = []
        self.result = None
        # Define table name [self.table_name]

        # set default options to the fields if options are None
        for key in self.fields:
            if self.fields[key] is None:
                self.fields[key] = {}

        self.attr_list = list(map(self.__get_attr_list, self.fields))

    def __get_attr_list(self, key):
        if "alias" in self.fields[key]:
            return "%s.%s AS %s" % \
                (self.table_name, key, self.fields[key]["alias"])
        else:
            return "%s.%s" % (self.table_name, key)

    def __encode_objects(self, key, value):
        # two ways from here: either json dumps you, either you're going back
        # with empty hands
        if "json" in self.fields[key] and self.fields[key]["json"]:
            return json.dumps(value)
        else:
            return value

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
    def select(self, where='', values={}, group_by='', order_by='', limit=-1,
               offset=-1, count=False):

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

        fields = self.attr_list + self.join_fields

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
    def find(self, where='', values={}, order_by=''):
        res = self.select(where, values, '', order_by, 1).fetchone()
        self.clear()
        return res

    #
    # SQL insert function
    #
    # @param  dict      values        dictionary of insertion, eg. {"id": 1}
    # @return bool
    #
    def insert(self, values, ret=''):
        values = {key: self.__encode_objects(key, values[key])
                  for key in values if key in self.fields}
        field_list = {key: "%%(%s)s" % key
                      for key in values if key in self.fields and
                      self.fields[key].get("rdonly", False) is False}
        query_tail = ''
        if (len(field_list) == 0):
            return False
        if len(ret) > 0 and ret in self.fields:
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
        values = {key: self.__encode_objects(key, values[key])
                  for key in values if key in self.fields}
        field_list = ["%s=%%(%s)s" % (key, key)
                      for key in values if key in self.fields and
                      self.fields[key].get("rdonly", False) is False]
        if (len(field_list) == 0):
            return False
        values = dict(list(values.items()) + list(condition.items()))

        query = self.link.update % \
            (self.table_name, ", " . join(field_list), where)

        self.result = self.link.execute(query, values)
        if (self.result is None):
            return False
        else:
            self.clear()
            return True

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
    # @param  dict      values     dictionary of condition values, eg. {"id": 1}
    # @param  string    group_by   query expression
    # @param  string    order_by   query expression
    # @return list                 list of records
    #
    def all(self, where='', values={}, group_by='', order_by='', limit=-1,
            offset=-1):
        all = self.select(where, values, group_by, order_by, limit,
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

    def create_table(self, name, fields, indexes={}):
        if len(fields) == 0:
            return False

        # itarate through fields
        ps = []
        for field in fields:
            ps.append(self._field_sql(field))

        # itarate through indexes
        for index in indexes:
            ps.append(self._index_sql(index))

        # itarate through indexes
        q = 'CREATE TABLE {} ({})'.format(name, ','. join(ps))
        return self.link.execute(q)

    def alter_table(self, name, fields, type: str=None):
        if len(fields) == 0:
            return False

        q = 'ALTER TABLE {} {} {}'
        if len(fields) == 1:
            self.link.execute(q . format(name, 'ADD COLUMN',
                                         self._field_sql(fields[0])))
        elif len(fields) == 2:
            if fields[0] != fields[1]:
                self.link.execute(q . format(
                    name, 'RENAME COLUMN',
                    '{} TO {}'.format(fields[0], fields[1])))
            if type:
                self.link.execute(q . format(
                    name, 'ALTER COLUMN',
                    '{0} TYPE {1} USING ({0}::{1})'.format(fields[1], type)))

    def rename_table(self, name, new_name):
        return self.link.execute('ALTER TABLE %s RENAME TO %s' % (name,
                                                                  new_name))

    def drop(self, table, field=None):
        if field is None:
            return self.link.execute('DROP TABLE %s CASCADE' % table)
        else:
            return self.link.execute(
                'ALTER TABLE %s DROP COLUMN %s' % (table, field))

    def _field_sql(self, field_def):
        # name:type:not_null:ai
        # first_name:varchar(100):1

        _def = field_def.split(':')
        return '{} {} {} {}'. format(
            _def[0], _def[1], 'NOT NULL' if _def[2] == '1' else '',
            'DEFAULT {}'. format(_def[3]) if len(_def) > 3 else '')

    def _index_sql(self, index_def):
        # name:type
        _def = index_def.split(':')
        return ' {} KEY ({})'. format(_def[1], _def[0])

    def create_trigger(self, trigger_name: str, table_name: str,
                       function_name: str, when: str, events: list,
                       each: str=None, condition: str=None, arguments: list={}):

        self.link.execute(
            "CREATE TRIGGER {} {} {} ON {} {} {} EXECUTE PROCEDURE \
            {}({})".format(trigger_name, when, ' OR '. join(events), table_name,
                           'FOR EACH {}'. format(each) if each else '',
                           'WHEN ({})'. format(condition) if condition else '',
                           function_name,
                           ', '. join(arguments) if len(arguments) > 0 else ''))
