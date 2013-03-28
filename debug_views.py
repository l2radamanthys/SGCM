# To change this template, choose Tools | Templates
# and open the template in the editor.

from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.contrib import auth #para login
from django.contrib.auth.models import User
from django.contrib.auth.models import Group as DjangoGroup

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

import calendar
import datetime

from GestionTurnos.models import *
import GestionTurnos.forms as my_forms
from utils import *
from globals import *



"""
    Las vistas aqui incluidas solo son para Debug de errores, no se implementaran
    en la version de producion
"""

def calendar(request,month=None, year=None):
    """
    """

    mi_template = get_template('GestionTurnos/calendar.html')
    dict = generate_base_keys(request)

    if month != None and year != None:
        month = int(month) % 13
        year = int(year)

    else:
        year = datetime.date.today().year
        month = datetime.date.today().month

    #hoy
    t_year = datetime.date.today().year
    t_month = datetime.date.today().month

    cal = calendar.Calendar()
    wekends = cal.monthdayscalendar(year, month)

    dict['month'] = MONTHS[month-1]
    dict['year'] = year
    dict['wekends'] = wekends

    if month == 1:
        dict['prev_month'] = 12
        dict['next_month'] = 2
        dict['prev_year'] = year - 1
        dict['next_year'] = year

    elif month == 12:
        dict['prev_month'] = 11
        dict['next_month'] = 1
        dict['prev_year'] = year
        dict['next_year'] = year + 1

    else:
        dict['prev_month'] = month - 1
        dict['next_month'] = month + 1
        dict['prev_year'] = year
        dict['next_year'] = year

    if dict['prev_month'] < t_month and dict['prev_year'] == t_year or dict['prev_year'] < t_year:
        dict['prev_month'] = t_month
        dict['prev_year'] = t_year


    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def perms_list(request):
    mi_template = get_template('GestionTurnos/perm-list.html')
    dict = generate_base_keys(request)

    #from django.contrib.auth.models import Permission

    dict['perms'] = Permission.objects.all()


    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)



def apps_list(request):
    mi_template = get_template('GestionTurnos/apps-list.html')
    dict = generate_base_keys(request)

    #from django.contrib.auth.models import Permission

    dict['apps'] = ContentType.objects.all()


    html_cont = mi_template.render(Context(dict))
    return HttpResponse(html_cont)


def test_mail(request):
    pass
