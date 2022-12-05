"""
    aqui van las views como clases xd
"""

import csv
import os
from django.shortcuts import render
from django.views import View
import barcode
from barcode.writer import ImageWriter
from random import randint
import re
# !: No module named 'Modelos.models'##
from Modelos.models import Producto, clientes, venta


# from
# Create your views here.

# ENCODING ACENTOS Y Ñ


# EL diego va a realizar la parte de los graficos y wea
# yo(vicente i neeed help) con cargar los datos cvs con reglas
# codigo de barra y vender producto no esta destinado a ni uno de los 2
# correos masivos esta casi realizado por las mismas clases hay q adaptarlo


def producto(request):
    """obtiene todos los productos"""
    if request.method == "GET":
        productos = Producto.objects.all().order_by("codproducto")
        if productos:
            return render(request, "datosprod.html", {"productos": productos})
        else:
            return render(request, "datosprod.html", {"error": "No hay productos"})


def cliente(request):
    if request.method == "GET":
        cliente = clientes.objects.all()
        if cliente:
            return render(request, "clientes.html", {"cliente": cliente})
        else:
            return render(request, "clientes.html", {"error": "no hay cliente"})


def carga_masiva(request):
    """carga masiva de productos"""
    with open(
        os.path.join(os.path.dirname(__file__), "../Djando_productos.csv"),
        encoding="utf-8",
    ) as csvfile:
        reader = csv.DictReader(csvfile)
        prods = [
            Producto(
                # se ve como tabla ahora xd

                nombreproducto=row["Nombre Producto"],
                provedor=row["Proveedor"],
                categoria=row["Categoria"],
                cantidad_x_unidad=row["Cantidad Por Unidad"],
                valor_euro=row["Precio Unidad"],
                valor_peso=transformar_euro_peso(row["Precio Unidad"]),
                stock=row["Unidades En Existencia"],
                codproducto=crearcodigobarra(row["Codigo Producto"]),
            )
            for row in reader
        ]
        bulk = Producto.objects.bulk_create(prods)
        print(bulk)
        productos = Producto.objects.all()
        return render(request, "datosprod.html", {"productos": productos})
        # TODO: redirect to products


def carga_cliente(request):
    with open(
        os.path.join(os.path.dirname(__file__), "../cliente.csv"),
        encoding="utf-8",
    ) as csvfile:
        reader = csv.DictReader(csvfile)
        clients = [
            clientes(
                rut=generrut(idx),
                numero_cliente=row["NumeroCliente"],
                fecha_registro=row["Fecha Ingreso"],
                apellido_p=row["Apellido Paterno"],
                apellido_m=row["Apellido Materno"],
                nombre=row["Nombres"],
                correo=genecorreo(
                    row["Nombres"], row["Apellido Paterno"], row["Apellido Materno"]),
                telefono=juanvtr(idx),
                fecha_nacimiento=row["Fecha Nacimiento"]
            )
            for idx, row in enumerate(reader)
        ]
        bulk = clientes.objects.bulk_create(clients)
        cliente = clientes.objects.all()
        return render(request, "clientes.html", {"cliente": cliente})
        # TODO: redirect to clients


def genecorreo(nombre, apellido1, apellido2):
    return (nombre[0]+apellido1+apellido2[0]).lower()+"@djangocorreo.tk"


def generrut(index):
    rut = 1435566 + index
    rutdv = str(rut) + "-" + str(4 if index == 0 else randint(1, 9))
    return str(rutdv)


def crearcodigobarra(numero):
    code128 = barcode.get_barcode_class("code128")
    my_code = code128(numero, writer=ImageWriter())
    with open("eva4Vs_Ds/static/barcode/"+str(numero)+".png", "wb") as f:
        my_code.write(f)
    return my_code.get_fullcode()


def juanvtr(index):
    return str(1435566 + index)


def transformar_euro_peso(euro):
    # regex para  eliminar "€"
    euro = re.sub(r"€", "", euro)
    return int(float(euro) * 900)

# funciones de ejempl
# ///
# def obtproductoinfo(request):
#     codigoprod = request.GET['codigoprod']
#     objetoprod = retornaprods(codigoprod)
#     return render(request, "detalleventa.html",{"producto":objetoprod})
# # aca
# ///
# retornar
# def retornaprods(codigoprod):
#     for producto in listaprod:
#         if str(producto.codigoprod) == codigoprod:  
#             return producto
#     return "null"

# toma el codigo pero no lo compara bien con los demas codigos

# # version imitando  eva3
# global listaproductos
# listaproductos = Producto.objects.all()


# def obtproductoinfo(request):
#     codigoprod = request.GET['codproductos']
#     objetoprod = retornarprod(codigoprod)            
#     return render(request, "detalleprod.html", {"producto": objetoprod})

    
# def retornarprod(codproducto):
#     for producto in listaproductos:
#         if str(producto.codproducto) == codproducto:
#             return producto
#     return "null"

# # version diego copilot
def obtproductoinfo(request):
    productolist = Producto.objects.all()
    if request.method == "GET":
        codigoprod = request.GET['codproductos']
        objproduc  = retornarprod['codiprod']
        for producto in productolist:
            if str(producto.codproducto) == codigoprod:
                return render(request, "detalleprod.html", {"producto": objproduc})

    
def retornarprod(codproducto):
    productolist = Producto.objects.all()
    for producto in productolist:
        if str(producto.codproducto) == codproducto:
            return producto
    return "null"

