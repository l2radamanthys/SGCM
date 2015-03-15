
import os
import sys

proyect_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(proyect_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

#print proyect_path
#print os.environ['DJANGO_SETTINGS_MODULE'] 

import django
#django.setup()

from django.core.mail import send_mail

send_mail(
	'Subject here', 
	'Here is the message.', 
	'sgcm.smtp@yahoo.com',
    ['l2radamanthys@gmail.com']
	)