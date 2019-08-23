class Zones:

    def __init__(self, busbarSectionList, voltageLevelList, baseVoltageList,
                 powerTransformerEndList, powerTransformerList, ACLinesList):

        self.busBar = busbarSectionList
        self.voltageLvl = voltageLevelList
        self.baseVoltage = baseVoltageList
        self.pTEnd = powerTransformerEndList
        self.PT = powerTransformerList
        self.ACLines = ACLinesList