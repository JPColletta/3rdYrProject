from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Enigma import models as md
from Enigma import serializer as sz


@api_view(['GET', 'POST'])
def preset_list(request):
    """
    List all presets, no option to create
    :return: serialized preset data
    """
    if request.method == 'GET' or 'POST':
        presets = md.presetModel.objects.all()
        serializer = sz.presetSerializer(presets, context={'request': request}, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def preset_detail(request, pk):
    """
    Retrieve a preset instance
    :param pk: Primary Key of target
    :return: serialized preset data for target preset only
    """
    try:
        preset = md.presetModel.objects.get(pk=pk)
    except md.presetModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST' or 'GET':
        serializer = sz.presetSerializer(preset, context={'request':request})
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def rotor_list(request):
    """
    List all rotors, no option to create
    :return: serialized preset data
    """
    if request.method == 'GET' or 'POST':
        rotors = md.rotorModel.objects.all()
        serializer = sz.rotorSerializer(rotors, context={'request': request}, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def rotor_detail(request, pk):
    """
    Retrieve a rotor instance
    :param pk: Primary Key of target
    :return: serialized rotor data for target preset only
    """
    try:
        rotor = md.rotorModel.objects.get(pk=pk)
    except md.rotorModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST' or 'GET':
        serializer = sz.rotorSerializer(rotor, context={'request': request})
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def reflector_list(request):
    """
    List all reflector, no option to create
    :return: serialized reflector data
    """
    if request.method == 'GET' or 'POST':
        reflectors = md.reflectorModel.objects.all()
        serializer = sz.reflectorSerializer(reflectors, context={'request': request}, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def reflector_detail(request, pk):
    """
    Retrieve a reflector instance
    :param pk: Primary Key of target
    :return: serialized reflector data for target preset only
    """
    try:
        reflector = md.reflectorModel.objects.get(pk=pk)
    except md.reflectorModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST' or 'GET':
        serializer = sz.reflectorSerializer(reflector, context={'request': request})
        return Response(serializer.data)

