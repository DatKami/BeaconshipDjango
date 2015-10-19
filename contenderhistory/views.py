from django.shortcuts import render
from django.utils import simplejson
from contenderhistory.models import *
from django.db.models import Avg, Max, Min

def change_elo_win(request):
  pass


def show_up(request):
  c = {} # a list of variables to pass to the webpage
  pass

"""
Get the history of a contender in a day or month.
Returns:  avg - average of all history points in this time period.
          min - min " "
          max - max " "
Arguments:	id - int - of a contender
            year - int - to pull history from
            month - int - to pull history from
            day - int - " " " "
"""
def get_history_month(id, year, month, day=None):
  q = Contender.objects.filter(id=id)
  q.filter(date_committed__year=str(year),
           date_committed__month=str(month))
  if day:
    q.filter(date_committed__day=str(day))
  #at this point the filter has all the history for the contender
  #so tell the database to pull it
  count = q.count()
  if count > 0:
    avg = q.aggregate(Avg('elo'))
    min = q.aggregate(Min('elo'))
    max = q.aggregate(Max('elo'))
    return avg, min, max
  return None, None, None
  