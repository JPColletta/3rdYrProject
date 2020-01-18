from django.db import models
import string

class presetModel(models.Model):
    name = models.CharField(max_length=8)
    initvec = models.CharField(max_length=26)
    class meta():
        db_table = 'preset_table'


class rotorModel(models.Model):
    data = models.ForeignKey(presetModel, on_delete=models.CASCADE)
    char_map = models.CharField(max_length=26)
    turnoverPos = models.CharField(max_length=4)
    notchPos = models.CharField(max_length=4)
    name = models.CharField(max_length=8)
    preset = models.CharField(max_length=16)
    class meta():
        db_table = 'rotor_table'

class reflectorModel(models.Model):
    data = models.ForeignKey(presetModel, on_delete=models.CASCADE)
    char_map = models.CharField(max_length=26)
    name = models.CharField(max_length=8)
    preset = models.CharField(max_length=16)
    class meta():
        db_table = 'reflector_table'


def getEnigmaFormLists(presetBool='None'):
    rotornames, reflectornames = [], []
    presets = presetModel.objects.all()
    for preset in presets:
        if preset.name == presetBool:
            rotors = rotorModel.objects.filter(data=preset.id)
            reflectors = reflectorModel.objects.filter(data=preset.id)
            for rotor in rotors:
                rotornames.append(rotor.name)
            for reflector in reflectors:
                reflectornames.append(reflector.name)
    if presetBool == 'None':
        rotors = rotorModel.objects.all()
        reflectors = reflectorModel.objects.all()
        for rotor in rotors:
            rotornames.append(rotor.name)
        for reflector in reflectors:
            reflectornames.append(reflector.name)
    indexList = [x for x in range(0, 26)]
    alphList = [string.ascii_uppercase[x] for x in range(0, 26)]
    return toChoice(rotornames), toChoice(reflectornames), toChoice(indexList), toChoice(alphList)

def getPresets():
    presetNames = ['None']
    presets = presetModel.objects.all()
    for preset in presets:
        presetNames.append(preset.name)

    return toChoice(presetNames)

def chooseReflectors(importedSettings):
    reflector = reflectorModel.objects.filter(name=importedSettings[0])
    for ref in reflector:
        return importReflector(ref.char_map)


def chooseRotors(importedSettings):
    rotorlist = []
    rotorChoice = [importedSettings[1][0], importedSettings[1][1], importedSettings[1][2]]
    for rotor in rotorChoice:
        targetRotors = rotorModel.objects.filter(name=rotor)
        for targetRotor in targetRotors:
            rotorlist.append([targetRotor.char_map, targetRotor.notchPos, targetRotor.turnoverPos, targetRotor.name])
    return rotorlist


def importReflector(reflectorRAW):
    outputlistRAW = []
    outputlist = []
    visited = set()
    alphList = [string.ascii_uppercase[x] for x in range(0, 26)]
    for letter in reflectorRAW:
        outputlistRAW.append([alphList[reflectorRAW.index(letter)], letter])
    for a, b in outputlistRAW:
        if not b in visited:
            visited.add(a)
            outputlist.append([a, b])
    return outputlist


def toChoice(list):
    outputlist = []
    for entry in list:
        if entry is not '\'' or ',':
            outputlist.append((entry, entry))
    return outputlist


def toList(Choices):
    outputlist = []
    for entry in Choices:
        outputlist.append(entry[0])
    return outputlist


def toMyList(stringList):
    # Config imported from string, need to convert '[abc]' to ['a','b','c']
    outputlist = []
    for letter in stringList:
        outputlist.append(letter)
    return outputlist


def splitRaw(inputStringRAW):
    return inputStringRAW.split(', ')


def splitSublistsRaw(inputString):
    inputString = inputString.replace('[[', '').replace(']]', '')
    return inputString.split('],[')


def unpackString(string):
    data = string.split(',')
    outputlist = []
    for dat in data:
            outputlist.append(dat)
    return outputlist


