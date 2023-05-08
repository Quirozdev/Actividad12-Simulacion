from tkinter import *
from PIL import Image, ImageTk

ventana_principal= Tk()
ventana_principal.title("Verificador de precios")
ventana_principal.geometry("800x600")

# este diccionario va a contener a todos los productos
# sus llaves son los codigos de cada producto y  sus valores son los datos de cada producto
productos = {
   '1h3fsd': {
      'nombre': 'Tostitos 79g',
      'precio': 16,
      'imagen': './img/tostitos.png'
   },
   '2afu13': {
      'nombre': 'Pepsi 400ml',
      'precio': 10,
      'imagen': './img/pepsi_chica.png'
   },
   '3opasd': {
      'nombre': 'Galletas emperador de nuez',
      'precio': 15,
      'imagen': './img/emperador_nuez.png'
   },
   '4xvhqw': {
      'nombre': 'Mazapan gigante',
      'precio': 9,
      'imagen': './img/mazapan.png'
   },
   '518xfp': {
      'nombre': 'Leche Yaqui roja 1.892L',
      'precio': 28,
      'imagen': './img/leche_yaqui_roja.png'
   },
   '6kqagb': {
      'nombre': 'Doritos Nacho',
      'precio': 14,
      'imagen': './img/doritos.png'
   },
   '7asf12': {
      'nombre': 'Galletas Arcoiris',
      'precio': 18,
      'imagen': './img/galletas_arcoiris.png'
   },
   '8xbnqu': {
      'nombre': 'Ruffles Queso',
      'precio': 16,
      'imagen': './img/ruffles_queso.png'
   },
   '9mtehs': {
      'nombre': 'Gansito',
      'precio': 15,
      'imagen': './img/gansito.png'
   },
   '10jrqe': {
      'nombre': 'Chokis',
      'precio': 17,
      'imagen': './img/chokis.png'
   }
}


def crear_imagen_a_label(ruta_imagen: str):
   # se abre la imagen
   imagen = Image.open(ruta_imagen)
   # se redimensiona la imagen para que todas las imagenes tengan el mismo tamanio
   imagen_convertida = ImageTk.PhotoImage(imagen.resize((350, 350)))
   return imagen_convertida


def cambiar_imagen_a_label(ruta_imagen: str):
   imagen = crear_imagen_a_label(ruta_imagen)
   label_imagen_producto.config(image=imagen)
   # el garbage collector de python elimina a las imagenes antes de mostrarse, por eso se necesita que la imagen siga siendo
   # referenciada
   label_imagen_producto.image = imagen


label_instrucciones = Label(ventana_principal, text="Escanea un producto!", font=("Consolas", 18))
label_escaneando = Label(ventana_principal, text="", font=("Consolas", 18), foreground="red")
label_imagen_producto = Label(ventana_principal)
# para que la imagen inicial sea la del escaner
cambiar_imagen_a_label('./img/escaner_codigo.png')
label_nombre_producto = Label(ventana_principal, text="Nombre del producto: -------", font=("Consolas", 18))
label_precio_producto = Label(ventana_principal, text="Precio del producto: $--.--", font=("Consolas", 18))

# esta variable va ir conteniendo el codigo que se vaya introduciendo
ventana_principal.codigo_introducido = ""


def evento_tecla_presionada(e):
    # se obtiene la tecla presionada
    codigo = e.keysym
    # esa tecla se va agregando a todo el codigo que se vaya introduciendo, siendo una union de teclas
    ventana_principal.codigo_introducido += codigo
    label_escaneando.config(text="Escaneando...")
    # despues de 1500 milisegundos se ejecuta la funcion encontrar producto con todas las teclas juntadas,
    # que forman al codigo introducido
    ventana_principal.tarea = ventana_principal.after(2500, encontrar_producto)


def encontrar_producto():
    # esto es porque el escaner de barras que utilice desde mi celular agregaba un Return despues de cada codigo de barras
    ventana_principal.codigo_introducido = ventana_principal.codigo_introducido.replace("Return", "")
    # se checa al diccionario de productos, obteniendo el producto mediante la llave que seria el codigo introducido,
    # si no se encuentra al producto regrea None
    producto = productos.get(ventana_principal.codigo_introducido)
    if producto is None:
        # se tiene que checar tambien que el codigo introducido no este vacio porque como la funcion del .after()
        # se ejecuta cada 1500 milisegundos, en la ultima ejecucion cuando se inserto la ultima tecla, el codigo introducido
        # va a venir vacio
        if ventana_principal.codigo_introducido != "":
            print(ventana_principal.codigo_introducido)
            cambiar_imagen_a_label('./img/producto_no_encontrado.png')
            label_nombre_producto.config(text="Nombre del producto: Producto no encontrado...")
            label_precio_producto.config(text="Precio del producto: $--.--")
    else:
        # si encontro un producto se obtienen sus propiedades y se les ponen a los labels correspondientes
        print(ventana_principal.codigo_introducido)
        cambiar_imagen_a_label(producto['imagen'])
        label_nombre_producto.config(text=f"Nombre del producto: {producto['nombre']}")
        label_precio_producto.config(text=f"Precio del producto: ${producto['precio']}")
    label_escaneando.config(text="")
    # se resetea el codigo introducido
    ventana_principal.codigo_introducido = ""



label_instrucciones.pack()
label_escaneando.pack(pady=20)
label_imagen_producto.pack()
label_nombre_producto.pack(pady=20)
label_precio_producto.pack(pady=20)

# se agrega el evento de presionar una tecla
ventana_principal.bind('<KeyPress>', evento_tecla_presionada)
ventana_principal.mainloop()