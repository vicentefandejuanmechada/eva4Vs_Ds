from django.shortcuts import render
from Modelos.models import producto,clientes,venta
import csv
# from 
# Create your views here.


#EL diego va a realizar la parte de los graficos y wea
#yo(vicente i neeed help) con cargar los datos cvs con reglas 
#codigo de barra y vender producto no esta destinado a ni uno de los 2
# correos masivos esta casi realizado por las mismas clases hay q adaptarlo

##NO DEVUELVE LOS PRODUCTOS NOSE PORQUE XD
def importdta():
    cargarcvs = 'Djando_productos.csv'
    with open(cargarcvs) as f:
      reader = csv.reader(f,delimiter=";")
      for row in reader:
        pproducto = producto(codprod=row[0],nombreproducto=row[1],provedor=row[2],categoria=row[3],cantidad_x_unidad=row[4],valor_peso=row[5],valor_euro=row[6],stock=row[7])
        pproducto.save()


def cargardatos(request):
    prod= producto.objects.all()
    return render(request, "productos.html",{"prodductos": prod})
