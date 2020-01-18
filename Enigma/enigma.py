import string
from . import models as md

class Rotor:
    """
    Engima Rotor Class - V.1.0
    Author Joshua Colletta
    """
    def __init__(self, mappinglist, offset, ID, notch, turnoverpos):
        """
        Constructor for Rotor
        :param mappinglist: The Rotors internal wiring, represented as a list of chars making a 1-1 mapping
        :param offset: Offset for the rotor (Part of Settings)
        :param ID: Internal ID, this is the location of the rotor in the rotor assembley
        :param notch: Position of spring loaded mechanism in the rotor
        :param turnoverpos: Position that causes next rotor to advance
        """
        self.mappinglistIN = []
        self.notch = notch
        self.turnoverpos = turnoverpos
        self.positionlist = []
        self.offset = offset
        self.position = 0
        self.ID = ID
        if len(mappinglist) == 26:
            mappinglist = md.toMyList(mappinglist)
            for entry in mappinglist:
                self.positionlist.append(mappinglist.index(entry))
                self.mappinglistIN.append(string.ascii_uppercase.index(entry.upper()) % 26)
        print(offset)
        self.stepOuter(offset)

    def getindx(self, inputIndex, forward=True, debugging=False):
        """
        Resolve the output pin given an input pin and a direction
        :param inputIndex: Input signal pin number
        :param forward: Boolean value for programming direction of mapping
        :param debugging: Boolean, value for setting debugging output (shows every internal step)
        :return: returns the output index of the current rotor
        """
        if forward:
            output = self.positionlist.index(self.mappinglistIN[inputIndex])
        else:
            output = self.mappinglistIN.index(self.positionlist[inputIndex])
        if debugging == True:
            print("Rotor:", self.ID, "is in position", self.position, "Input:", inputIndex, "output:", output)
            print(self.positionlist)
            print(self.mappinglistIN)
            print('\n')
        return output

    def stepinc(self):
        """
        Steps the whole rotor (inner and outer)
        :return: None (OOP)
        """
        self.position += 1
        self.positionlist = self.positionlist[1:] + self.positionlist[:1]
        self.mappinglistIN = self.mappinglistIN[1:] + self.mappinglistIN[:1]

    def stepOuter(self, x):
        """
        Steps the outer ring of the rotor
        :param x: Number of steps
        :return: None (OOP)
        """
        if int(x) >= 1:
            for i in range(int(x)):
                self.positionlist = self.positionlist[1:] + self.positionlist[:1]

    def clock(self):
        """
        Compares top rotor char with turnover char
        :return: True if the current rotor is in its turnover position
        """
        if self.turnoverpos == string.ascii_uppercase[self.positionlist[0]]:
            self.position = 0
            return True

    #getters/setters
    def getStep(self):
        return self.position

class plugboard:
    """
    Enigma Plugboard Class - V.1.0
    Author Joshua Colletta
    """
    def __init__(self, pluglist):
        """
        Plugboard Constructor
        :param pluglist: List of plugboard connections
        """
        if len(pluglist) <= 13:
            pluglistSanFlag = True
            for entry in pluglist:
                if entry[0] == entry[1]:
                    # No plug onto itself
                    pluglistSanFlag = False
            if pluglistSanFlag is True:
                self.pluglist = pluglist
            else:
                print("Error in Pluglist Data")


    def getChar(self, inputChar):
        """
        Return the plugboard output for any letter, handles no plugs and letter not plugged in also
        :param inputChar: Any standard Char
        :return: The result of the plugboard for this character
        """
        if len(self.pluglist) is not 0:
            for i in range(len(self.pluglist)):
                if self.pluglist[i][0] is inputChar:
                    return self.pluglist[i][1]
                if self.pluglist[i][1] is inputChar:
                    return self.pluglist[i][0]
            return inputChar
        else:
            return inputChar


