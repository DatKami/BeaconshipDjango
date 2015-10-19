from django.shortcuts import render
from beaconship.models import *

# Create your views here.

"""
  Something funny happens here.
  Returns:    A joggled ship
  Arguments:  id - int - for the pk of the ship
"""
def joggle_ship(id):
  ship = Ships.objects.get(id=id)
  contenders = BSContender.objects.filter(ship=ship)
  
  
