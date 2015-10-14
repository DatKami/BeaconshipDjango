from django.db import models
from contenderhistory.models import *
from colorful.fields import RGBColorField

GENDERS = (
    (None, 'N'),
    ('M','M'),
    ('F','F'),
)

"""
A ship defines a collection of Beaconship contenders.
For grabbing contenders related to each other by their series.
"""
class Ship(Model):
  def __str__(self):
    return self.name
    
  id        = models.AutoField(primary_key = True)
  name      = CharField(max_length = 32)
  active    = BooleanField(default = True)

"""
A Beaconship contender using a generic contender.
"""
class BSContender(Contender):
  shorthand = CharField(max_length = 16, verbose_name = "Shorthand")
  color     = RGBColorField(default="#FFFFFF")
  gender    = models.CharField(max_length = 1 , choices=GENDERS, default='N')
  ship      = ForeignKey(Ship, related_name = '+', on_delete=PROTECT)