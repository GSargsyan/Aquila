import geocoder

from app.lib.table_view import TableView


class Countries(TableView):
    def __init__(self):
        self.table_name = 'countries'

    def iso2_from_ip(self, ip):
        return geocoder.ip(ip).country
