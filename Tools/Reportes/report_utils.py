


from report_globals import *


def set_color(canvas, color):
    """
        Define el color del canvas usando un formato hexadecimal
    """
    if len(color) == 6:
        #conversion a entero
        r = int(color[:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)
        #convertimos a flotante
        r = round(float(r) / 255, 3)
        g = round(float(g) / 255, 3)
        b = round(float(b) / 255, 3)

        print r,g,b
        canvas.setFillColorRGB(r,g,b)

    else:
        print "Error formato no valido"


def hr_line(canvas, y):
    canvas.line(m_left, y, m_right, y)
