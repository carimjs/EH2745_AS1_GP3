from Zones import Zones


def CalculateYBusMatrix(powerGrid, voltageLevelList, busbarSectionList, powerTransformerEndList, powerTransformerList,
                        baseVoltageList, ACLinesList):
    # First, we look for the Busbar sections

    zonesList = []
    posBB = 0

    for _ in busbarSectionList:
        busBarEC = busbarSectionList[posBB].equipmentContBB
        # print(busbarSectionList[posBB].nameBB)

        # We look for the base voltage of the busbar

        posVL = 0

        for _ in voltageLevelList:
            if voltageLevelList[posVL].IDVLvl == busBarEC[1:]:
                # print(voltageLevelList[posVL].nameBaseV)
                # Now, we look for the base voltage
                posBL = 0
                for _ in baseVoltageList:
                    if voltageLevelList[posVL].VoltageVLvl[1:] == baseVoltageList[posBL].IDBaseV:
                        # print(baseVoltageList[posBL].nameBaseV)

                        # Now, let's look for the Power Transformer End
                        posPTE = 0
                        for _ in powerTransformerEndList:
                            if powerTransformerEndList[posPTE].baseVolPTEnd[1:] == baseVoltageList[posBL].IDBaseV:

                                # Next, find the transformer
                                posPT = 0
                                for _ in powerTransformerList:
                                    if powerTransformerList[posPT].IDPowTrans == powerTransformerEndList[
                                                                                     posPTE].powerTransformer[1:]:
                                        # print(powerTransformerList[posPT].namePowTrans)

                                        # Find the AC Lines
                                        posLine = 0
                                        actualLine = []
                                        for _ in ACLinesList:
                                            if ACLinesList[posLine].baseVLine[1:] == baseVoltageList[posBL].IDBaseV:
                                                actualLine = ACLinesList[posLine]
                                            posLine += 1

                                        zonesList.append(Zones(busbarSectionList[posBB], voltageLevelList[posVL],
                                                               baseVoltageList[posBL],
                                                               powerTransformerEndList[posPTE],
                                                               powerTransformerList[posPT], actualLine))

                                    posPT += 1
                            posPTE += 1
                    posBL += 1
            posVL += 1
        posBB += 1

    reduceZones(zonesList)
    # calculateYBus(zonesList)

"""
Reduce reduceZones function, locates which elements has values of interest for the calculation of the Y-Bus matrix
this means, that there are some buses that have several transformers but they don't have value for tranformer or line
because the adjacent buses do, ie, bus 6. 
Please note this function is done after the grid topology is built.
"""

def reduceZones(zonesList):
    tempZones = zonesList.copy()
    newZones = []

    for zone in zonesList:
        for newZ in newZones:
            if zone.busBar.nameBB == newZ.busBar.nameBB:
                if float(newZ.pTEnd.rPTEnd) <= float(zone.pTEnd.rPTEnd):
                    newZones.remove(newZ)
        newZones.append(zone)

    calculateYBus(newZones)


def calculateYBus(zones):
    line = 1
    rL = 0
    xL = 0
    gL = 0
    bL = 0
    rT = 0
    xT = 0

    Zline = 0
    Yline = 0
    Ztrafo = 0

    Y_outdiag = 0
    i = 0
    j = 0
    Y_ = 0

    # we will extract the voltage of every bus bar section
    # the following list includes the voltages of each bus bar
    Voltagelevel = [380, 225, 225, 10.5, 110]

    # we will define a S base for the whole system, which will be equal to 100 MVA
    S_base = 100

    # Then we will proceed to calculate the base impedance as well as the base admittance
    Z_base = []
    Y_base = []

    for yu in Voltagelevel:
        Z_base.append(yu * yu / S_base)
        Y_base.append(S_base / (yu * yu))

    for zoneA in zones:
        for zoneB in zones:
            if i == j:

                Ztd = 0
                Ltd = 0

                if zoneA.ACLines:
                    rL = float(zoneA.ACLines.rLine)
                    xL = float(zoneA.ACLines.xLine)
                    gL = float(zoneA.ACLines.gLine)
                    bL = float(zoneA.ACLines.bLine)
                    Zline = complex(rL, xL)
                    Yline = complex(gL, bL)

                    try:
                        Ltd = (1 / (Zline / Z_base[i])) + 0.5 * (Yline / Yline[i])
                    except:
                        Ltd = 0

                if zoneA.pTEnd:
                    rT = float(zoneA.pTEnd.rPTEnd)
                    xT = float(zoneA.pTEnd.xPTEnd)

                    Ztrafo = complex(rT, xT)
                    try:
                        Ztd = (1 / (Ztrafo / Z_base[i]))

                    except:
                        Ztd = 0

                try:
                    Y_ = Ltd + Ztd

                    if Y_ == 0:
                        Y_ = Ylast

                    else:
                        Ylast = Y_

                    print('Element Y' + str(i) + str(j) + ' is a Diagonal element' + ' = ' + str(Y_))


                except ZeroDivisionError:
                    pass



            else:
                if zoneA.ACLines:
                    if zoneB.ACLines:
                        if zoneA.ACLines.baseVLine == zoneB.ACLines.baseVLine:

                            rL = float(zoneA.ACLines.rLine)
                            xL = float(zoneA.ACLines.xLine)
                            gL = float(zoneA.ACLines.gLine)
                            bL = float(zoneA.ACLines.bLine)
                            line = 0

                            Zline = complex(rL, xL);

                            try:
                                Y_outdiag = (1 / (Zline / Z_base[i]))

                                print('Element Y' + str(i) + str(j) + " = nonZeroElement" + ' = ' + str(Y_outdiag))

                            except ZeroDivisionError:
                                print('Element Y' + str(i) + str(j) + ' = 0')

                if zoneA.PT and line:
                    if zoneB.PT:
                        if zoneA.PT.IDPowTrans == zoneB.PT.IDPowTrans:
                            rT = float(zoneA.pTEnd.rPTEnd)
                            xT = float(zoneA.pTEnd.xPTEnd)

                            Ztrafo = complex(rT, xT);

                            try:
                                Y_outdiag = (1 / (Ztrafo / Z_base[i]))
                                print('Element Y' + str(i) + str(j) + " = nonZeroElement" + ' = ' + str(Y_outdiag))

                            except ZeroDivisionError:
                                print('Element Y' + str(i) + str(j) + ' = 0')

                        else:
                            print('Element Y' + str(i) + str(j) + " = 0")
            j += 1
            line = 1
        i += 1
        j = 0
    i = 0
    j = 0
