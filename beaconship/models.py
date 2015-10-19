from django.db import models
from contenderhistory.models import *
from colorful.fields import RGBColorField
from django.contrib.auth.models import User

GENDERS = (
    (None, 'N'),
    ('M','M'),
    ('F','F'),
)

"""
A tagline is a question a ship can offer to its users.
"""
class Tagline(Model):
  def __str__(self):
    return self.question
  id        = AutoField(primary_key = True)
  question  = CharField(max_length = 64)
  author    = ForeignKey(User, related_name = '+', 
              blank = True, null=True, on_delete=SET_NULL)


"""
A ship defines a collection of Beaconship contenders.
For grabbing contenders related to each other by their series.
"""
class Ship(Model):
  def __str__(self):
    return self.name
    
  id        = AutoField(primary_key = True)
  name      = CharField(max_length = 32)
  active    = BooleanField(default = True)
  author    = ForeignKey(User, related_name = '+', 
              blank = True, null=True, on_delete=SET_NULL)
  taglines  = ManyToManyField(Tagline, 
              blank=True, null=True, related_name='taglines')

"""
A Beaconship contender using a generic contender.
"""
class BSContender(Contender):
  shorthand = CharField(max_length = 16, verbose_name = "Shorthand")
  color     = RGBColorField(default="#FFFFFF")
  gender    = CharField(max_length = 1 , choices=GENDERS, default='N')
  ship      = ForeignKey(Ship, related_name = '+', on_delete=PROTECT)