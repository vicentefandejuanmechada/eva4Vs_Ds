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
from django.core.mail import send_mail
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A2
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
# !: No module named 'Modelos.models'##
from Modelos.models import Producto, clientes, venta
from django.core.mail import EmailMessage
from pathlib import Path
import datetime

# from
# Create your views here.

# ENCODING ACENTOS Y Ñ


# EL diego va a realizar la parte de los graficos y wea
# yo(vicente i neeed help) con cargar los datos cvs con reglas
# codigo de barra y vender producto no esta destinado a ni uno de los 2
# correos masivos esta casi realizado por las mismas clases hay q adaptarlo

# funcion para obtener productos(fuinciona)
def producto(request):
    """obtiene todos los productos"""
    if request.method == "GET":
        productos = Producto.objects.all().order_by("codproducto")
        if productos:
            return render(request, "datosprod.html", {"productos": productos})
        else:
            # ! ruta principal producto
            return render(request, "datosprod.html", {"error": "No hay productos"})

# funcion para obtener clientes(funciona)


def cliente(request):  # obtener
    if request.method == "GET":
        cliente = clientes.objects.all()
        if cliente:
            return render(request, "clientes.html", {"cliente": cliente})
        else:
            return render(request, "clientes.html", {"error": "no hay cliente"})

# funcion para obtener lista con todos los productos(funciona)


def carga_masiva(request):  # ! ruta boton cargar
    """carga masiva de productos"""
    #!comprobar si ya se insertaron datos y cancelar botn
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

# funcion para obtener lista con todos los clientes(funciona)


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
                telefono=crear_num(idx),
                fecha_nacimiento=row["Fecha Nacimiento"]
            )
            for idx, row in enumerate(reader)
        ]
        bulk = clientes.objects.bulk_create(clients)
        cliente = clientes.objects.all()
        return render(request, "clientes.html", {"cliente": cliente})
        # TODO: redirect to clients
# funcion para generar correo cliente(funciona)


def genecorreo(nombre, apellido1, apellido2):
    return (nombre[0]+apellido1+apellido2[0]).lower()+"@djangocorreo.tk"

# funcion para generar rut cliente(funciona)


def generrut(index):
    rut = 1435566 + index
    rutdv = str(rut) + "-" + str(4 if index == 0 else randint(1, 9))
    return str(rutdv)

# funcion para generar codigo de barra(funciona)


def crearcodigobarra(numero):
    code128 = barcode.get_barcode_class("code128")
    my_code = code128(numero, writer=ImageWriter())
    with open("eva4Vs_Ds/static/barcode/"+str(numero)+".png", "wb") as f:
        my_code.write(f)
    return my_code.get_fullcode()

# funcion para generar numero telefono(funciona)


def crear_num(index):
    return str(1435566 + index)

# funcion para transformar euro a peso(funciona)


def transformar_euro_peso(euro):
    # regex para  eliminar "€"
    euro = re.sub(r"€", "", euro)
    return int(float(euro) * 900)


global productolist
productolist = Producto.objects.all()

# funcion que obtiene los parametros del producto buscado


def publicidad(request):
    return render(request, "publicidad.html")


def obtproductoinfo(request):
    codigoprod = request.GET['codproducto']
    objproduc = retornarprod(codigoprod)
    return render(request, "detalleprod.html", {"producto": objproduc})

# retorna el producto en caso de existir


def retornarprod(codproducto):
    for productos in productolist:
        if str(productos.codproducto) == codproducto:
            return productos
    return "null"

# funcion prara crear pdf (esperando confirmacion)


# metodo vender(funciona)
def venderprod(request):
    if request.method == "POST":
        stock = request.POST['cantidad_input']
        id_venta = request.POST['codigo_input']
        producto_venta = Producto.objects.get(codproducto=id_venta)
        if int(stock) <= int(producto_venta.stock):
            producto_venta.stock = int(producto_venta.stock) - int(stock)
            producto_venta.save()
            return render(request, "compra_exitosa.html")
        else:
            return render(request, "compra_fallida.html")

# metodo para poder ver  todos los productos en la base de datos


def verproductos(request):
    productos = Producto.objects.all().order_by("codproducto")
    return render(request, "verproductos.html", {"productos": productos})


