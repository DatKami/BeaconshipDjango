from django.db.models import *
  
"""
A contender in a ELO/Win system.
"""
class Contender(Model):
  def __str__(self):
    return self.name
    
  id        = models.AutoField(primary_key = True)
  name      = CharField(max_length = 32)
  elo       = PositiveSmallIntegerField(verbose_name = "ELO", default = 1400)
  wins      = PositiveIntegerField(default = 0)
  active    = BooleanField(default=True)
  
  def save(self, *args, **kwargs):
    #Every time we make an edit to the contender, we make a new history
    super(Contender, self).save(*args, **kwargs)
    #make the history object
    History(contender = self, elo = self.elo, wins = self.wins).save() 

"""
A historic point in a Win/ELO system.
""" 
class ContenderHistory(Model):
  def __str__(self):
    return self.contender.name + " " + date_committed
    
  class Meta:
    verbose_name        = "Contender History"
    verbose_name_plural = "Contender Histories"
  
  contender       = ForeignKey(Contender, related_name ='+', on_delete=PROTECT)
  date_committed  = DateTimeField(auto_now_add=True)
  elo             = PositiveSmallIntegerField(verbose_name = "ELO")
  wins            = PositiveIntegerField()