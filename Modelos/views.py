"""
    aqui van las views como clases xd
"""

import csv
import os
from django.shortcuts import render
from django.views import View

from Modelos.models import Producto  ##!: No module named 'Modelos.models'##

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
            return render(request, "productos.html", {"productos": productos})
        return render(request, "productos.html", {"error": "No hay productos"})


def cargaMasiva(request):
    with open(
        os.path.join(os.path.dirname(__file__), "../Djando_productos.csv"),
        encoding="utf-8",
    ) as csvfile:
        reader = csv.DictReader(csvfile)
        prods = [
            Producto(
                codproducto=row["CodigoProducto"],
                nombreproducto=row["NombreProducto"],
                provedor=row["Proveedor"],
                cantidad_x_unidad=row["CantidadPorUnidad"],
                valor_euro=row["PrecioUnidad"],
                stock=row["UnidadesEnExistencia"],
            )
            for row in reader
        ]
        bulk = Producto.objects.bulk_create(prods)
        print(bulk)
        productos = Producto.objects.all()
        return render(request, "productos.html", {"productos": productos})


##NO DEVUELVE LOS PRODUCTOS NOSE PORQUE XD
# def importdta():
#     cargarcvs = 'Djando_productos.csv'
#     with open(cargarcvs) as f:
#       reader = csv.reader(f,delimiter=";")
#       for row in reader:
#         pproducto = producto(codprod=row[0],nombreproducto=row[1],provedor=row[2],categoria=row[3],cantidad_x_unidad=row[4],valor_peso=row[5],valor_euro=row[6],stock=row[7])
#         pproducto.save()


# def cargardatos(request):
#     prod= producto.objects.all()
#     return render(request, "productos.html",{"prodductos": prod})
