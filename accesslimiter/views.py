from django.shortcuts import render
from accesslimiter.models import *
from django.utils import timezone
from django.utils.timezone import localtime
from datetime import *

# Create your views here.

"""
Return a relevant IP.
Arguments:  An HTTP request
Returns:    An IP address.
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
      
  return ip   #and return it
  
"""
Logs an IP to update the hits counter.
Arguments: IP string
"""  
def log_ip(ip):
  access, created = Access.objects.get_or_create(ip_address = ip)
  if not created:               #update an existing entry
    access.hits = F('hits') + 1 #no race condition to increase hits
    access.save()
  #else move along

"""
Determines if an IP is eligible to post.
Arguments:  Access object
Returns:    The current time
            If now is past the IP's cooldown counter       
"""  
def is_post_eligible(access):
  now     = timezone.localtime(timezone.now())
  return now, ( now >= access.valid_after )


"""
Updates the post counter if a post is eligible, and ignores posts for X hours.
Arguments:  Access object
            Hours to delay the next post
Returns:    If a post is allowed
"""
def track_post(access, hours):
  now, eligible = is_post_eligible(access)
  if eligible:
    access.posts = F('posts') + 1
    access.valid_after = now + timedelta(hours=hours)
    access.save()
  return eligible
    
"""
Updates the complete counter, and runs track_post.
Arguments:  HTTP request
            If the access should track a post
            Hours to delay the next post
Returns:    If a post is allowed
"""    
def track_complete(request, permission, hours):
  post = False
  access  = Access.objects.get(ip_address = capture_ip(request))
  access.completes = F('completes') + 1
  #check if we should track a post
  if permission:
    post = track_post(access, hours)
  access.save()
  #tell the caller if a post was made
  return post
    
  
  
    