from django.shortcuts import render
from django.http import HttpResponse
from Enigma import forms, enigma
import Enigma.models as md
import string

def index(request):
    template = '/index.html'
    pluglist = []
    presetForm = forms.presetForm(request.POST)
    enigmaForm = forms.basicenigmaForm()
    if request.method == 'POST' and 'PresetSubmit' in request.POST:
        presetdata = request.POST.get('preset')

        enigmaForm.updatePreset(presetdata)

    if request.method == "POST" and 'EnigmaSubmit' in request.POST:
        data = enigmaForm.getSettings()
        emachine = enigma.enigma(pluglist, md.chooseRotors(data), md.chooseReflectors(data), data[3])
        emachine.messageSettings(data[2])
        return render(request, template, {'Form': enigmaForm, 'form1': presetForm})
    else:
        return render(request, 'Enigma/index.html', {'Form': enigmaForm, 'Form1': presetForm})
