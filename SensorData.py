class SensorDataObject:
    time_data = ""
    deveui = ""
    FPort = -1
    FCntUp = -1
    ADRbit = -1
    MType = -1
    FCntDn = -1
    payload_hex = ""
    payload_ascii = ""
    mic_hex = ""
    Lrcid = ""
    LrrRSSI = 9999999.9
    LrrSNR = 9999999.9
    SpFact = -1
    SubBand = ""
    Channel = ""
    DevLrrCnt = 999999
    Lrrid = ""
    Late = -1
    LrrLAT = 9999999.9
    LrrLON = 9999999.9
    CustomerID = -1
    CustomerDataALRPRO = ""
    ModelCfg = -1
    InstantPER = -1
    MeanPER = -1
    DevAddr = ""

    def __init__(self, time_data, deveui, FPort, FCntUp, ADRbit, MType, FCntDn, payload_hex, payload_ascii, mic_hex, Lrcid, LrrRSSI, LrrSNR, SpFact,
                 SubBand, Channel, DevLrrCnt, Lrrid, Late, LrrLAT, LrrLON, CustomerID, CustomerDataALRPRO, ModelCfg, InstantPER, MeanPER, DevAddr ):
        self.time_data = time_data
        self.deveui = deveui
        self.FPort = FPort
        self.FCntUp = FCntUp
        self.ADRbit = ADRbit
        self.MType = MType
        self.FCntDn = FCntDn
        self.payload_hex = payload_hex
        self.payload_ascii = payload_ascii
        self.mic_hex = mic_hex
        self.Lrcid = Lrcid
        self.LrrRSSI = LrrRSSI
        self.LrrSNR = LrrSNR
        self.SpFact = SpFact
        self.SubBand = SubBand
        self.Channel = Channel
        self.DevLrrCnt = DevLrrCnt
        self.Lrrid = Lrrid
        self.Late = Late
        self.LrrLAT = LrrLAT
        self.LrrLON = LrrLON
        self.CustomerID = CustomerID
        self.CustomerDataALRPRO = CustomerDataALRPRO
        self.ModelCfg = ModelCfg
        self.InstantPER = InstantPER
        self.MeanPER = MeanPER
        self.DevAddr = DevAddr

    def generateString(self):
        sql = 'INSERT INTO sensorschema.uplink_table (time_data, deveui, FPort, FCntUp, ADRbit, MType, FCntDn, ' \
              'payload_hex, payload_ascii, mic_hex, Lrcid, LrrRSSI, LrrSNR, SpFact, SubBand, Channel, ' \
              'DevLrrCnt, Lrrid, Late, LrrLAT, LrrLON, CustomerID, CustomerDataALRPRO, ModelCfg, InstantPER, MeanPER, DevAddr ) ' \
              'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
        return sql

    def generateValues(self):
        return (self.time_data, self.deveui, self.FPort, self.FCntUp, self.ADRbit, self.MType, self.FCntDn, self.payload_hex,
                self.payload_ascii, self.mic_hex, self.Lrcid, self.LrrRSSI,self.LrrSNR, self.SpFact,
                self.SubBand, self.Channel, self.DevLrrCnt, self.Lrrid, self.Late, self.LrrLAT, self.LrrLON, self.CustomerID,
                self.CustomerDataALRPRO, self.ModelCfg, self.InstantPER, self.MeanPER, self.DevAddr)





















