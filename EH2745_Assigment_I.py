from Node import Node
from Substation import Substation
from BaseVoltage import BaseVoltage
from VoltageLevel import VoltageLevel
from PowerTransformer import PowerTransformer
from ACLine import ACLine
from Terminal import Terminal
from Equipment import Equipment
from Breaker import Breaker
from GeneratingUnit import GeneratingUnit
from SynchronousMachine import SynchronousMachine
from RegulatingControl import RegulatingControl
from EnergyConsumer import EnergyConsumer
from PowerTransformerEnd import PowerTransformerEnd
from RatioTapChanger import RatioTapChanger
from lxml import etree
from pathlib import Path
from CalculateYBusMatrix import CalculateYBusMatrix


def getInformation():

    data_pathXML = Path(f'./Assignment_EQ_reduced.xml')


    def dens(to_strip, char="}"):
        return str(to_strip).split(char)[-1]


    with open(data_pathXML) as f:
        eq_xml = etree.parse(f)


    rootXML = eq_xml.getroot()
    nsmap = rootXML.nsmap
    REMOVE_NAMESPACE = True

    if REMOVE_NAMESPACE:
        for e in rootXML.xpath("//*", namespaces=nsmap):
            e.tag = dens(e.tag)
            if e.attrib:
                for k in e.attrib.keys():
                    e.attrib[dens(k)] = e.attrib.pop(k)


    # Open SSH file

    data_pathSSH = Path(f'./Assignment_SSH_reduced.xml')


    def dens(to_strip, char="}"):
        return str(to_strip).split(char)[-1]


    with open(data_pathSSH) as f:
        eq_SSH = etree.parse(f)


    rootSSH = eq_SSH.getroot()
    nsmap = rootSSH.nsmap
    REMOVE_NAMESPACE = True

    if REMOVE_NAMESPACE:
        for e in rootSSH.xpath("//*", namespaces=nsmap):
            e.tag = dens(e.tag)
            if e.attrib:
                for k in e.attrib.keys():
                    e.attrib[dens(k)] = e.attrib.pop(k)

    # Base Voltage

    for nnn in rootXML.findall('BaseVoltage'):
        IDBaseV = nnn.get('ID')
        nameBaseV = nnn.find('BaseVoltage.nominalVoltage').text
        baseV = nnn.find('BaseVoltage.nominalVoltage').text
        baseVoltageList.append(BaseVoltage(IDBaseV, nameBaseV, baseV))

    # Substation

    for n in rootXML.findall('Substation'):
        IDSS = n.get('ID')
        nameSS = n.find('IdentifiedObject.shortName').text
        regionSS=n.find('Substation.Region').attrib['resource']
        substationList.append(Substation(IDSS, nameSS, regionSS))

    # Voltage Level

    for nn in rootXML.findall('VoltageLevel'):
        IDVLvl = nn.get('ID')
        nameVLvl = nn.find('IdentifiedObject.name').text
        SSVLvl = nn.find('VoltageLevel.Substation').attrib['resource']
        VoltageVLvl = nn.find('VoltageLevel.BaseVoltage').attrib['resource']
        voltageLevelList.append(VoltageLevel(IDVLvl, nameVLvl, SSVLvl, VoltageVLvl))

    # Generating Unit

    for nn in rootXML.findall('GeneratingUnit'):
        IDGenU = nn.get('ID')
        nameGenU = nn.find('IdentifiedObject.name').text
        maxPGenU = nn.find('GeneratingUnit.maxOperatingP').text
        minPGenU = nn.find('GeneratingUnit.minOperatingP').text
        equipmentGenU = nn.find('Equipment.EquipmentContainer').attrib['resource']
        generatingUnitList.append(GeneratingUnit(IDGenU, nameGenU, maxPGenU, minPGenU, equipmentGenU))

    # print('Generating Unit:')
    # print(GeneratingUnit)

    # Synchronous Machines

    PSynchMach = []
    QSynchMach = []
    xt = 0

    for gg in rootSSH.findall('SynchronousMachine'):
        PSynchMach.append(gg.find('RotatingMachine.p').text)
        QSynchMach.append(gg.find('RotatingMachine.q').text)

    for nn in rootXML.findall('SynchronousMachine'):
        IDSynchMach = nn.get('ID')
        nameSynchMach = nn.find('IdentifiedObject.name').text
        rateSSynchMach = nn.find('RotatingMachine.ratedS').text
        genUnitSynchMach = nn.find('RotatingMachine.GeneratingUnit').attrib['resource']
        regContrSynchMach = nn.find('RegulatingCondEq.RegulatingControl').attrib['resource']
        equipContSynchMach = nn.find('Equipment.EquipmentContainer').attrib['resource']

        for ee in rootXML.findall('VoltageLevel'):
            if ee.get('ID') == equipContSynchMach[1:]:
                baseVolSynchMach = ee.find('VoltageLevel.BaseVoltage').attrib['resource']
                break

        synchronousMachineList.append(SynchronousMachine(IDSynchMach, nameSynchMach,
                                                         rateSSynchMach, PSynchMach,
                                                         QSynchMach, genUnitSynchMach,
                                                         regContrSynchMach, equipContSynchMach,
                                                         baseVolSynchMach))
        xt += 1

        # print('Synchronous Machine:')
        # print(SynchronousMachine)

    # RegulatingControl

    xc = 0
    targetValue = []

    for gg in rootSSH.findall('RegulatingControl'):
        targetValue.append(gg.find('RegulatingControl.targetValue').text)

    for nn in rootXML.findall('RegulatingControl'):
        IDRegCtrl = nn.get('ID')
        nameRegCtrl = nn.find('IdentifiedObject.name').text

        regulatingControlList.append(RegulatingControl(IDRegCtrl, nameRegCtrl, targetValue))
        xc += 1

        # print('Regulating Control:')
        # print(RegulatingControl)

    # Power Transformer

    for nn in rootXML.findall('PowerTransformer'):
        IDPowTrans = nn.get('ID')
        namePowTrans = nn.find('IdentifiedObject.name').text
        equipmentContPowTrans = nn.find('Equipment.EquipmentContainer').attrib['resource']
        powerTransformerList.append(PowerTransformer(IDPowTrans, namePowTrans, equipmentContPowTrans))

    # Energy Consumer

    xd = 0
    PEnergyConsumer = []
    QEnergyConsumer = []

    for gg in rootSSH.findall('EnergyConsumer'):
        PEnergyConsumer.append(gg.find('EnergyConsumer.p').text)
        QEnergyConsumer.append(gg.find('EnergyConsumer.q').text)

    for nn in rootXML.findall('EnergyConsumer'):
        IDEnergyConsumer = nn.get('ID')
        nameEnergyConsumer = nn.find('IdentifiedObject.name').text
        equipEnergyConsumer = nn.find('Equipment.EquipmentContainer').attrib['resource']

        for ee in rootXML.findall('VoltageLevel'):
            if ee.get('ID') == equipEnergyConsumer[1:]:
                baseVolEnergyConsumer = ee.find('VoltageLevel.BaseVoltage').attrib['resource']
                break

        energyConsumerList.append(EnergyConsumer(IDEnergyConsumer, nameEnergyConsumer,
                                                      PEnergyConsumer, QEnergyConsumer,
                                                      equipEnergyConsumer, baseVolEnergyConsumer))
        xd += 1

        # print('Energy Consumer:')
        # print(EnergyConsumer)

    # Power Transformers End

    for nn in rootXML.findall('PowerTransformerEnd'):
        IDPTEnd = nn.get('ID')
        namePTEnd = nn.find('IdentifiedObject.name').text
        rPTEnd = nn.find('PowerTransformerEnd.r').text
        xPTEnd = nn.find('PowerTransformerEnd.x').text
        IDTransformer = nn.find('PowerTransformerEnd.PowerTransformer').attrib['resource']
        baseVolPTEnd = nn.find('TransformerEnd.BaseVoltage').attrib['resource']
        terminalPTEnd = nn.find('TransformerEnd.Terminal').attrib['resource']
        powerTransformer = nn.find('PowerTransformerEnd.PowerTransformer').attrib['resource']

        powerTransformerEndList.append(PowerTransformerEnd(IDPTEnd, namePTEnd, rPTEnd, xPTEnd, IDTransformer,
                                    baseVolPTEnd, terminalPTEnd, powerTransformer))

        #print('Power Transformer End:')
        #print(powerTransformerList)

    # Breaker -> State: is open?

    for nn in rootXML.findall('Breaker'):
        IDBreaker = nn.get('ID')
        nameBreaker = nn.find('IdentifiedObject.name').text
        stateBreaker = nn.find('Switch.normalOpen').text
        equipmentContBreaker = nn.find('Equipment.EquipmentContainer').attrib['resource']

        for ee in rootXML.findall('VoltageLevel'):
            if ee.get('ID') == equipmentContBreaker[1:]:
                baseVolBreak = ee.find('VoltageLevel.BaseVoltage').attrib['resource']
                break

        breakerList.append(Breaker(IDBreaker, nameBreaker, stateBreaker, equipmentContBreaker, baseVolBreak))

        # print('Breaker:')
        # print(breakerList)

    # Ratio Tap Changer

    for nn in rootXML.findall('RatioTapChanger'):
        IDRTC = nn.get('ID')
        nameRTC = nn.find('IdentifiedObject.name').text
        stepRTC = nn.find('TapChanger.normalStep').text

        ratioTapChangerList.append(RatioTapChanger(IDRTC, nameRTC, stepRTC))

        # print('Ratio Tap Changer:')
        # print(ratioTapChangerList)

    # Find resistance (r) and reactance (x) of every AC line

    for n in rootXML.findall('ACLineSegment'):
        IDLine = n.get('ID')
        nameLine = n.find('IdentifiedObject.name').text
        equipmentContLine = n.find('Equipment.EquipmentContainer').attrib['resource']
        rLine = n.find('ACLineSegment.r').text
        xLine = n.find('ACLineSegment.x').text
        bLine = n.find('ACLineSegment.bch').text
        gLine = n.find('ACLineSegment.gch').text
        baseVLine = n.find('ConductingEquipment.BaseVoltage').attrib['resource']
        ACLinesList.append(ACLine(IDLine, nameLine, equipmentContLine, rLine, xLine, bLine, gLine, baseVLine))

    topologyGenerator(rootXML, rootSSH, baseVoltageList, substationList, voltageLevelList,
                      generatingUnitList, regulatingControlList, powerTransformerList,
                      energyConsumerList, powerTransformerEndList, breakerList, ratioTapChangerList,
                      synchronousMachineList, ACLinesList)

    return


