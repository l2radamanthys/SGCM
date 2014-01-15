# -*- coding: utf-8 -*-


"""
Tareas Programadas
"""

from django_cron import cronScheduler, Job
import datetime

from GestionTurnos.models import *


class UpdateTurnStatus(Job):
    """
        Actualiza el estado de los turnos
    """
    #ejecutarse cada 10 minutos
    run_every = 60


    def job(self):
        t = datetime.datetime.now()
        date = datetime.date.today()
        hour = datetime.time(t.hour, t.minute)
        #dias pasados
        turns = Turn.objects.filter(day__date__lte=date, status=0)
        for turn in turns:
            turn.status = 4
            turn.save()
        #hasta hoy
        turns = Turn.objects.filter(day__date=date, status=0, start__lte=hour)
        for turn in turns:
            turn.status = 4
            turn.save()

        print "run job .D"


cronScheduler.register(UpdateTurnStatus)