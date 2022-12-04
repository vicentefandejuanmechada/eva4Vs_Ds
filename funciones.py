from barcode.codex import code128
from barcode.writer import ImageWriter
from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer,
Paragraph, Table, TableStyle,colors,cm)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4




def crearcodigobarra(numero):
    with open("eva4Vs_Ds/static/barcode/"+numero+".jpg", "wb") as f:
        code128(numero, writer = ImageWriter()).write(f)

def transformar_euro_peso(euro):
    return euro*700





def creararchivoPDFmasivo(nombre):
     #encriptar el pdf con el rut sin el digito verificador
    rutt=nombre[0],nombre[1],nombre[3],nombre[4],nombre[5],nombre[6],nombre[7],nombre[8]
    doc = SimpleDocTemplate("eva4Vs_D/pdf/codigobarra.pdf", pagesize=A4 encrypt=str(rutt))
    story = []
    datos = [['codigo barra', "nombre producto", "cantidad por unidad", "precio PCL","Precio euro","proveedor"]]
    listaalumnos = Productos.objects.all()
    for alum in listaalumnos:
        barcode= Image("cfttalcaalumnos/static/barcode/"+(insertar producto.codigobarra)+".jpg", width=100, height=100)
        datos.append([alum.rut, alum.nombre, alum.apellidop, alum.apellidom])
    tabla = Table(data=datos,
                    colWidths=[2 * cm, 4 * cm, 4 * cm, 4 * cm, 4 * cm, 4 * cm],
                    rowHeights=0.5 * cm,
                    style=[
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ])  
    story.append(tabla)
    story.append(Spacer(0, 15))
    doc.build(story)

