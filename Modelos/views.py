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
            return render(request, "datosprod.html", {"productos": productos})
        else:
            return render(request, "datosprod.html", {"error": "No hay productos"})

def carga_masiva(request):
    """carga masiva de productos"""
    with open(
        os.path.join(os.path.dirname(__file__), "../Djando_productos.csv"),
        encoding="latin1",
    ) as csvfile:
        reader = csv.DictReader(csvfile)
        print("+++++++++++CARGAAAAAA+++++++++")
        prods = [
            Producto(
                codproducto=row["Codigo Producto"],
                nombreproducto=row["Nombre Producto"],
                provedor=row["Proveedor"],
                cantidad_x_unidad=row["Cantidad Por Unidad"],
                valor_euro=row["Precio Unidad"],
                stock=row["Unidades En Existencia"],
            )
            for row in reader
        ]
        bulk = Producto.objects.bulk_create(prods)
        print(bulk)
        productos = Producto.objects.all()
        return render(request, "datosprod.html", {"productos": productos})
        # TODO: redirect to products