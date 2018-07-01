import geocoder


class Countries:
    def name_to_id(self, country):
        pass

    def from_ip(self, ip):
        info = geocoder.freegeoip(ip)
        return None
