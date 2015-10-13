from django.db.models import *
from colorful.fields import RGBColorField
GENDERS = (
    (None, 'N'),
    ('M','M'),
    ('F','F'),
)

# Create your models here.
class Contender(Model):
  def __str__(self):
    return self.full_name
    
  full_name = CharField(max_length = 64)
  shorthand = CharField(max_length = 32, verbose_name = "Shorthand")
  elo =       PositiveSmallIntegerField(verbose_name = "ELO", default = 1400)
  wins =      PositiveIntegerField(default = 0)
  color =     RGBColorField(default="#FFFFFF")
  gender =    models.CharField(max_length = 1 , choices=GENDERS, default='N')
  version =   PositiveIntegerField(default = 0)
  active =    BooleanField(default=True)
  
  def save(self, *args, **kwargs):
  #Every time we make an edit to the contender, we make a new history for items
    self.version = self.version + 1
    History(elo = self.elo, wins = self.wins).save() #make the history object
    super(Contender, self).save(*args, **kwargs) #save this
  
class History(Model):
  def __str__(self):
    return self.contender.full_name + last
  contender = ForeignKey(Contender, related_name = 'history_contender',
                         on_delete=PROTECT)
  last =      DateTimeField('Date Committed' auto_now_add=True)
  elo =       PositiveSmallIntegerField(verbose_name = "ELO")
  wins =      PositiveIntegerField()