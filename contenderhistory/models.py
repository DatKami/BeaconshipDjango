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
    return self.name
  id        = models.AutoField(primary_key = True)
  name      = CharField(max_length = 32)
  shorthand = CharField(max_length = 16, verbose_name = "Shorthand")
  elo       = PositiveSmallIntegerField(verbose_name = "ELO", default = 1400)
  wins      = PositiveIntegerField(default = 0)
  color     = RGBColorField(default="#FFFFFF")
  gender    = models.CharField(max_length = 1 , choices=GENDERS, default='N')
  active    = BooleanField(default=True)
  
  def save(self, *args, **kwargs):
    #Every time we make an edit to the contender, we make a new history
    """"
    if self.pk is not None: #does this object exist yet?
      orig = Contender.objects.get(pk=self.pk)
      if orig.version != self.version:
        #something is messed up here, recalc
    #done dealing with a new version, so save
    self.version = self.version + 1
    """
    super(Contender, self).save(*args, **kwargs)
    #make the history object
    History(contender = self, elo = self.elo, wins = self.wins).save() 
    
  
class History(Model):
  def __str__(self):
    return self.contender.name + " " + date_commited
    
  class Meta:
    verbose_name_plural = "Histories"
  
  contender     = ForeignKey(Contender, related_name = '+', on_delete=PROTECT)
  date_commited = DateTimeField(auto_now_add=True)
  elo           = PositiveSmallIntegerField(verbose_name = "ELO")
  wins          = PositiveIntegerField()