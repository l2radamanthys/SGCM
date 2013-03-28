#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django import forms

from HistoriaClinica.models import *
from globals import *


class AntecedentesPerinatalesForm(forms.Form):


    class Meta:
        model = AntecedentesPerinatales
        fields = (
            'pregnancy_number',
            'pregnancy_duration',
            'controls',
            'normal_birth',
            'weight',
            'size',
            'pathologies',
            'medical_care',
            'coments',
        )
