#importa datos Usuarios desde Un CSV


import os, sys
import csv
from random import choice


abc = "0123456789abcdefghijklmnopqrstuvwxyz"

proyect_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(proyect_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

user_csv = "media/export/user.csv"
usrinf_csv = "media/export/userinf.csv"
usergrp_csv = "media/export/user_group.csv"


from django.contrib.auth.models import User
from django.contrib.auth.models import Group as DjangoGroup
from GestionTurnos.models import UserInformation


users = csv.reader(open(user_csv), delimiter=';', quotechar='"')
userinfs = csv.reader(open(usrinf_csv), delimiter=';', quotechar='"')
usr_grps = csv.reader(open(usergrp_csv), delimiter=';', quotechar='"')

kuser = {}

#id; username; first_name;last_name;email;password;is_staff;is_active;is_superuser;last_login;date_joined;

for row in users:
    if row[0] == 'id': continue #saltar primera linea

    if User.objects.filter(username=row[1]).count():
        print "exist", row[1]
        row[1] = row[1] + choice(abc)


    #user = User.objects.create_user(
        #username=row[1],
        #email=row[4],
        #password="123456"
    #)


    print row[1],row[4],row[5]