class rotorAssembley:
    """
    Enigma Rotor Assembley Class - V.1.1 - Super Class of Rotor
    Author Joshua Colletta
    """
    def __init__(self, rotorlist, reflectorlist, offsetlist):
        """
        Rotor Assembley Constructor
        :param rotorlist: List of Rotors (RAW)
        :param reflectorlist: list of Reflectors (RAW)
        :param offsetlist: list of Rotor offsets (RAW)
        """
        self.rotorlist = []
        counter = 0
        for rotordata in rotorlist:
            self.rotorlist.append(Rotor(rotordata[0], offsetlist[rotorlist.index(rotordata)], counter, rotordata[1], rotordata[2]))
            counter += 1
        if len(reflectorlist) == 13:
            # simulate the reflector as a fully populated plugboard object
            self.reflector = plugboard(reflectorlist)

    def Rotors(self, inputindex, debugging, forward=True):
        """
        Helper function of Rotor Assembley - calculates the output pin the rotors in a given direction
        :param inputindex: Input pin in rotor Ass
        :param debugging: Debugging option passed down to Rotor Object, obtained from enigma object
        :param forward: Direction boolean
        :return: The output pin of the rotor Ass
        """
        for Rotor in self.rotorlist:
            inputindex = Rotor.getindx(inputindex, forward, debugging)
        return inputindex

    def stepRotor(self):
        """
        Steps the rotor ass by iterating the rotorlist - DOUBLE STEP
        :return:
        """
        for Rotor in self.rotorlist:
            nextStep = Rotor.clock()
            if Rotor.ID == 0:
                Rotor.stepinc()
            elif nextStep is True:
                self.rotorlist[self.rotorlist.index(Rotor) + 1].stepinc()

    def rotorAss(self, inputChar, debugging):
        """
        enciphers a given char through the entire rotor ass including reflector (This is essentially a enigma machine without the plugboard)
        :param inputChar: Input Character
        :param debugging: Debugging option passed down from Enigma
        :return: The output pin of the rotor ass
        """
        if debugging:
            print("Input Char:", inputChar)
        inputPin = string.ascii_uppercase.index(inputChar.upper())
        UKWIN = self.Rotors(inputPin, debugging)
        outputPin = string.ascii_uppercase[UKWIN]
        UKWOUT = self.reflector.getChar(outputPin)
        if debugging:
            print("UKW Reads:", UKWOUT)
        self.rotorlist.reverse()
        refinputPin = string.ascii_uppercase.index(UKWOUT.upper())
        rotorAssOUT = self.Rotors(refinputPin, debugging, False)
        if debugging:
            print("Output Char:", rotorAssOUT, '\n')
        self.rotorlist.reverse()
        return rotorAssOUT


class enigma:
    """
    Enigma Core Class - V.1.2
    Author Joshua Colletta
    """

    def __init__(self, plugList, rotorList, reflectorList, offsetlist):
        """
        Enigma Constructor
        :param plugList: List of plugboard connections
        :param rotorList: List of Rotors (RAW)
        :param reflectorList: List of Reflectors (RAW)
        :param offsetlist: List of Rotor Offsets (RAW)
        """
        self.pluglist = plugList
        self.rotorlist = rotorList
        self.reflectorlist = reflectorList
        self.plugboard = plugboard(plugList)
        self.rotorassembley = rotorAssembley(self.rotorlist, self.reflectorlist, offsetlist)


    def enchipherMessage(self, String,debugging=False):
        """
        Enciphers a message
        :param String: Input Message
        :param debugging: Debugging output option
        :return: A list of enciphered chars
        """
        outputlist = []
        for letter in String:
            self.rotorassembley.stepRotor()
            letter1 = self.rotorassembley.rotorAss(letter, debugging)
            outputlist.append(string.ascii_uppercase[letter1])
        return outputlist

    def messageSettings(self, settings):
        """
        Enigma Helper Function - Imports Message Settings
        :param settings: Message Setting list returned from forms.py
        :return: None (OOP)
        """
        for i in range(0, len(settings)):
            for j in range(0, string.ascii_uppercase.index(settings[i])):
                print("Rotating Rotor: ", self.rotorassembley.rotorlist[i].ID)
                self.rotorassembley.rotorlist[i].stepinc()







