#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django import forms

from HistoriaClinica.models import *
from globals import *


class AntecedentesPerinatalesForm(forms.ModelForm):
    """
    """
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
        widgets = {
            'pregnancy_number': forms.TextInput({'class':'edt_c'}),
            'pregnancy_duration': forms.TextInput({'class':'edt_c'}),
            'weight': forms.TextInput({'class':'edt_c'}),
            'size': forms.TextInput({'class':'edt_c'}),
            'coments': forms.Textarea(attrs={'cols':'52', 'rows':'5'}),
        }
