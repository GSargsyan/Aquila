from app.lib.data_view import DataView


class TableView(DataView):
    def __init__(self):
        self.PAGE_SIZE = 10
        super(TableView, self).__init__()

    def find_by_field(self, field, value, op='=', fields=['*']):
        return self.find(fields, '{}.{} {} %(value)s'.format(
            self.table_name, field, op), {'value': value})

    def all_by_field(self, field, value, op='=', fields=['*'], order_by=''):
        return self.all(fields, field + op + '%(value)s', {'value': value},
                        order_by=order_by)

    def find_by_id(self, item_id, fields=['*']):
        return self.find_by_field('id', item_id, fields=fields)

    def delete_by_id(self, item_id):
        return self.delete('id=%(item_id)s', {'item_id': item_id})

    def update_by_id(self, values, item_id):
        return self.update(values, 'id=%(item_id)s', {'item_id': item_id})

    def select_page(self, fields=['*'], where='', values={}, group_by='',
                    order_by='', limit=10, page=1, count=False):

        return self.select(fields, where, values, group_by, order_by, limit,
                           (int(page) - 1) * int(limit), count=count)
