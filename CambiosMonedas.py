from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Notebook
import Util
import csv
from functional import seq
from datetime import datetime
import matplotlib.pyplot as plt
from functools import reduce
import math

#***** Subrutinas *****

def obtenerMonedas():
    with open("./datos/Cambios Monedas.csv") as archivo:
        monedas = seq(csv.reader(archivo)).drop(1) \
                  .map(lambda linea: linea[0]) \
                  .distinct() \
                  .to_list()
    return monedas

def obtenerDatos():
    with open("./datos/Cambios Monedas.csv") as archivo:
        datosCSV = csv.reader(archivo) # obtener los datos CSV
        next(datosCSV) # saltar la primera linea
        return [
            { "moneda": linea[0], \
              "fecha": datetime.strptime(linea[1], "%d/%m/%Y").date(),
              "cambio": float(linea[2]) \
            } for linea in datosCSV
            ]

def filtrarDatos(datos, moneda, desde, hasta):
    return list(filter(lambda item: item["moneda"]==moneda \
                  and item["fecha"] >= desde \
                  and item["fecha"] <= hasta, datos))

def extraerFechasYCambios(datos):
    fechas = list(map(lambda item: item["fecha"],datos))
    cambios = list(map(lambda item: item["cambio"],datos))
    return fechas, cambios

def graficar():
    moneda = monedas[cmbMoneda.current()] #nombre de la moneda escogida
    desde = cldDesde.get_date()
    hasta = cldHasta.get_date()
    datos = obtenerDatos()
    datosFiltrados = filtrarDatos(datos, moneda, desde, hasta)
    fechas, cambios = extraerFechasYCambios(datosFiltrados)
    
    #grafica
    plt.clf()
    plt.plot(fechas, cambios)
    plt.ylabel(f"Cambios de {moneda}")
    plt.xlabel("Fecha")
    plt.grid()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("graficamonedas.png")

    #mostrar la grafica en el panel
    lblGrafica = Label(paneles[0])
    imgGrafica = PhotoImage(file="graficamonedas.png")
    lblGrafica.configure(image=imgGrafica)
    lblGrafica.image = imgGrafica
    lblGrafica.place(x=0,y=0)

    #redimensionar la ventana
    v.minsize(imgGrafica.width(), imgGrafica.height()+100)
    panelPestañas.select(0)

def calcularPromedio(datos):
    return reduce(lambda suma, item: suma + item, datos) / len(datos) \
           if datos else 0

def calcularDesviacionEstandar(datos):
    promedio = calcularPromedio(datos)
    return math.sqrt(reduce(lambda suma, item: suma + (item-promedio)**2, datos) / len(datos) \
           if datos else 0)

def calcularMediana(datos):
    datosOrdenados = sorted(datos)
    n = len(datosOrdenados)
    mediana = (lambda item: item[n//2] if n % 2 == 1 \
               else reduce(lambda a, b: (a+b)/2, map(lambda i: item[i], [n//2, n//2-1]))) \
                    (datosOrdenados)
    return mediana

def calcularMaximo(datos):
    return reduce(lambda maximo, item: item if item>maximo else maximo, datos) if datos else 0

def calcularMinimo(datos):
    return reduce(lambda minimo, item: item if item<minimo else minimo, datos) if datos else 0

def calcularModa(datos):
    #contar cada dato diferente (hallar la frecuencia de cada dato)
    frecuencias = reduce(lambda diccionarios, dato: \
                         { **diccionarios, dato: diccionarios.get(dato, 0)+1 }, datos, {})
    #la moda es el dato con mayor frecuencia
    maxFrecuencia = reduce(lambda maximo, item: item if item[1]>maximo[1] else maximo, \
                           frecuencias.items()) if datos else 0
    return maxFrecuencia[0]

def obtenerEstadisticas():
    moneda = monedas[cmbMoneda.current()]
    desde = cldDesde.get_date()
    hasta = cldHasta.get_date()
    datos = obtenerDatos()
    datosFiltrados = filtrarDatos(datos, moneda, desde, hasta)
    cambios = list(map(lambda item: item["cambio"],datosFiltrados))

    return {
        "Promedio":calcularPromedio(cambios),
        "Desviación Estandar":calcularDesviacionEstandar(cambios),
        "Máximo":calcularMaximo(cambios),
        "Mínimo":calcularMinimo(cambios),
        "Mediana":calcularMediana(cambios),
        "Moda":calcularModa(cambios)
    }

def mostrarEstadisticas():
    #limpiar el panel
    for item in paneles[1].winfo_children():
        item.destroy()
    
    estadisticas = obtenerEstadisticas()

    for i, (clave, valor) in enumerate(estadisticas.items()):
        Util.agregarEtiqueta(paneles[1], clave, i, 0)
        Util.agregarEtiqueta(paneles[1], valor, i, 1)

    panelPestañas.select(1)
    

#***** Programa Principal *****
v = Tk()
v.title("Cambios de Moneda")
v.geometry("500x300")

iconos =["./iconos/Grafica.png", "./iconos/Datos.png"]
textos=["Gráfica Cambio vs Fecha", "Estadísticas"]

botones = Util.agregarBarra(v, iconos, textos)
botones[0].configure(command = graficar)
botones[1].configure(command = mostrarEstadisticas)


#Agregar panel para selecionar monedas y rango de fechas
panel = Frame(v)
panel.pack(side=TOP, fill=X)

monedas = obtenerMonedas()

Util.agregarEtiqueta(panel, "Moneda:", 0, 0)
cmbMoneda = Util.agregarLista(panel, monedas, 0, 1)
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
    paneles.append(panel)

"""def mostrarDatos():
    # Limpiar el panel (asumiendo que el panel 2 es para esta vista)
    for item in paneles[2].winfo_children():
        item.destroy()
    
    moneda = monedas[cmbMoneda.current()]
    desde = cldDesde.get_date()
    hasta = cldHasta.get_date()
    datos = obtenerDatos()
    datosFiltrados = filtrarDatos(datos, moneda, desde, hasta)
    
    # Crear encabezados
    Util.agregarEtiqueta(paneles[2], "Fecha", 0, 0)
    Util.agregarEtiqueta(paneles[2], "Cambio", 0, 1)
    
    # Mostrar los datos
    for i, dato in enumerate(datosFiltrados, start=1):
        Util.agregarEtiqueta(paneles[2], dato["fecha"].strftime("%d/%m/%Y"), i, 0)
        Util.agregarEtiqueta(paneles[2], dato["cambio"], i, 1)
    
    panelPestañas.select(2)  # Seleccionar la pestaña de datos




    botones[2].configure(command = mostrarDatos)  # Agrega esta línea después de las configuraciones de los otros botones




    paneles = []
for texto in textos:  # Esto ya creará 3 paneles porque textos ahora tiene 3 elementos
    panel = Frame(v)
    panelPestañas.add(panel, text=texto)
    paneles.append(panel)"""

    

