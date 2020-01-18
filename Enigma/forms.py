from django import forms
from Enigma import models as md


class basicenigmaForm(forms.Form):
    preset = 'None'
    IDlist, reflectorNameList, indexList, alphList = md.getEnigmaFormLists(preset)
    inputUKW = forms.CharField(label='Select Reflector:', widget=forms.Select(choices=reflectorNameList))
    rotor2ID = forms.CharField(label='Select Rotor 2:', widget=forms.Select(choices=IDlist))
    rotor2SP = forms.CharField(label='Set Top Char for rotor 2:', widget=forms.Select(choices=alphList))
    rotor2OF = forms.CharField(label='Set Internal Offset for rotor 2:', widget=forms.Select(choices=indexList))

    rotor1ID = forms.CharField(label='Select Rotor 1:', widget=forms.Select(choices=IDlist))
    rotor1SP = forms.CharField(label='Set Top Char for rotor 1:', widget=forms.Select(choices=alphList))
    rotor1OF = forms.CharField(label='Set Internal Offset for rotor 1:', widget=forms.Select(choices=indexList))

    rotor0ID = forms.CharField(label='Select Rotor 0:', widget=forms.Select(choices=IDlist))
    rotor0SP = forms.CharField(label='Set Top Char for rotor 0:', widget=forms.Select(choices=alphList))
    rotor0OF = forms.CharField(label='Set Internal Offset for rotor 0:', widget=forms.Select(choices=indexList))

    def getSettings(self):
        return [self.data['inputUKW'], [self.data['rotor0ID'],self.data['rotor1ID'],self.data['rotor2ID']],[self.data['rotor0SP'],self.data['rotor1SP'],self.data['rotor2SP']],[self.data['rotor0OF'],self.data['rotor1OF'],self.data['rotor2OF']]]

    def updatePreset(self, preset):
        basicenigmaForm.preset = preset


class presetForm(forms.Form):
    presetNames = md.getPresets()
    preset = forms.CharField(label='Choose a Preset', widget=forms.Select(choices=presetNames))
