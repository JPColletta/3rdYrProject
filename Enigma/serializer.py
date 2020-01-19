from rest_framework import serializers
from Enigma import models as md

class presetSerializer(serializers.ModelSerializer):
    class meta:
        model = md.presetModel
        fields =  ('id', 'name', 'initvec')
        depth = 1

class rotorSerializer(serializers.ModelSerializer):
    presetSer = presetSerializer()
    class meta:
        model = md.rotorModel
        fields = ('char_map', 'turnover_pos', 'notchPos', 'name', 'preset', 'presetSer')

class reflectorSerializer(serializers.ModelSerializer):
    presetSer = presetSerializer()
    class meta:
        model = md.reflectorModel
        fields = ('char_map', 'name', 'preset', 'presetSer')
