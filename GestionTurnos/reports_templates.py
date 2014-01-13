# -*- coding: utf-8 -*-

import reportlab
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

from report_globals import *
from report_utils import *


def generate_turn(response, turn):
    """

    """
    c = canvas.Canvas(response, A4)
    y = y_rest #alto disponible

    #titulo
    c.setFont("Helvetica", H2)
    set_color(c, "666666")
    c.drawString(m_left, y, "Comprobante del Turno")
    y -= P
    set_color(c, "000000")
    hr_line(c, y)

    #Nro Turno
    #----------------------------------------------------
    t1 = stringWidth("Nro Orden", "Helvetica", P)
    t2 = stringWidth("22", "Helvetica", H1)
    w = t1 + 2*10 #ancho cajas
    pd = (w - t2) / 2
    #posicion inicial
    xi = m_right - w - cm
    yi = m_top - 2.3*cm

    #texto
    c.setFont("Helvetica", P)
    c.drawString(xi+10, yi, "Nro Orden")
    c.setFont("Helvetica-Bold", H1)
    set_color(c, "AAAAAA")
    c.drawString(xi+pd, yi - H1, "22")

    #horizontal lines
    c.line(xi, yi+P, xi+w, yi+P)
    c.line(xi, yi-5, xi+w, yi-5)
    c.line(xi, yi-5-H1, xi+w, yi-5-H1)
    #vert lines
    c.line(xi, yi+P, xi, yi-5-H1)
    c.line(xi+w, yi+P, xi+w, yi-5-H1)
    #resetea color texto
    set_color(c, "000000")
    #---------------------------------------

    #Datos Medico
    y -= 2*P
    c.setFont("Helvetica-Bold", P)
    c.drawString(m_left, y, "Medico:")
    c.setFont("Helvetica", P)
    c.drawString(m_left + x_rest/6, y, turn.medic.get_full_name())

    #Datos paciente
    y -= 2*P
    c.setFont("Helvetica-Bold", P)
    c.drawString(m_left, y, "Pacientes:")
    c.setFont("Helvetica", P)
    c.drawString(m_left + x_rest/6, y, turn.patient.get_full_name())

    #Fecha
    y -= 2*P
    c.setFont("Helvetica-Bold", P)
    c.drawString(m_left, y, "Fecha:")
    c.setFont("Helvetica", P)
    c.drawString(m_left + x_rest/6, y, "23/12/2013")

    y -= 2*P
    c.setFont("Helvetica-Bold", P)
    c.drawString(m_left, y, "Inicia:")
    c.setFont("Helvetica", P)
    c.drawString(m_left + x_rest/6, y, "08:30")

    c.setFont("Helvetica-Bold", P)
    c.drawString(m_left + (x_rest/6)*4, y, "Finaliza:")
    c.setFont("Helvetica", P)
    c.drawString(m_left + (x_rest/6)*5, y, "08:50")

    #pie pagina
    #-------------------------------------------------------------
    y -= 2*P
    hr_line(c, y)
    y -= 18
    c.setFont("Helvetica", 10)
    c.drawString(m_left, y, "Se recomienda que asista 20 minutos antes del horario acordado para evitar cualquier tipo de Inconvenientes.")
    y -= P
    hr_line(c, y)
    #--------------------------------------------------------------
    c.save()
