class CorrectionObject:
    id_d = ''
    ideal_seconds = 30
    devEui = ''

    def __init__(self, id_d, devEui):
        self.id_d = id_d
        self.devEui = devEui
    
    def getId(self):
        return self.id_d


