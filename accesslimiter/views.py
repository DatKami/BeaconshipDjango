from django.shortcuts import render
from accesslimiter.models import *

# Create your views here.

"""
Return a relevant IP.
"""  
def capture_ip(request):
  #check 3 sources:
  #HTTP_CLIENT_IP, then
  #HTTP_X_FORWARDED_FOR, and last
  #REMOTE_ADDR

  ip = request.META.get('HTTP_CLIENT_IP')
  if ip:
    ip = ip.split(',')[0]
  else:
    ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip:
      ip =  ip.split(',')[0]
    else:
      ip = request.META.get('REMOTE_ADDR').split(',')[0]
      
  log_ip(ip)  #log the ip
  return ip   #and return it
  
"""
Logs an IP to update the hits counter.
"""  
def log_ip(ip):
  access, created = Access.objects.get_or_create(ip_address = ip)
  if not created:               #update an existing entry
    access.hits = F('hits') + 1 #no race condition to increase hits
    access.save()
  #else move along

"""

"""  
def is_post_eligible(ip):

    