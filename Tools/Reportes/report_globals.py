
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

W,H = A4

#margenes
m_top = H-2*cm #margen top
m_right = W-2*cm #margen 
m_left = cm
m_bottom = cm

y_pos = m_top #posicion actual del cursor
y_rest = m_top - m_bottom #alto disponible para dibujo
x_rest = m_right - m_left
y_anchor = 0 #separacion vertical


#tamanios de texto
H1 = 34
H2 = 23
H3 = 18
P = 12