# metodo para crear el pdf de los productos(funciona)
def creararchivoPDF(nombre, story):
    rut = nombre[3]+ nombre[4] + nombre[5] + nombre[6]
    ruta = os.path.join(__file__, f'../pdf/{nombre}.pdf')
    doc = SimpleDocTemplate(ruta, pagesize=A2, encrypt=str(rut))
    doc.build(story)


def crearstory():
    story = []
    datos = [['codigo barra', "nombre producto",
              "cantidad por unidad", "precio PCL", "Precio euro", "proveedor"]]
    listproductos = Producto.objects.all()
    for prod in listproductos:
        barcode = Image('eva4Vs_Ds/static/barcode/' +
                        prod.codproducto+'.png', width=100, height=50)
        datos.append([barcode, prod.nombreproducto, prod.cantidad_x_unidad,
                     prod.valor_peso, prod.valor_euro, prod.provedor])

    t = Table(datos, colWidths=[5 * cm, 8 * cm,
                                8 * cm, 5 * cm, 5 * cm, 8 * cm])
    t.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                           ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                           ('BACKGROUND', (0, 0), (-1, 0), colors.green)]))
    story.append(t)
    return story

# metodo para enviar el correo con el pdf adjunto
def correoadjunto(request):
    lista = clientes.objects.all()
    pdf = crearstory()
    for cliente in lista:
        creararchivoPDF(cliente.rut, pdf)
        print("="*5 + "enviado" + "="*5)
        email = EmailMessage(
            f'Hola {cliente.nombre}.',
            'Este es un correo de prueba',
            'diego.soto.mino@gmail.com',
            [cliente.correo],
            reply_to=['diego.soto.mino@gmail.com'],
            headers={'Message-ID': 'foo'},
        )
        email.attach_file(os.path.join(
            os.path.dirname(__file__), f'pdf/{cliente.rut}.pdf'))

        email.send()
    return render(request, "enviado.html")


def graficos(request):
    lista = clientes.objects.all()
    return render(request, "grafico.html",{"productos":lista})







# #funcion para mandar correo mayores de 34
# cliente = Cliente.objects.all()
#     cont = 0
#     for clientes in cliente:
#         fecha_naci = clientes.Fecha_Nacimiento
#         print(fecha_naci)
#         anocomparacion = datetime.date(1988,12,12)
#         print(anocomparacion)
#         if (fecha_naci <=anocomparacion):


            
def correoadjunto2(request):
    lista = clientes.objects.all()
    pdf = crearstory()
    for cliente in lista:
        fecha_nacimiento = cliente.fecha_nacimiento
        fecha_nacimiento = datetime.date
        
        comparacion = datetime.date(1988,12,12)
        if (fecha_nacimiento <=comparacion):
            creararchivoPDF(cliente.rut, pdf)
            print("="*5 + "enviado" + "="*5)
            email = EmailMessage(
            f'Hola {cliente.nombre}.',
            'Este es un correo de prueba',
            'diego.soto.mino@gmail.com',
            [cliente.correo],
            reply_to=['diego.soto.mino@gmail.com'],
            headers={'Message-ID': 'foo'},
        )
            email.attach_file(os.path.join(
                os.path.dirname(__file__), f'pdf/{cliente.rut}.pdf'))

            email.send()
        return render(request, "enviado.html")

        
#correo para numero clientes registrados que el número cliente sea mayor a  1033
def correoadjunto1033(request):
    lista = clientes.objects.all()
    pdf = crearstory()
    for cliente in lista:
        numero_cliente = cliente.numero_cliente
        if (int(numero_cliente) <= 1033):
           creararchivoPDF(cliente.rut, pdf)
        print("="*5 + "enviado" + "="*5)
        email = EmailMessage(
            f'Hola {cliente.nombre}.',
            'Este es un correo de prueba',
            'diego.soto.mino@gmail.com',
            [cliente.correo],
            reply_to=['diego.soto.mino@gmail.com'],
            headers={'Message-ID': 'foo'},
        )
        email.attach_file(os.path.join(
            os.path.dirname(__file__), f'pdf/{cliente.rut}.pdf'))

        email.send()
    return render(request, "enviado.html") 


def graficos(request):
    lista = clientes.objects.all()
    return render(request, "grafico.html",{"productos":lista})