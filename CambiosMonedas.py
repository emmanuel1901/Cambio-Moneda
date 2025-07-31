from tkinter import *
import Util
from tkinter import Notebook

v = Tk()
v.title("Cambios de Moneda")
v.geometry("400x300")

iconos =["./iconos/Grafica.png", "./iconos/Datos.png"]
textos=["Gráfica Cambio vs Fecha", "Estadísticas"]

botones = Util.agregarBarra(v, iconos, textos)

#Agregar panel para selecionar monedas y rango de fechas
panel = Frame(v)
panel.pack(side=TOP, fill=X)

Util.agregarEtiqueta(panel, "Moneda:", 0, 0)
cmbMoneda = Util.agregarLista(panel, [], 0, 1)
Util.agregarEtiqueta(panel, "Desde:", 0, 2)
cldDesde = Util.agregarCalendario(panel, 0, 3)
Util.agregarEtiqueta(panel, "Hasta:", 0, 4)
cldHasta = Util.agregarCalendario(panel, 0, 5)

#Agregar las pestañas para despliegue de la información
panelPestañas= Notebook(v)
panelPestañas.pack(fill=BOTH,expand=YES)
paneles = []
for texto in textos:
    panel = Frame(v)
    panelPestañas.add(panel, text=texto)



