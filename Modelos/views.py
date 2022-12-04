from django.shortcuts import render
from Modelos.models import producto,clientes,venta
import csv
# from 
# Create your views here.

def importdta ():
    cargarcvs = 'C:/csv/Djando_productos.csv'
    with open(cargarcvs) as f:
      reader = csv.reader(f,delimiter=";")
      for row in reader:
        pproducto = producto(codprod=row[0],nombreproducto=row[1],provedor=row[2],categoria=row[3],cantidad_x_unidad=row[4],valor_peso=row[5],valor_euro=row[6],stock=row[7])
        pproducto.save()


def cargardatos(request):
    prod= producto.objects.all()
    return render(request, "productos.html",{"prodductos": prod})
# def cargardatos(request):
#     productos = producto.objects.all()

#     return render(request, "productos.html",{"prodductos": productos})