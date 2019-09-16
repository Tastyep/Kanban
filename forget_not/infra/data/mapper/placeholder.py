class AnonPlaceHolder(object):
    def __init__(self, count=1):
        self.v = list("?" * count)

    def __repr__(self):
        return ",".join(self.v)


class PlaceHolder(object):
    def __init__(self, tag):
        self.v = ":" + tag

    def __repr__(self):
        return self.v
