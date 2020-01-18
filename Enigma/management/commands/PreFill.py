from os import path, getcwd
from django.core.management.base import BaseCommand as BC
import Enigma.models as md
import csv

class Command(BC):


    def customInit(self):
        importfile = path.abspath(getcwd()) + '\\Enigma\\rotorDataRaw.txt'
        with open(importfile, 'r') as f:
            for line in f.readlines():

                rotorVector = []
                reflectorVector = []
                rawSplit = md.splitRaw(line)
                print(rawSplit)
                nameRAW, rotorRAW, reflectorRAW, EKWRAW= rawSplit[0], rawSplit[1], rawSplit[2], rawSplit[3][1:27]
                rotorListRaw = md.splitSublistsRaw(rotorRAW)
                reflectorListRaw = md.splitSublistsRaw(reflectorRAW)

                for rotor in rotorListRaw:
                    rotorVector.append(md.unpackString(rotor))

                for reflector in reflectorListRaw:
                    reflectorVector.append(md.unpackString(reflector))

                PModel = md.presetModel()
                PModel.name,  PModel.initvec = nameRAW, EKWRAW
                PModel.save()
                for rotor in rotorVector:
                    RModel = md.rotorModel()
                    print(rotor)
                    RModel.data, RModel.char_map, RModel.notchPos, RModel.turnoverPos, RModel.name, RModel.preset = PModel, rotor[0], rotor[1], rotor[2], rotor[3], nameRAW
                    RModel.save()
                print('\n')
                for reflector in reflectorVector:
                    RefModel = md.reflectorModel()
                    RefModel.data, RefModel.char_map, RefModel.name, RefModel.preset = PModel, reflector[0], reflector[1], nameRAW
                    RefModel.save()
                rotorVector, reflectorVector = [], []


        print('\n' + "!!!Preset Models Saved To DataBase!!!"+ '\n')


    def handle(self, *args, **options):
        self.customInit()



