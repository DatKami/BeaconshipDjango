from django.shortcuts import render
from beaconship.models import *
from contenderhistory.views import historic_month
from django.utils import timezone
from django.utils.timezone import localtime
from datetime import *

# Create your views here.

"""
  Something funny happens here.
  Returns:    A joggled ship
  Arguments:  ship_id - int - for the pk of the ship
"""
def joggle_ship(ship_id):
  ship = Ships.objects.get(id=ship_id)
  contenders = BSContender.objects.filter(ship=ship)
  contenders.order_by('id')
  c_historics = []
  date = timezone.localtime(timezone.now())
  for day in range(30):
    start = datetime(date.year, date.month, date.day)
    end = datetime(date.year, date.month, date.day) + timedelta(microseconds=-1) + timedelta(days=1)
    query = ContenderHistory.objects.filter(contender__in=contenders, date_committed__gt=start, date_committed__lt=end).order_by('-date_committed').distinct('contender')
    query.order_by('-elo')
    toput = list(query)
    c_historics.append(toput)
    date = date - timedelta(days=-1)
  return c_historics