def topologyGenerator(rootXML, rootSSH, baseVoltageList, substationList, voltageLevelList,
                      generatingUnitList, regulatingControlList, powerTransformerList,
                      energyConsumerList, powerTransformerEndList, breakerList, ratioTapChangerList,
                      synchronousMachineList, ACLinesList):

    # Initialize variables to use

    nodeNumber = 1
    powerGrid = [Node]
    busbarSectionList = []

    #Find all Coonectivity Nodes

    for n in rootXML.findall('ConnectivityNode'):
        IDCN = n.get('ID')
        nameCN = n.find('IdentifiedObject.name').text
        containerCN = n.find('ConnectivityNode.ConnectivityNodeContainer').attrib['resource']
        powerGrid.append(Node(nodeNumber, IDCN, nameCN, containerCN))
        TNum = 0

        # Find terminals and add them to the CN

        for nn in rootXML.findall('Terminal'):
            CNTerminal = nn.find('Terminal.ConnectivityNode').attrib['resource']
            if CNTerminal[1:] == IDCN:
                IDTerminal = nn.get('ID')
                nameTerminal = nn.find('IdentifiedObject.name').text
                CETerminal = nn.find('Terminal.ConductingEquipment').attrib['resource']
                powerGrid[nodeNumber].addTerminal(Terminal(IDTerminal, nameTerminal, CETerminal, CNTerminal))

                TNum += 1

                # Find the Conducting Equipment and add them to the Terminal
                # First, let's look for bus bars

                for nnn in rootXML.findall('BusbarSection'):
                    IDBB = nnn.get('ID')
                    if IDBB == CETerminal[1:]:
                        nameBB = nnn.find('IdentifiedObject.name').text
                        equipmentContBB = nnn.find('Equipment.EquipmentContainer').attrib['resource']
                        busbarSectionList.append(Equipment(IDBB, nameBB, equipmentContBB))
                        powerGrid[nodeNumber].terminalList[TNum].addCE(Equipment(IDBB, nameBB, equipmentContBB))

                # Now, let's find the Power Transformers

                pos = 0

                for _ in powerTransformerList:
                    IDPowTrans = powerTransformerList[pos].IDPowTrans
                    if IDPowTrans == CETerminal[1:]:
                        powerGrid[nodeNumber].terminalList[TNum].addCE(powerTransformerList[pos])
                    pos += 1

                # Now, let's find the Breakers

                pos = 0

                for _ in breakerList:
                    IDBreaker = breakerList[pos].IDBreaker
                    if IDBreaker == CETerminal[1:]:
                        powerGrid[nodeNumber].terminalList[TNum].addCE(breakerList[pos])
                    pos += 1

                # Now, let's find the Generation Units

                pos = 0

                for _ in generatingUnitList:
                    IDGenUnit = generatingUnitList[pos].IDGenUnit
                    if IDGenUnit == CETerminal[1:]:
                        powerGrid[nodeNumber].terminalList[TNum].addCE(generatingUnitList[pos])
                    pos += 1

                # Now, let's find the Regulating Units

                pos = 0

                for _ in regulatingControlList:
                    IDRegCtrl = regulatingControlList[pos].IDRegCtrl
                    if IDRegCtrl == CETerminal[1:]:
                        powerGrid[nodeNumber].terminalList[TNum].addCE(regulatingControlList[pos])
                    pos += 1

                # Are you not getting bored? We find the loads

                pos = 0

                for _ in energyConsumerList:
                    IDEnergyConsumer = energyConsumerList[pos].IDEnergyConsumer
                    if IDEnergyConsumer == CETerminal[1:]:
                        powerGrid[nodeNumber].terminalList[TNum].addCE(IDEnergyConsumer[pos])
                    pos += 1

                # Now, we find the Synchronous Machine

                pos = 0

                for _ in synchronousMachineList:
                    IDSynchMach = synchronousMachineList[pos].IDSynchMach
                    if IDSynchMach == CETerminal[1:]:
                        powerGrid[nodeNumber].terminalList[TNum].addCE(synchronousMachineList[pos])
                    pos += 1

                # Almost finally... the Power Transformers End

                pos = 0

                for _ in powerTransformerEndList:
                    IDPTEnd = powerTransformerEndList[pos].IDPTEnd
                    if IDPTEnd == CETerminal[1:]:
                        powerGrid[nodeNumber].terminalList[TNum].addCE(powerTransformerEndList[pos])
                    pos += 1

                # Finally, the AC Lines

                pos = 0

                for _ in ACLinesList:
                    IDLine = ACLinesList[pos].IDLine
                    if IDLine == CETerminal[1:]:
                        powerGrid[nodeNumber].terminalList[TNum].addCE(ACLinesList[pos])
                    pos += 1

        nodeNumber += 1

    # GraphMyPowerGrid
    yBusMtx = CalculateYBusMatrix(voltageLevelList, busbarSectionList, powerTransformerEndList, powerTransformerList,
                        baseVoltageList, ACLinesList, energyConsumerList)

    for element in yBusMtx:
        if element != 0:
            print(element)

    print()
    print("All other elements are cero")


# Initialize variables to be used ("in memory")


data_pathXML = Path(f'./Assignment_EQ_reduced.xml')


baseVoltageList = []
substationList = []
voltageLevelList = []
generatingUnitList = []
synchronousMachineList = []
regulatingControlList = []
powerTransformerList = []
energyConsumerList = []
powerTransformerEndList = []
breakerList = []
ratioTapChangerList = []
ACLinesList = []


getInformation()


