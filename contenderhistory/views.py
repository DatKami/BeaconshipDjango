from django.shortcuts import render
from django.utils import simplejson
from contenderhistory.models import *
from django.db.models import Avg, Max, Min
from django.utils import timezone
from django.utils.timezone import localtime
from datetime import *
from contenderhistory.config import *

def change_elo_win(request):
  pass


def show_up(request):
  c = {} # a list of variables to pass to the webpage
  pass

"""
Get the history of a contender in a day or month.
Returns:    avg     - int       - average of all history points in this time period.
            nothing - bool      - If false, no possible data points are backwards from this point
Arguments:	id      - int       - of a contender
            start   - datetime  - to start the query
            end     - datetime  - to end the query
"""
def get_history(id, start, end):
  q = Contender.objects.filter(id=id)
  r = q.filter(
  #at this point the filter has all the history for the contender
  #so tell the database to pull it
  count = r.count()
  if count > 0:
    avg = r.aggregate(Avg('elo'))
    return avg, True
  else: #we need to head backwards and get the first available ELO
    r = q.filter(date_committed__lt=start)
    r.order_by(-'date_committed')
    count = r.count()
    if count > 0:
      return r[0], True
    else:
      return DEFAULT_ELO, False #no points in history, return the default ELO
    

"""
Return a set of points representing the Avg ELO for a 30 day period,
and the min and max of the averages.
Returns:    Array - int[] - representing ELO values
            Min   - int   - of ELO values
            Max   - int   - of ELO values
Arguments:  ID    - int   - of the contender
            date  - dtetme- if specified, start query here and go backwards
"""
def historic_month(id, date=None):
  if not date:  #make a date for them
    date = timezone.localtime(timezone.now())
  elos = [1400 for k in range(30)]
  for i in range(30):
    start = datetime(date.year, date.month, date.day)
    end = datetime(date.year, date.month, date.day) + timedelta(microseconds=-1) + timedelta(days=1)
    elos[29-i], do_not_skip = get_history(id, start, end)
    if not do_not_skip:
      break
    date = date + timedelta(days=-1)
  min = min(elos)
  max = max(elos)
  return elos, min, max

"""
Return a set of points representing the Avg ELO for a 24 hour period,
and the min and max of the averages.
Returns:    Array - int[] - representing ELO values
            Min   - int   - of ELO values
            Max   - int   - of ELO values
Arguments:  ID    - int   - of the contender
            date  - dtetme- if specified, start query here and go backwards
"""  
def historic_day(id, date=None):
  if not date:  #make a date for them
    date = timezone.localtime(timezone.now())
  elos = [1400 for k in range(24)]
  for i in range(24):
    start = datetime(date.year, date.month, date.day, date.hour)
    end = datetime(date.year, date.month, date.day, date.hour) + timedelta(microseconds=-1) + timedelta(hours=1)
    elos[23-i], do_not_skip = get_history(id, start, end)
    if not do_not_skip:
      break
    date = date + timedelta(hours=-1)
  min = min(elos)
  max = max(elos)
  return elos, min, max