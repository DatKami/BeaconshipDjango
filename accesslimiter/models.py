from django.db.models import *

# Create your models here.
class Access(Model):
  def __str__(self):
    return self.ip_address
    
  class Meta:
    verbose_name_plural = "Accesses"
  
  ip_address  = GenericIPAddressField()
  valid_after = DateTimeField(auto_now_add = True)
  hits        = IntegerField(default = 0)
  completes   = IntegerField(default = 0)
  posts       = IntegerField(default = 0)
  