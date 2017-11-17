
class Sector(object):
    def __init__(self, sector_id, enodeb_id, tac, lon, lat, u, paging):
        self.sector_id = sector_id
        self.enodeb_id = enodeb_id
        self.tac = tac
        self.lon = lon
        self.lat = lat
        self.u = u
        self.paging = paging

    def __repr__(self):
        return "{},{},{},{},{},{},{}\n".format(self.sector_id, self.enodeb_id, self.tac, self.lon, self.lat, self.u, self.paging)

    def __str__(self):
        return "{},{},{},{},{},{},{}\n".format(self.sector_id, self.enodeb_id, self.tac, self.lon, self.lat, self.u, self.paging)