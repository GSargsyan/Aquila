import geocoder

from app.lib.table_view import TableView


class Countries(TableView):
    def __init__(self):
        self.table_name = 'countries'

    def iso2_from_ip(self, ip):
        """ Convert IPv4 to country code

        Returns
        -------
        str
            ISO-2 code of the country
        """
        return geocoder.ip(ip).country
