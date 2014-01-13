
import reportlab

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm


from report_globals import *



def main():
    w,h = A4 # 595x842 pt aprox
    print A4, cm
    canva = canvas.Canvas("test.pdf", pagesize=A4)
    #canva.translate(cm, cm)

    y_disp = y_rest #alto disponible


    canva.line(m_left, m_top, m_right, m_top)
    canva.line(m_left, m_bottom, m_right, m_bottom)
    canva.setFont("Helvetica", H2)
    canva.drawString(m_left, y_disp, "SGCM")
    y_disp = y_disp - H2 + 7
    canva.setFont("Helvetica", P)
    canva.drawString(m_left, y_disp, "Sistema de Gestion de Consultorio Medico")

    while (y_disp-P) > m_bottom:
        y_disp = y_disp - P    
        canva.drawString(m_left, y_disp, "Otro Texto de Relleno ")
    
    #canva.line(m_left, m_top, m_left, m_bottom)

    canva.save()


main()
