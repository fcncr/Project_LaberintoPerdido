#INSTITUTO TECNOLÓGICO DE COSTA RICA 
#PROYECTO #2 TALLER DE PROGRAMACIÓN
#Exploradores del Laberinto Perdido
#Fabián Cambronero Núñez
#Carné: 2026079420

#Imports del proyecto 
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog, messagebox
from datetime import datetime

# -------------------------
# CONSTANTES DE DISEÑO
# -------------------------

#Areas y tamaño de la celda
AREA_MAPA = 620
TAM_MAX_CELDA = 90
TAM_MIN_CELDA = 20

#Colores que utilizaremos 
COLOR_FONDO = "#0b1120"
COLOR_PANEL = "#111827"
COLOR_PANEL_2 = "#1f2937"
COLOR_BORDE = "#b45309"
COLOR_DORADO = "#facc15"
COLOR_TEXTO = "#f9fafb"
COLOR_TEXTO_SUAVE = "#d1d5db"

COLOR_AZUL = "#2563eb"
COLOR_AZUL_2 = "#1d4ed8"
COLOR_VERDE = "#16a34a"
COLOR_VERDE_2 = "#15803d"
COLOR_GRIS = "#475569"
COLOR_MORADO = "#7c3aed"
COLOR_ROJO = "#dc2626"
COLOR_AMARILLO = "#facc15"

COLOR_HOVER = "#f8fafc"
COLOR_TEXTO_HOVER = "black"

#Colores dependiendo lo que encuentre en la matriz 
COLORES_CELDAS = {
    "E": "#16a34a",   # Entrada
    ".": "#d6c7a1",   # Camino
    "#": "#374151",   # Pared
    "T": "#facc15",   # Tesoro
    "X": "#b91c1c",   # Trampa
    "S": "#2563eb",   # Salida
    "V": "#7dd3fc",   # Visitado
    "R": "#6b7280",   # Retroceso
    "*": "#fb923c",   # Ruta final
}

#Simbolos validos que utilizaremos
SIMBOLOS_MAPA_BASE = ["E", ".", "#", "T", "X", "S"]
SIMBOLOS_MARCAS = ["V", "R", "*"]
SIMBOLOS_VALIDOS = SIMBOLOS_MAPA_BASE + SIMBOLOS_MARCAS

#Dimensiones de la matriz
MIN_FILAS = 5
MIN_COLUMNAS = 5
MAX_FILAS = 20
MAX_COLUMNAS = 20

DIRECCIONES_MOVIMIENTO = [
    [-1, 0],  # Arriba
    [0, 1],   # Derecha
    [1, 0],   # Abajo
    [0, -1]   # Izquierda
]

TIEMPO_ANIMACION = 50

# -------------------
# VARIABLES GLOBALES
# -------------------

ventana = None
canvas_mapa = None
texto_informacion = None
mapa = []

tipo_celda_seleccionado = "."
modo_edicion_activo = False
ultimo_resultado_busqueda = None

# ----------------------
# MAPA PANTALLA INICIAL
# ----------------------

def crear_mapa_demo_20x20():
    filas = [
        "####################",
        "#E....#.....#......#",
        "#.##..#.###.#.####.#",
        "#..#..#...#.#....#.#",
        "##.#.####.#.####.#.#",
        "#..#....#.#....#.#T#",
        "#.####.#.#.####.#.##",
        "#......#.#......#..#",
        "###.####.######.##.#",
        "#...#....#....#....#",
        "#.###.####.##.####.#",
        "#...#......#......T#",
        "###.#.######.#######",
        "#...#....X...#.....#",
        "#.######.#####.###.#",
        "#......#.....#...#.#",
        "#.####.#####.###.#.#",
        "#T...#.....#.....#S#",
        "#....X..#.......X..#",
        "####################",
    ]

    nueva_matriz = []

    for fila in filas:
        nueva_matriz.append(list(fila))

    return nueva_matriz


# ------------------------
# CREACION DE INTERFAZ
# ------------------------

#Crea la interfaz general
def crear_interfaz():
    crear_encabezado()
    crear_menu_superior()
    crear_zona_principal()

#Procedimiento para crear el encabezado
def crear_encabezado():
    encabezado = tk.Frame(ventana, bg=COLOR_FONDO)
    encabezado.pack(fill="x", padx=16, pady=(8, 2))

    titulo = tk.Label(
        encabezado,
        text="EXPLORADORES DEL LABERINTO PERDIDO",
        font=("Arial", 20, "bold"),
        bg=COLOR_FONDO,
        fg=COLOR_DORADO
    )
    titulo.pack(anchor="center")

#Procedimiento para crear el menu superior de botones
def crear_menu_superior():
    contenedor = tk.Frame(ventana, bg=COLOR_FONDO)
    contenedor.pack(fill="x", padx=16, pady=(2, 6))

    menu = tk.Frame(
        contenedor,
        bg=COLOR_PANEL,
        bd=2,
        relief="ridge",
        highlightbackground=COLOR_BORDE,
        highlightthickness=1
    )
    menu.pack(anchor="center", fill="x")

    #Llamadas para crear la botonera superior del programa 
    fila_1 = tk.Frame(menu, bg=COLOR_PANEL)
    fila_1.pack(anchor="center", pady=(7, 3))

    crear_boton_menu(fila_1, "Crear mapa", abrir_ventana_crear_mapa, COLOR_AZUL)
    crear_boton_menu(fila_1, "Cargar mapa", cargar_mapa, COLOR_AZUL)
    crear_boton_menu(fila_1, "Guardar mapa", guardar_mapa, COLOR_AZUL)
    crear_boton_menu(fila_1, "Editar mapa", abrir_editor_mapa, COLOR_AMARILLO, color_texto="black")

    fila_2 = tk.Frame(menu, bg=COLOR_PANEL)
    fila_2.pack(anchor="center", pady=(3, 7))

    crear_boton_menu(fila_2, "Buscar primer tesoro", buscar_primer_tesoro, COLOR_VERDE, ancho=20)
    crear_boton_menu(fila_2, "Buscar todos los tesoros", buscar_todos_los_tesoros, COLOR_VERDE, ancho=22)
    crear_boton_menu(fila_2, "Limpiar marcas", limpiar_marcas, COLOR_GRIS)
    crear_boton_menu(fila_2, "Guardar resultado", guardar_resultado, COLOR_VERDE_2, ancho=18)
    crear_boton_menu(fila_2, "Salir", salir, COLOR_ROJO, ancho=10)

#Función para crear botones
#Entradas: El lugar donde se ubica, texto que contiene, comando que ejecuta, color
#Salidas: Crea el boton 
def crear_boton_menu(padre, texto, comando, color, ancho=16, color_texto="white"):
    boton = tk.Button(
        padre,
        text=texto,
        command=comando,
        width=ancho,
        font=("Arial", 9, "bold"),
        bg=color,
        fg=color_texto,
        activebackground=COLOR_HOVER,
        activeforeground=COLOR_TEXTO_HOVER,
        relief="flat",
        bd=0,
        padx=7,
        pady=6,
        cursor="hand2"
    )

    boton.pack(side="left", padx=4)

    #EVENTOS DEL HOVER DEL MOUSE
    #Cuando el mouse esta encima
    boton.bind(
        "<Enter>",
        lambda evento: boton.config(
            bg=COLOR_HOVER,
            fg=COLOR_TEXTO_HOVER
        )
    )

    #Cuando el mouse esta afuera
    boton.bind(
        "<Leave>",
        lambda evento: boton.config(
            bg=color,
            fg=color_texto
        )
    )

#Crea la zona donde dibujaremos el mapa más adelante 
def crear_zona_principal():
    global canvas_mapa

    zona = tk.Frame(ventana, bg=COLOR_FONDO)
    zona.pack(fill="both", expand=True, padx=16, pady=(2, 10))

    panel_mapa = tk.Frame(
        zona,
        bg=COLOR_PANEL,
        bd=3,
        relief="ridge",
        highlightbackground=COLOR_BORDE,
        highlightthickness=2
    )
    panel_mapa.pack(anchor="n")

    etiqueta_mapa = tk.Label(
        panel_mapa,
        text="MAPA DEL LABERINTO",
        font=("Arial", 12, "bold"),
        bg=COLOR_PANEL,
        fg=COLOR_DORADO
    )
    etiqueta_mapa.pack(pady=(7, 3))

    contenedor_canvas = tk.Frame(
        panel_mapa,
        bg="#030712",
        bd=2,
        relief="sunken"
    )
    contenedor_canvas.pack(padx=12, pady=(3, 8))

    canvas_mapa = tk.Canvas(
        contenedor_canvas,
        width=AREA_MAPA,
        height=AREA_MAPA,
        bg="#030712",
        highlightthickness=0,
        bd=0
    )
    canvas_mapa.pack(padx=7, pady=7)

    crear_area_informacion(panel_mapa)

#Crea el area donde vamos a mostrar información respecto al programa
#Entradas: donde se va a crear el area de información 
#Salidas: Se crea el area de la información
def crear_area_informacion(padre):
    global texto_informacion

    marco_info = tk.Frame(
        padre,
        bg=COLOR_PANEL_2,
        bd=2,
        relief="ridge",
        highlightbackground=COLOR_BORDE,
        highlightthickness=1
    )
    marco_info.pack(fill="x", padx=12, pady=(0, 10))

    etiqueta = tk.Label(
        marco_info,
        text="INFORMACIÓN DEL SISTEMA",
        font=("Arial", 9, "bold"),
        bg=COLOR_PANEL_2,
        fg = "white"
    )
    etiqueta.pack(anchor="w", padx=9, pady=(5, 1))

    texto_informacion = tk.Text(
        marco_info,
        height=4,
        width=68,
        font=("Consolas", 9, "bold"),
        bg="#0f172a",
        fg=COLOR_TEXTO,
        insertbackground=COLOR_TEXTO,
        relief="flat",
        bd=0,
        padx=9,
        pady=6,
        wrap="word"
    )
    texto_informacion.pack(fill="x", padx=9, pady=(2, 8))
    texto_informacion.config(state="disabled")


# -----------------
# DIBUJO DEL MAPA
# -----------------

#Procedimiento principal para diujar el mapa
def dibujar_mapa():
    canvas_mapa.delete("all")
    dibujar_fondo_canvas()

    filas = len(mapa)

    if filas == 0:
        return

    columnas = len(mapa[0])

    if columnas == 0:
        return

    tam_celda = calcular_tamano_celda(filas, columnas)

    ancho_mapa = columnas * tam_celda
    alto_mapa = filas * tam_celda

    inicio_x = (AREA_MAPA - ancho_mapa) // 2
    inicio_y = (AREA_MAPA - alto_mapa) // 2

    # Sombra externa del tablero
    canvas_mapa.create_rectangle(
        inicio_x - 16,
        inicio_y - 16,
        inicio_x + ancho_mapa + 18,
        inicio_y + alto_mapa + 18,
        fill="#020617",
        outline=""
    )

    canvas_mapa.create_rectangle(
        inicio_x - 12,
        inicio_y - 12,
        inicio_x + ancho_mapa + 12,
        inicio_y + alto_mapa + 12,
        fill="#1c1917",
        outline="#facc15",
        width=3
    )

    canvas_mapa.create_rectangle(
        inicio_x - 6,
        inicio_y - 6,
        inicio_x + ancho_mapa + 6,
        inicio_y + alto_mapa + 6,
        outline="#92400e",
        width=3
    )
    #Recorre la matriz y va dibujando cada uno llamando a la función de dibujar_celda
    for fila in range(filas):
        for col in range(columnas):
            simbolo = mapa[fila][col]

            x1 = inicio_x + col * tam_celda
            y1 = inicio_y + fila * tam_celda
            x2 = x1 + tam_celda
            y2 = y1 + tam_celda

            dibujar_celda(x1, y1, x2, y2, simbolo, tam_celda)

#Prepara el fondo para dibujar el mapa poniendo objetos visuales
def dibujar_fondo_canvas():
    canvas_mapa.create_rectangle(
        0,
        0,
        AREA_MAPA,
        AREA_MAPA,
        fill="#020617",
        outline=""
    )

    # Fondo con sensación de cueva/ruinas
    for i in range(0, AREA_MAPA, 90):
        canvas_mapa.create_line(
            i,
            0,
            i + 150,
            AREA_MAPA,
            fill="#0f172a",
            width=1
        )

    for j in range(0, AREA_MAPA, 110):
        canvas_mapa.create_line(
            0,
            j,
            AREA_MAPA,
            j + 90,
            fill="#111827",
            width=1
        )

    # Piedras decorativas del fondo
    for i in range(18):
        x = (i * 67 + 35) % AREA_MAPA
        y = (i * 91 + 48) % AREA_MAPA

        canvas_mapa.create_oval(
            x,
            y,
            x + 10,
            y + 5,
            fill="#1f2937",
            outline=""
        )

#Función que dibujo el contenido de cada celda
#Entradas: Donde debe dibujarlo, que simbolo debe dibujar y l tamaño respectivo 
#Salidas: El dibujo en el canvas
def dibujar_celda(x1, y1, x2, y2, simbolo, tam):
    # Fondo base de cada celda
    canvas_mapa.create_rectangle(
        x1,
        y1,
        x2,
        y2,
        fill="#111827",
        outline="#020617",
        width=1
    )

    if simbolo == ".":
        dibujar_camino(x1, y1, x2, y2, tam)

    elif simbolo == "#":
        dibujar_pared(x1, y1, x2, y2, tam)

    elif simbolo == "E":
        dibujar_camino(x1, y1, x2, y2, tam)
        dibujar_entrada(x1, y1, x2, y2, tam)

    elif simbolo == "T":
        dibujar_camino(x1, y1, x2, y2, tam)
        dibujar_tesoro(x1, y1, x2, y2, tam)

    elif simbolo == "X":
        dibujar_camino(x1, y1, x2, y2, tam)
        dibujar_trampa(x1, y1, x2, y2, tam)

    elif simbolo == "S":
        dibujar_camino(x1, y1, x2, y2, tam)
        dibujar_salida(x1, y1, x2, y2, tam)

    elif simbolo == "V":
        dibujar_camino(x1, y1, x2, y2, tam)
        dibujar_visitado(x1, y1, x2, y2, tam)

    elif simbolo == "R":
        dibujar_camino(x1, y1, x2, y2, tam)
        dibujar_retroceso(x1, y1, x2, y2, tam)

    elif simbolo == "*":
        dibujar_camino(x1, y1, x2, y2, tam)
        dibujar_ruta_final(x1, y1, x2, y2, tam)

#Dibuja el camino normal del canvas
#Entradas: Ubicacion y tamaño 
#Salidas: el dibujo en el canvas
def dibujar_camino(x1, y1, x2, y2, tam):
    # Piso de piedra / arena
    canvas_mapa.create_rectangle(
        x1,
        y1,
        x2,
        y2,
        fill="#bfae82",
        outline="#7c6f4f",
        width=1
    )

    canvas_mapa.create_rectangle(
        x1 + 2,
        y1 + 2,
        x2 - 2,
        y2 - 2,
        fill="#d8c79a",
        outline=""
    )

#Dibuja las paredes del laberinto 
#Entradas: Las coordenadas y el tamaño donde debe dibujarse
#Salidas: el dibujo en el canvas
def dibujar_pared(x1, y1, x2, y2, tam):
    # Bloque oscuro principal
    canvas_mapa.create_rectangle(
        x1,
        y1,
        x2,
        y2,
        fill="#1f2937",
        outline="#020617",
        width=1
    )

    # Relieve superior
    canvas_mapa.create_rectangle(
        x1 + 2,
        y1 + 2,
        x2 - 2,
        y1 + tam * 0.32,
        fill="#4b5563",
        outline=""
    )

    # Centro de piedra
    canvas_mapa.create_rectangle(
        x1 + 3,
        y1 + tam * 0.32,
        x2 - 3,
        y2 - 3,
        fill="#374151",
        outline=""
    )

        

#Dibuja la entrada del laberinto 
#Entradas: Las coordenadas y el tamaño donde debe dibujarse
#Salidas: el dibujo en el canvas
def dibujar_entrada(x1, y1, x2, y2, tam):
    # Portal verde
    canvas_mapa.create_rectangle(
        x1 + 4,
        y1 + 4,
        x2 - 4,
        y2 - 4,
        fill="#083819",
        outline="#06b850",
        width=2
    )

    canvas_mapa.create_text(
        (x1 + x2) / 2,
        (y1 + y2) / 2 + tam * 0.06,
        text="E",
        fill="#06b850",
        font=("Arial", max(10, int(tam * 0.52)), "bold")
    )

#Dibuja el tesoro del laberinto 
#Entradas: Las coordenadas y el tamaño donde debe dibujarse
#Salidas: el dibujo en el canvas
def dibujar_tesoro(x1, y1, x2, y2, tam):
    # Cofre cuadrado base
    canvas_mapa.create_rectangle(
        x1 + tam * 0.22,
        y1 + tam * 0.28,
        x2 - tam * 0.22,
        y2 - tam * 0.18,
        fill="#8b4513",
        outline="#3b1f0f",
        width=2
    )

    # Parte superior dorada
    canvas_mapa.create_rectangle(
        x1 + tam * 0.22,
        y1 + tam * 0.28,
        x2 - tam * 0.22,
        y1 + tam * 0.44,
        fill="#facc15",
        outline="#3b1f0f",
        width=2
    )

    # Línea divisoria entre tapa y cuerpo
    canvas_mapa.create_line(
        x1 + tam * 0.22,
        y1 + tam * 0.44,
        x2 - tam * 0.22,
        y1 + tam * 0.44,
        fill="#3b1f0f",
        width=2
    )

    # Franja vertical dorada
    canvas_mapa.create_rectangle(
        x1 + tam * 0.46,
        y1 + tam * 0.28,
        x1 + tam * 0.54,
        y2 - tam * 0.18,
        fill="#facc15",
        outline="#92400e"
    )

    # Cerradura
    canvas_mapa.create_rectangle(
        x1 + tam * 0.43,
        y1 + tam * 0.54,
        x1 + tam * 0.57,
        y1 + tam * 0.70,
        fill="#50270a",
        outline="#50270a"
    )

#Dibuja las trampas del mapa
#Entradas: Las coordenadas y el tamaño donde debe dibujarse
#Salidas: el dibujo en el canvas
def dibujar_trampa(x1, y1, x2, y2, tam):
    # Base roja oscura
    canvas_mapa.create_rectangle(
        x1 + 3,
        y1 + 3,
        x2 - 3,
        y2 - 3,
        fill="#7f1d1d",
        outline="#fecaca",
        width=1
    )

    # Piso peligroso
    canvas_mapa.create_rectangle(
        x1 + 5,
        y2 - tam * 0.28,
        x2 - 5,
        y2 - 5,
        fill="#450a0a",
        outline="#111827"
    )

    # Púas rojas estilo trampa
    cantidad = 4

    if tam < 27:
        cantidad = 3

    espacio = (tam - 10) / cantidad

    for i in range(cantidad):
        p1 = x1 + 5 + i * espacio
        p2 = x1 + 5 + (i + 0.5) * espacio
        p3 = x1 + 5 + (i + 1) * espacio

        canvas_mapa.create_polygon(
            p1,
            y2 - tam * 0.28,
            p2,
            y1 + tam * 0.18,
            p3,
            y2 - tam * 0.28,
            fill="#ef4444",
            outline="#7f1d1d"
        )

#Dibuja la salida del laberinto
#Entradas: Las coordenadas y el tamaño donde debe dibujarse
#Salidas: el dibujo en el canvas
def dibujar_salida(x1, y1, x2, y2, tam):
    # Portal azul de salida
    canvas_mapa.create_rectangle(
        x1 + 4,
        y1 + 4,
        x2 - 4,
        y2 - 4,
        fill="#172554",
        outline="#6d7f96",
        width=2
    )

    canvas_mapa.create_text(
        (x1 + x2) / 2,
        (y1 + y2) / 2,
        text="S",
        fill="#92a8c5",
        font=("Arial", max(10, int(tam * 0.48)), "bold")
    )

#Dibuja la casilla visitada
#Entradas: Las coordenadas y el tamaño donde debe dibujarse
#Salidas: el dibujo en el canvas
def dibujar_visitado(x1, y1, x2, y2, tam):
    canvas_mapa.create_rectangle(
        x1 + 5,
        y1 + 5,
        x2 - 5,
        y2 - 5,
        fill="#0e7490",
        outline="#67e8f9",
        width=2
    )

    canvas_mapa.create_text(
        (x1 + x2) / 2,
        (y1 + y2) / 2,
        text="V",
        fill="white",
        font=("Arial", max(8, int(tam * 0.38)), "bold")
    )

#Dibuja la casilla retroceso
#Entradas: Las coordenadas y el tamaño donde debe dibujarse
#Salidas: el dibujo en el canvas
def dibujar_retroceso(x1, y1, x2, y2, tam):
    canvas_mapa.create_rectangle(
        x1 + 5,
        y1 + 5,
        x2 - 5,
        y2 - 5,
        fill="#4b5563",
        outline="#d1d5db",
        width=2
    )

    canvas_mapa.create_text(
        (x1 + x2) / 2,
        (y1 + y2) / 2,
        text="R",
        fill="white",
        font=("Arial", max(8, int(tam * 0.38)), "bold")
    )

#Dibuja la casilla de ruta final
#Entradas: Las coordenadas y el tamaño donde debe dibujarse
#Salidas: el dibujo en el canvas
def dibujar_ruta_final(x1, y1, x2, y2, tam):
    canvas_mapa.create_rectangle(
        x1 + 5,
        y1 + 5,
        x2 - 5,
        y2 - 5,
        fill="#fb923c",
        outline="#7c2d12",
        width=2
    )

    canvas_mapa.create_text(
        (x1 + x2) / 2,
        (y1 + y2) / 2,
        text="★",
        fill="#7c2d12",
        font=("Arial", max(8, int(tam * 0.38)), "bold")
    )

#Función para calcular el tamaño de una celda
def calcular_tamano_celda(filas, columnas):
    mayor_dimension = max(filas, columnas)
    tam = AREA_MAPA // mayor_dimension

    if tam > TAM_MAX_CELDA:
        tam = TAM_MAX_CELDA

    if tam < TAM_MIN_CELDA:
        tam = TAM_MIN_CELDA

    return tam


# ---------------------
# AREA DE INFORMACION
# ---------------------
#Función para escribir un mensaje
#Entradas: el mensaje 
#Salidas: el texto en pantalla
def escribir_informacion(mensaje, limpiar=True):
    texto_informacion.config(state="normal")

    if limpiar:
        texto_informacion.delete("1.0", "end")

    texto_informacion.insert("end", mensaje)
    texto_informacion.config(state="disabled")

#Función para agregar texto al final
#Entradas: el mensaje 
#Salidas: el texto en pantalla
def agregar_informacion(mensaje):
    texto_informacion.config(state="normal")
    texto_informacion.insert("end", "\n" + mensaje)
    texto_informacion.see("end")
    texto_informacion.config(state="disabled")

#Procedimiento para indicar el mensaje inicial de la caja de texto
def mostrar_informacion_inicial():
    filas = len(mapa)
    columnas = 0

    if filas > 0:
        columnas = len(mapa[0])

    mensaje = (
        "Aqui se mostraran mensajes para informar sobre el estado del videojuego "

    )

    escribir_informacion(mensaje)

#Cuenta la cantidad de simbolos que hay en el mapa
def contar_simbolo(simbolo):
    cantidad = 0

    for fila in mapa:
        for celda in fila:
            if celda == simbolo:
                cantidad = cantidad + 1

    return cantidad

#Función para validar el mapa de juego
#Entradas: Matriz del mapa
#Salidas: Booleano y mensaje dependiendo el resultado
def validar_mapa(matriz):
    if matriz == []:
        return False, "Error: no se puede resolver un mapa vacio."

    filas = len(matriz)

    if filas < MIN_FILAS:
        return False, "Error: el mapa debe tener al menos 5 filas."

    if filas > MAX_FILAS:
        return False, "Error: el mapa no puede tener mas de 20 filas."

    columnas = len(matriz[0])

    if columnas == 0:
        return False, "Error: el mapa tiene una fila vacia."

    if columnas < MIN_COLUMNAS:
        return False, "Error: el mapa debe tener al menos 5 columnas."

    if columnas > MAX_COLUMNAS:
        return False, "Error: el mapa no puede tener mas de 20 columnas."

    cantidad_entradas = 0
    cantidad_tesoros = 0

    for indice_fila in range(filas):
        fila = matriz[indice_fila]

        if len(fila) != columnas:
            return False, "Error: todas las filas del mapa deben tener la misma cantidad de columnas."

        for indice_columna in range(columnas):
            simbolo = fila[indice_columna]

            if simbolo not in SIMBOLOS_VALIDOS:
                return False, (
                    "Error: el mapa contiene un simbolo invalido: "
                    + str(simbolo)
                    + " en fila "
                    + str(indice_fila)
                    + ", columna "
                    + str(indice_columna)
                    + "."
                )

            if simbolo == "E":
                cantidad_entradas = cantidad_entradas + 1

            elif simbolo == "T":
                cantidad_tesoros = cantidad_tesoros + 1

    if cantidad_entradas == 0:
        return False, "Error: el mapa no tiene entrada."

    if cantidad_entradas > 1:
        return False, "Error: el mapa tiene mas de una entrada."

    if cantidad_tesoros == 0:
        return False, "Error: el mapa no contiene tesoros."

    return True, "Mapa valido."

#Mostrar mensajes cuando validamos el mapa
def mostrar_validacion_mapa():
    valido, mensaje = validar_mapa(mapa)

    escribir_informacion(mensaje)

    if valido:
        messagebox.showinfo("Validacion del mapa", mensaje)
    else:
        messagebox.showerror("Validacion del mapa", mensaje)

#Ventana para crear mapa
def abrir_ventana_crear_mapa():
    ventana_crear = tk.Toplevel(ventana)
    ventana_crear.title("Crear mapa nuevo")
    ventana_crear.geometry("360x260")
    ventana_crear.resizable(False, False)
    ventana_crear.configure(bg=COLOR_FONDO)
    ventana_crear.grab_set()

    etiqueta_titulo = tk.Label(
        ventana_crear,
        text="CREAR MAPA NUEVO",
        font=("Arial", 14, "bold"),
        bg=COLOR_FONDO,
        fg=COLOR_DORADO
    )
    etiqueta_titulo.pack(pady=(18, 8))

    etiqueta_info = tk.Label(
        ventana_crear,
        text="Ingrese dimensiones entre 5 y 20.",
        font=("Arial", 10, "bold"),
        bg=COLOR_FONDO,
        fg=COLOR_TEXTO_SUAVE
    )
    etiqueta_info.pack(pady=(0, 12))

    marco_formulario = tk.Frame(ventana_crear, bg=COLOR_PANEL, bd=2, relief="ridge")
    marco_formulario.pack(padx=20, pady=5, fill="x")

    etiqueta_filas = tk.Label(
        marco_formulario,
        text="Filas:",
        font=("Arial", 10, "bold"),
        bg=COLOR_PANEL,
        fg=COLOR_TEXTO
    )
    etiqueta_filas.grid(row=0, column=0, padx=12, pady=12, sticky="w")

    entrada_filas = tk.Entry(
        marco_formulario,
        width=10,
        font=("Arial", 10, "bold"),
        justify="center"
    )
    entrada_filas.grid(row=0, column=1, padx=12, pady=12)

    etiqueta_columnas = tk.Label(
        marco_formulario,
        text="Columnas:",
        font=("Arial", 10, "bold"),
        bg=COLOR_PANEL,
        fg=COLOR_TEXTO
    )
    etiqueta_columnas.grid(row=1, column=0, padx=12, pady=12, sticky="w")

    entrada_columnas = tk.Entry(
        marco_formulario,
        width=10,
        font=("Arial", 10, "bold"),
        justify="center"
    )
    entrada_columnas.grid(row=1, column=1, padx=12, pady=12)

    entrada_filas.insert(0, "10")
    entrada_columnas.insert(0, "10")
    #Confirmación de la creación del mapa
    def confirmar_creacion():
        global mapa

        texto_filas = entrada_filas.get()
        texto_columnas = entrada_columnas.get()

        if not texto_filas.isdigit() or not texto_columnas.isdigit():
            messagebox.showerror(
                "Error al crear mapa",
                "Las filas y columnas deben ser numeros enteros."
            )
            return

        filas = int(texto_filas)
        columnas = int(texto_columnas)

        if filas < MIN_FILAS or filas > MAX_FILAS:
            messagebox.showerror(
                "Error al crear mapa",
                "La cantidad de filas debe estar entre 5 y 20."
            )
            return

        if columnas < MIN_COLUMNAS or columnas > MAX_COLUMNAS:
            messagebox.showerror(
                "Error al crear mapa",
                "La cantidad de columnas debe estar entre 5 y 20."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar nuevo mapa",
            "Crear un mapa nuevo eliminara el mapa actual.\n\nDesea continuar?"
        )

        if not confirmar:
            return

        nuevo_mapa = []

        for fila in range(filas):
            nueva_fila = []

            for columna in range(columnas):
                nueva_fila.append(".")

            nuevo_mapa.append(nueva_fila)

        mapa = nuevo_mapa

        dibujar_mapa()

        escribir_informacion(
            "Mapa nuevo creado correctamente.\n"
            "Dimensiones: "
            + str(filas)
            + " filas x "
            + str(columnas)
            + " columnas.\n"
            "Recuerde colocar una entrada E y al menos un tesoro T antes de buscar."
        )

        ventana_crear.destroy()

    marco_botones = tk.Frame(ventana_crear, bg=COLOR_FONDO)
    marco_botones.pack(pady=16)

    boton_crear = tk.Button(
        marco_botones,
        text="Crear",
        command=confirmar_creacion,
        width=12,
        font=("Arial", 10, "bold"),
        bg=COLOR_VERDE,
        fg="white",
        relief="flat",
        cursor="hand2"
    )
    boton_crear.pack(side="left", padx=8)

    boton_cancelar = tk.Button(
        marco_botones,
        text="Cancelar",
        command=ventana_crear.destroy,
        width=12,
        font=("Arial", 10, "bold"),
        bg=COLOR_ROJO,
        fg="white",
        relief="flat",
        cursor="hand2"
    )
    boton_cancelar.pack(side="left", padx=8)     

#Procedimiento para abrir el editor del mapa
def abrir_editor_mapa():
    global modo_edicion_activo
    global tipo_celda_seleccionado

    if mapa == []:
        messagebox.showerror(
            "Editar mapa",
            "No hay ningun mapa para editar."
        )
        return

    modo_edicion_activo = True
    tipo_celda_seleccionado = "."

    canvas_mapa.bind("<Button-1>", editar_celda_canvas)

    ventana_editor = tk.Toplevel(ventana)
    ventana_editor.title("Editor de mapa")
    ventana_editor.geometry("400x360")
    ventana_editor.resizable(False, False)
    ventana_editor.configure(bg=COLOR_FONDO)
    #Procedimiento para cerrar el editor de mapas
    def cerrar_editor():
        global modo_edicion_activo

        modo_edicion_activo = False
        canvas_mapa.unbind("<Button-1>")

        escribir_informacion(
            "Modo edicion finalizado.\n"
            "Puede validar, guardar o ejecutar busquedas cuando el mapa este completo."
        )

        if ventana_editor.winfo_exists():
            ventana_editor.destroy()

    etiqueta_titulo = tk.Label(
        ventana_editor,
        text="EDITOR VISUAL DEL MAPA",
        font=("Arial", 14, "bold"),
        bg=COLOR_FONDO,
        fg=COLOR_DORADO
    )
    etiqueta_titulo.pack(pady=(16, 6))

    etiqueta_info = tk.Label(
        ventana_editor,
        text="Seleccione un tipo de celda y haga clic sobre el mapa.",
        font=("Arial", 10, "bold"),
        bg=COLOR_FONDO,
        fg=COLOR_TEXTO_SUAVE
    )
    etiqueta_info.pack(pady=(0, 10))

    marco_herramientas = tk.Frame(
        ventana_editor,
        bg=COLOR_PANEL,
        bd=2,
        relief="ridge"
    )
    marco_herramientas.pack(padx=16, pady=8, fill="both", expand=True)

    crear_boton_herramienta(marco_herramientas, "Entrada", "E", 0, 0, COLOR_VERDE)
    crear_boton_herramienta(marco_herramientas, "Camino", ".", 0, 1, "#d6c7a1", "black")
    crear_boton_herramienta(marco_herramientas, "Pared", "#", 1, 0, COLOR_GRIS)
    crear_boton_herramienta(marco_herramientas, "Tesoro", "T", 1, 1, COLOR_AMARILLO, "black")
    crear_boton_herramienta(marco_herramientas, "Trampa", "X", 2, 0, COLOR_ROJO)
    crear_boton_herramienta(marco_herramientas, "Salida", "S", 2, 1, COLOR_AZUL)

    boton_cerrar = tk.Button(
        ventana_editor,
        text="Cerrar editor",
        command=cerrar_editor,
        width=18,
        font=("Arial", 10, "bold"),
        bg=COLOR_ROJO,
        fg="white",
        relief="flat",
        cursor="hand2"
    )
    boton_cerrar.pack(pady=(4, 14))

    ventana_editor.protocol("WM_DELETE_WINDOW", cerrar_editor)

    escribir_informacion(
        "Modo edicion activado.\n"
        "Herramienta actual: Camino .\n"
        "Seleccione una herramienta y haga clic sobre una celda del mapa."
    )
#Función para crear los botones de herramientas 
#Entradas: donde va ubicado, el texto, el simbolo o valor, la fila, la columna, el color
def crear_boton_herramienta(padre, texto, simbolo, fila, columna, color, color_texto="white"):

    boton = tk.Button(
        padre,
        text=texto,
        command=lambda: seleccionar_tipo_celda(simbolo),
        width=16,
        font=("Arial", 10, "bold"),
        bg=color,
        fg=color_texto,
        activebackground=COLOR_HOVER,
        activeforeground=COLOR_TEXTO_HOVER,
        relief="flat",
        bd=0,
        padx=8,
        pady=8,
        cursor="hand2"
    )

    boton.grid(row=fila, column=columna, padx=12, pady=12)

#Guarda el simbolo que el usuario desea colocar en el mapa
#Entradas: el simbolo
#Salidas: lo guarda para utilizarlo cuando da click en el mapa
def seleccionar_tipo_celda(simbolo):

    global tipo_celda_seleccionado

    tipo_celda_seleccionado = simbolo

    escribir_informacion(
        "Herramienta seleccionada: "
        + obtener_nombre_simbolo(simbolo)
        + " ("
        + simbolo
        + ").\n"
        "Ahora haga clic sobre una celda del mapa."
    )

#Función para obtener el nombre de algún simbolo del mapa
#Entradas: Valor del simbolo 
#Salidas: String con el nombre que representa ese simbolo
def obtener_nombre_simbolo(simbolo):
    if simbolo == "E":
        return "Entrada"

    if simbolo == ".":
        return "Camino"

    if simbolo == "#":
        return "Pared"

    if simbolo == "T":
        return "Tesoro"

    if simbolo == "X":
        return "Trampa"

    if simbolo == "S":
        return "Salida"

    return "Desconocido"

#Función que detecta el click sobre el mapa y lo edita
#Entradas: el evento 
#Salidas: la modificación en el mapa
def editar_celda_canvas(evento):

    if not modo_edicion_activo:
        return

    posicion = obtener_celda_por_click(evento.x, evento.y)

    if posicion is None:
        escribir_informacion(
            "Clic fuera del mapa.\n"
            "Seleccione una celda dentro de la cuadricula."
        )
        return

    fila = posicion[0]
    columna = posicion[1]

    colocar_celda(fila, columna)

#Devuelve la celda donde le dimos click
#Entradas: Los pixeles donde se dio el click
#Salidas: las coordenadas de la matriz
def obtener_celda_por_click(x, y):

    filas = len(mapa)

    if filas == 0:
        return None

    columnas = len(mapa[0])

    if columnas == 0:
        return None

    tam_celda = calcular_tamano_celda(filas, columnas)

    ancho_mapa = columnas * tam_celda
    alto_mapa = filas * tam_celda

    inicio_x = (AREA_MAPA - ancho_mapa) // 2
    inicio_y = (AREA_MAPA - alto_mapa) // 2

    fin_x = inicio_x + ancho_mapa
    fin_y = inicio_y + alto_mapa

    if x < inicio_x or x >= fin_x:
        return None

    if y < inicio_y or y >= fin_y:
        return None

    columna = (x - inicio_x) // tam_celda
    fila = (y - inicio_y) // tam_celda

    return [fila, columna]

#Coloca el valor que deseamos sobre donde dimos click
#Entradas: la fila y la columa
#salidas: coloca el simbolo en el mapa
def colocar_celda(fila, columna):
    global mapa

    simbolo = tipo_celda_seleccionado

    if simbolo == "E":
        eliminar_entrada_existente()

    mapa[fila][columna] = simbolo

    dibujar_mapa()

    escribir_informacion(
        "Celda modificada correctamente.\n"
        "Fila: "
        + str(fila)
        + " | Columna: "
        + str(columna)
        + "\nNuevo valor: "
        + obtener_nombre_simbolo(simbolo)
        + " ("
        + simbolo
        + ")"
    )

#Procedimiento para eliminar una E del mapa si se van a colocar 2 
def eliminar_entrada_existente():
    for fila in range(len(mapa)):
        for columna in range(len(mapa[fila])):
            if mapa[fila][columna] == "E":
                mapa[fila][columna] = "."

#Permite cargar mapa desde un archivo txt
def cargar_mapa():

    global mapa

    ruta_archivo = filedialog.askopenfilename(
        title="Seleccionar archivo de mapa",
        filetypes=[
            ("Archivos de texto", "*.txt"),
            ("Todos los archivos", "*.*")
        ]
    )

    if ruta_archivo == "":
        escribir_informacion(
            "Carga cancelada.\n"
            "No se selecciono ningun archivo."
        )
        return

    try:
        archivo = open(ruta_archivo, "r", encoding="utf-8")
        lineas = archivo.readlines()
        archivo.close()

        nuevo_mapa = []

        for linea in lineas:
            linea = linea.strip()

            if linea != "":
                nueva_fila = list(linea)
                nuevo_mapa.append(nueva_fila)

        valido, mensaje = validar_mapa(nuevo_mapa)

        if not valido:
            escribir_informacion(
                "No se pudo cargar el mapa.\n"
                + mensaje
            )

            messagebox.showerror(
                "Archivo invalido",
                mensaje
            )

            return

        mapa = nuevo_mapa

        dibujar_mapa()

        escribir_informacion(
            "Mapa cargado correctamente.\n"
            "Archivo: "
            + ruta_archivo
            + "\nDimensiones: "
            + str(len(mapa))
            + " filas x "
            + str(len(mapa[0]))
            + " columnas."
        )

        messagebox.showinfo(
            "Mapa cargado",
            "El mapa se cargo correctamente."
        )

    except Exception as error:
        escribir_informacion(
            "Error al cargar el archivo.\n"
            + str(error)
        )

        messagebox.showerror(
            "Error al cargar archivo",
            "No se pudo cargar el archivo.\n\n"
            + str(error)
        )    


# -----------------
# GUARDADO DE MAPAS
# -----------------
#Limpia el mapa antes de guardarlo
#Entradas: Matriz con el mapa
#Salidas: Mapa limpio
def limpiar_mapa_para_guardar(matriz):
    mapa_limpio = []

    for fila in matriz:
        nueva_fila = []

        for celda in fila:
            if celda == "V" or celda == "R" or celda == "*":
                nueva_fila.append(".")
            else:
                nueva_fila.append(celda)

        mapa_limpio.append(nueva_fila)

    return mapa_limpio

#Función que convierte la matriz en texto 
#Entradas: La matriz del mapa
#Salidas: el texto listo para guardar 
def convertir_mapa_a_texto(matriz):
    texto = ""

    for fila in matriz:
        linea = ""

        for celda in fila:
            linea = linea + celda

        texto = texto + linea + "\n"

    return texto

#Procedimiento que guarda el mapa actual en un archivo txt
def guardar_mapa():

    if mapa == []:
        messagebox.showerror(
            "Guardar mapa",
            "No hay ningun mapa para guardar."
        )
        return

    mapa_limpio = limpiar_mapa_para_guardar(mapa)

    valido, mensaje = validar_mapa(mapa_limpio)

    if not valido:
        escribir_informacion(
            "No se puede guardar el mapa.\n"
            + mensaje
        )

        messagebox.showerror(
            "Mapa invalido",
            "El mapa no cumple las reglas del proyecto.\n\n"
            + mensaje
        )
        return

    ruta_archivo = filedialog.asksaveasfilename(
        title="Guardar mapa",
        defaultextension=".txt",
        filetypes=[
            ("Archivos de texto", "*.txt"),
            ("Todos los archivos", "*.*")
        ]
    )

    if ruta_archivo == "":
        escribir_informacion(
            "Guardado cancelado.\n"
            "No se selecciono ninguna ubicacion."
        )
        return

    try:
        texto_mapa = convertir_mapa_a_texto(mapa_limpio)

        archivo = open(ruta_archivo, "w", encoding="utf-8")
        archivo.write(texto_mapa)
        archivo.close()

        escribir_informacion(
            "Mapa guardado correctamente.\n"
            "Archivo: "
            + ruta_archivo
            + "\nFormato: archivo .txt limpio, sin marcas de busqueda."
        )

        messagebox.showinfo(
            "Mapa guardado",
            "El mapa se guardo correctamente."
        )

    except Exception as error:
        escribir_informacion(
            "Error al guardar el mapa.\n"
            + str(error)
        )

        messagebox.showerror(
            "Error al guardar",
            "No se pudo guardar el mapa.\n\n"
            + str(error)
        )


# -------------------
# LIMPIEZA DE MARCAS
# -------------------

#Procedimiento para limpiar las marcas del mapa
def limpiar_marcas():
    global mapa

    if mapa == []:
        messagebox.showerror(
            "Limpiar marcas",
            "No hay ningun mapa para limpiar."
        )
        return

    cantidad_limpiadas = 0

    for fila in range(len(mapa)):
        for columna in range(len(mapa[fila])):
            if mapa[fila][columna] == "V" or mapa[fila][columna] == "R" or mapa[fila][columna] == "*":
                mapa[fila][columna] = "."
                cantidad_limpiadas = cantidad_limpiadas + 1

    dibujar_mapa()

    escribir_informacion(
        "Limpieza de marcas finalizada.\n"
        "Casillas limpiadas: "
        + str(cantidad_limpiadas)
        + ".\n"
        "Se conservaron entrada, tesoros, paredes, trampas y salidas."
    )

    if cantidad_limpiadas == 0:
        messagebox.showinfo(
            "Limpiar marcas",
            "No habia marcas de busqueda para limpiar."
        )
    else:
        messagebox.showinfo(
            "Limpiar marcas",
            "Las marcas de busqueda fueron eliminadas correctamente."
        )

# -----------------------------------
# UTILIDADES BASE PARA BACKTRACKING
# -----------------------------------

def buscar_entrada(matriz):
    """
    Busca la posicion de la entrada E dentro del mapa.
    Retorna [fila, columna] si la encuentra.
    Retorna None si no existe entrada.
    """

    for fila in range(len(matriz)):
        for columna in range(len(matriz[fila])):
            if matriz[fila][columna] == "E":
                return [fila, columna]

    return None


def contar_tesoros_matriz(matriz):
    """
    Cuenta cuantos tesoros T existen en el mapa.
    Esta funcion solo cuenta tesoros para el resumen.
    No se usa para guiar el camino del algoritmo.
    """

    cantidad = 0

    for fila in range(len(matriz)):
        for columna in range(len(matriz[fila])):
            if matriz[fila][columna] == "T":
                cantidad = cantidad + 1

    return cantidad


def copiar_matriz(matriz):
    """
    Crea una copia independiente de una matriz.
    Se usara para guardar el mapa original antes de modificarlo con V, R o *.
    """

    copia = []

    for fila in matriz:
        nueva_fila = []

        for celda in fila:
            nueva_fila.append(celda)

        copia.append(nueva_fila)

    return copia


def posicion_dentro_del_mapa(matriz, fila, columna):
    """
    Verifica si una posicion esta dentro de los limites del mapa.
    """

    if fila < 0:
        return False

    if columna < 0:
        return False

    if fila >= len(matriz):
        return False

    if len(matriz) == 0:
        return False

    if columna >= len(matriz[0]):
        return False

    return True


def es_celda_transitable(matriz, fila, columna):
    """
    Verifica si una celda puede ser recorrida por el explorador.
    Son transitables:
    E, ., T y S

    No son transitables:
    #, X, V, R y *
    """

    if not posicion_dentro_del_mapa(matriz, fila, columna):
        return False

    celda = matriz[fila][columna]

    if celda == "E":
        return True

    if celda == ".":
        return True

    if celda == "T":
        return True

    if celda == "S":
        return True

    return False


def obtener_nombre_direccion(indice):
    """
    Retorna el nombre de una direccion segun el orden obligatorio.
    """

    if indice == 0:
        return "Arriba"

    if indice == 1:
        return "Derecha"

    if indice == 2:
        return "Abajo"

    if indice == 3:
        return "Izquierda"

    return "Desconocida"


def probar_utilidades_backtracking():
    """
    Funcion temporal para comprobar que las utilidades base funcionan.
    Esta prueba no resuelve el laberinto todavia.
    """

    valido, mensaje = validar_mapa(mapa)

    if not valido:
        escribir_informacion(
            "No se pueden probar las utilidades.\n"
            + mensaje
        )

        messagebox.showerror(
            "Mapa invalido",
            mensaje
        )
        return

    entrada = buscar_entrada(mapa)
    total_tesoros = contar_tesoros_matriz(mapa)
    copia = copiar_matriz(mapa)

    mensaje_prueba = (
        "Utilidades base del backtracking funcionando correctamente.\n"
        "Entrada encontrada en fila "
        + str(entrada[0])
        + ", columna "
        + str(entrada[1])
        + ".\n"
        "Tesoros totales en el mapa: "
        + str(total_tesoros)
        + ".\n"
        "Copia del mapa creada correctamente: "
        + str(len(copia))
        + " filas x "
        + str(len(copia[0]))
        + " columnas.\n"
        "Orden de movimiento preparado: Arriba, Derecha, Abajo, Izquierda."
    )

    escribir_informacion(mensaje_prueba)

    messagebox.showinfo(
        "Prueba de utilidades",
        "Las utilidades base funcionan correctamente."
    )

# =========================================================
# BUSQUEDA DEL PRIMER TESORO CON BACKTRACKING ANIMADO
# =========================================================

def buscar_primer_tesoro():
    """
    Ejecuta la busqueda del primer tesoro accesible usando backtracking recursivo.
    El algoritmo no conoce la posicion previa del tesoro.
    Detecta el tesoro solamente cuando llega a una celda T.
    La visualizacion se realiza con animacion usando ventana.after().
    """

    global mapa

    valido, mensaje = validar_mapa(mapa)

    if not valido:
        escribir_informacion(
            "No se puede iniciar la busqueda.\n"
            + mensaje
        )

        messagebox.showerror(
            "Mapa invalido",
            mensaje
        )
        return

    limpiar_marcas_sin_mensaje()

    mapa_original = copiar_matriz(mapa)
    entrada = buscar_entrada(mapa)

    if entrada is None:
        escribir_informacion(
            "No se puede iniciar la busqueda.\n"
            "No se encontro entrada E."
        )

        messagebox.showerror(
            "Busqueda",
            "No se encontro entrada E."
        )
        return

    estadisticas = {
        "visitadas": 0,
        "retrocesos": 0,
        "tesoro_encontrado": None
    }

    ruta_actual = []
    pasos_animacion = []

    escribir_informacion(
        "Busqueda iniciada.\n"
        "Explorando con backtracking recursivo...\n"
        "Orden: Arriba, Derecha, Abajo, Izquierda."
    )

    encontrado = backtracking_primer_tesoro(
        entrada[0],
        entrada[1],
        ruta_actual,
        estadisticas,
        pasos_animacion
    )

    if encontrado:
        agregar_pasos_ruta_final(
            ruta_actual,
            mapa_original,
            pasos_animacion
        )

    mapa = copiar_matriz(mapa_original)
    dibujar_mapa()

    animar_pasos_busqueda(
        pasos_animacion,
        0,
        mapa_original,
        encontrado,
        estadisticas
    )


def backtracking_primer_tesoro(fila, columna, ruta_actual, estadisticas, pasos_animacion):
    """
    Funcion recursiva de backtracking.
    Intenta encontrar el primer tesoro accesible desde la posicion actual.
    Orden de exploracion obligatorio:
    arriba, derecha, abajo, izquierda.
    """

    if not posicion_dentro_del_mapa(mapa, fila, columna):
        return False

    if not es_celda_transitable(mapa, fila, columna):
        return False

    celda_actual = mapa[fila][columna]

    ruta_actual.append([fila, columna])

    if celda_actual == "T":
        estadisticas["tesoro_encontrado"] = [fila, columna]
        return True

    if celda_actual != "E" and celda_actual != "S":
        mapa[fila][columna] = "V"
        estadisticas["visitadas"] = estadisticas["visitadas"] + 1
        pasos_animacion.append(["V", fila, columna])

    for indice in range(len(DIRECCIONES_MOVIMIENTO)):
        movimiento = DIRECCIONES_MOVIMIENTO[indice]

        nueva_fila = fila + movimiento[0]
        nueva_columna = columna + movimiento[1]

        if backtracking_primer_tesoro(
            nueva_fila,
            nueva_columna,
            ruta_actual,
            estadisticas,
            pasos_animacion
        ):
            return True

    ruta_actual.pop()

    if celda_actual != "E" and celda_actual != "S":
        mapa[fila][columna] = "R"
        estadisticas["retrocesos"] = estadisticas["retrocesos"] + 1
        pasos_animacion.append(["R", fila, columna])

    return False


def agregar_pasos_ruta_final(ruta_actual, mapa_original, pasos_animacion):
    """
    Agrega a la animacion las casillas que forman parte de la ruta final.
    No reemplaza visualmente E, T ni S.
    """

    for posicion in ruta_actual:
        fila = posicion[0]
        columna = posicion[1]

        simbolo_original = mapa_original[fila][columna]

        if simbolo_original != "E" and simbolo_original != "T" and simbolo_original != "S":
            pasos_animacion.append(["*", fila, columna])


def animar_pasos_busqueda(pasos_animacion, indice, mapa_original, encontrado, estadisticas):
    """
    Muestra paso a paso la busqueda usando ventana.after().
    Al terminar, registra el resultado para poder guardarlo.
    """

    if indice >= len(pasos_animacion):
        finalizar_animacion_busqueda(encontrado, estadisticas, mapa_original)
        return

    paso = pasos_animacion[indice]

    tipo_marca = paso[0]
    fila = paso[1]
    columna = paso[2]

    aplicar_paso_animacion(tipo_marca, fila, columna, mapa_original)

    dibujar_mapa()

    ventana.after(
        TIEMPO_ANIMACION,
        lambda: animar_pasos_busqueda(
            pasos_animacion,
            indice + 1,
            mapa_original,
            encontrado,
            estadisticas
        )
    )


def aplicar_paso_animacion(tipo_marca, fila, columna, mapa_original):
    """
    Aplica una marca visual al mapa durante la animacion.
    Conserva entrada, tesoros, paredes, trampas y salidas.
    """

    global mapa

    simbolo_original = mapa_original[fila][columna]

    if simbolo_original == "E":
        return

    if simbolo_original == "T":
        return

    if simbolo_original == "S":
        return

    if simbolo_original == "#":
        return

    if simbolo_original == "X":
        return

    mapa[fila][columna] = tipo_marca


def finalizar_animacion_busqueda(encontrado, estadisticas, mapa_original):
    """
    Muestra el resumen final despues de terminar la animacion.
    Tambien registra el resultado para poder guardarlo en archivo .txt.
    """

    if encontrado:
        fila_tesoro = estadisticas["tesoro_encontrado"][0]
        columna_tesoro = estadisticas["tesoro_encontrado"][1]

        mensaje_final = (
            "Busqueda finalizada: tesoro encontrado.\n"
            "Posicion del tesoro: fila "
            + str(fila_tesoro)
            + ", columna "
            + str(columna_tesoro)
            + ".\n"
            "Casillas visitadas: "
            + str(estadisticas["visitadas"])
            + ".\n"
            "Retrocesos realizados: "
            + str(estadisticas["retrocesos"])
            + "."
        )

        resultado_reporte = (
            "Se encontro un tesoro accesible desde la entrada en fila "
            + str(fila_tesoro)
            + ", columna "
            + str(columna_tesoro)
            + "."
        )

        registrar_ultimo_resultado_busqueda(
            "Buscar primer tesoro",
            mapa_original,
            mapa,
            contar_tesoros_matriz(mapa_original),
            [[fila_tesoro, columna_tesoro]],
            resultado_reporte
        )

        escribir_informacion(mensaje_final)

        messagebox.showinfo(
            "Tesoro encontrado",
            "Se encontro un tesoro en fila "
            + str(fila_tesoro)
            + ", columna "
            + str(columna_tesoro)
            + "."
        )

    else:
        mensaje_final = (
            "Busqueda finalizada: no se encontro ningun tesoro accesible.\n"
            "Casillas visitadas: "
            + str(estadisticas["visitadas"])
            + ".\n"
            "Retrocesos realizados: "
            + str(estadisticas["retrocesos"])
            + "."
        )

        registrar_ultimo_resultado_busqueda(
            "Buscar primer tesoro",
            mapa_original,
            mapa,
            contar_tesoros_matriz(mapa_original),
            [],
            "No se encontro ningun tesoro accesible desde la entrada."
        )

        escribir_informacion(mensaje_final)

        messagebox.showwarning(
            "Tesoro no encontrado",
            "No se encontro ningun tesoro accesible desde la entrada."
        )


def limpiar_marcas_sin_mensaje():
    """
    Limpia V, R y * sin mostrar ventanas emergentes.
    Se usa internamente antes de iniciar una nueva busqueda.
    """

    global mapa

    for fila in range(len(mapa)):
        for columna in range(len(mapa[fila])):
            if mapa[fila][columna] == "V" or mapa[fila][columna] == "R" or mapa[fila][columna] == "*":
                mapa[fila][columna] = "."

# =========================================================
# BUSQUEDA DE TODOS LOS TESOROS CON BACKTRACKING ANIMADO
# =========================================================

def buscar_todos_los_tesoros():
    """
    Ejecuta una busqueda completa para encontrar todos los tesoros accesibles.
    El algoritmo no conoce previamente las posiciones de los tesoros.
    Los registra solamente cuando llega a una celda T durante la exploracion.
    """

    global mapa

    valido, mensaje = validar_mapa(mapa)

    if not valido:
        escribir_informacion(
            "No se puede iniciar la busqueda de todos los tesoros.\n"
            + mensaje
        )

        messagebox.showerror(
            "Mapa invalido",
            mensaje
        )
        return

    limpiar_marcas_sin_mensaje()

    mapa_original = copiar_matriz(mapa)
    entrada = buscar_entrada(mapa)
    total_tesoros = contar_tesoros_matriz(mapa)

    if entrada is None:
        escribir_informacion(
            "No se puede iniciar la busqueda.\n"
            "No se encontro entrada E."
        )

        messagebox.showerror(
            "Busqueda",
            "No se encontro entrada E."
        )
        return

    visitados = crear_matriz_visitados(len(mapa), len(mapa[0]))

    estadisticas = {
        "visitadas": 0,
        "retrocesos": 0,
        "total_tesoros": total_tesoros,
        "tesoros_encontrados": [],
        "rutas_encontradas": []
    }

    ruta_actual = []
    pasos_animacion = []

    escribir_informacion(
        "Busqueda de todos los tesoros iniciada.\n"
        "Explorando todos los caminos posibles con backtracking...\n"
        "Orden: Arriba, Derecha, Abajo, Izquierda."
    )

    backtracking_todos_los_tesoros(
        entrada[0],
        entrada[1],
        visitados,
        ruta_actual,
        estadisticas,
        pasos_animacion
    )

    agregar_pasos_rutas_todos_los_tesoros(
        estadisticas["rutas_encontradas"],
        mapa_original,
        pasos_animacion
    )

    mapa = copiar_matriz(mapa_original)
    dibujar_mapa()

    animar_pasos_busqueda_todos(
        pasos_animacion,
        0,
        mapa_original,
        estadisticas
    )


def crear_matriz_visitados(filas, columnas):
    """
    Crea una matriz booleana para controlar las celdas ya visitadas.
    Esto evita ciclos infinitos sin depender solamente de cambiar simbolos del mapa.
    """

    visitados = []

    for fila in range(filas):
        nueva_fila = []

        for columna in range(columnas):
            nueva_fila.append(False)

        visitados.append(nueva_fila)

    return visitados


def backtracking_todos_los_tesoros(fila, columna, visitados, ruta_actual, estadisticas, pasos_animacion):
    """
    Backtracking recursivo para explorar todos los caminos accesibles.
    Continúa explorando aun despues de encontrar un tesoro.
    """

    if not posicion_dentro_del_mapa(mapa, fila, columna):
        return

    if not es_celda_transitable(mapa, fila, columna):
        return

    if visitados[fila][columna]:
        return

    visitados[fila][columna] = True

    celda_actual = mapa[fila][columna]
    ruta_actual.append([fila, columna])

    if celda_actual == "T":
        tesoro_ya_registrado = False

        for tesoro in estadisticas["tesoros_encontrados"]:
            if tesoro[0] == fila and tesoro[1] == columna:
                tesoro_ya_registrado = True

        if not tesoro_ya_registrado:
            estadisticas["tesoros_encontrados"].append([fila, columna])
            estadisticas["rutas_encontradas"].append(copiar_ruta(ruta_actual))

    elif celda_actual != "E" and celda_actual != "S":
        estadisticas["visitadas"] = estadisticas["visitadas"] + 1
        pasos_animacion.append(["V", fila, columna])

    for indice in range(len(DIRECCIONES_MOVIMIENTO)):
        movimiento = DIRECCIONES_MOVIMIENTO[indice]

        nueva_fila = fila + movimiento[0]
        nueva_columna = columna + movimiento[1]

        backtracking_todos_los_tesoros(
            nueva_fila,
            nueva_columna,
            visitados,
            ruta_actual,
            estadisticas,
            pasos_animacion
        )

    ruta_actual.pop()

    if celda_actual != "E" and celda_actual != "T" and celda_actual != "S":
        estadisticas["retrocesos"] = estadisticas["retrocesos"] + 1
        pasos_animacion.append(["R", fila, columna])


def copiar_ruta(ruta):
    """
    Crea una copia independiente de una ruta.
    """

    copia = []

    for posicion in ruta:
        copia.append([posicion[0], posicion[1]])

    return copia


def agregar_pasos_rutas_todos_los_tesoros(rutas_encontradas, mapa_original, pasos_animacion):
    """
    Agrega al final de la animacion las rutas hacia los tesoros encontrados.
    Se agregan al final para que los retrocesos no borren visualmente la ruta final.
    """

    for ruta in rutas_encontradas:
        for posicion in ruta:
            fila = posicion[0]
            columna = posicion[1]

            simbolo_original = mapa_original[fila][columna]

            if simbolo_original != "E" and simbolo_original != "T" and simbolo_original != "S":
                pasos_animacion.append(["*", fila, columna])


def animar_pasos_busqueda_todos(pasos_animacion, indice, mapa_original, estadisticas):
    """
    Anima la busqueda completa de todos los tesoros usando ventana.after().
    """

    if indice >= len(pasos_animacion):
        finalizar_animacion_busqueda_todos(estadisticas, mapa_original)
        return

    paso = pasos_animacion[indice]

    tipo_marca = paso[0]
    fila = paso[1]
    columna = paso[2]

    aplicar_paso_animacion(tipo_marca, fila, columna, mapa_original)

    dibujar_mapa()

    ventana.after(
        TIEMPO_ANIMACION,
        lambda: animar_pasos_busqueda_todos(
            pasos_animacion,
            indice + 1,
            mapa_original,
            estadisticas
        )
    )


def finalizar_animacion_busqueda_todos(estadisticas,mapa_original):
    """
    Muestra el resumen final de la busqueda de todos los tesoros.
    """

    total_tesoros = estadisticas["total_tesoros"]
    encontrados = len(estadisticas["tesoros_encontrados"])

    posiciones = obtener_texto_posiciones_tesoros(
        estadisticas["tesoros_encontrados"]
    )

    if encontrados == total_tesoros:
        resultado = "Todos los tesoros son accesibles desde la entrada."
    else:
        resultado = "Existe al menos un tesoro inaccesible."
    
    registrar_ultimo_resultado_busqueda(
        "Buscar todos los tesoros",
        mapa_original,
        mapa,
        total_tesoros,
        estadisticas["tesoros_encontrados"],
        resultado
    )

    mensaje_final = (
        "Busqueda de todos los tesoros finalizada.\n"
        "Tesoros totales: "
        + str(total_tesoros)
        + ".\n"
        "Tesoros encontrados: "
        + str(encontrados)
        + ".\n"
        + posiciones
        + "\nCasillas visitadas: "
        + str(estadisticas["visitadas"])
        + ".\n"
        "Retrocesos realizados: "
        + str(estadisticas["retrocesos"])
        + ".\n"
        + resultado
    )

    escribir_informacion(mensaje_final)

    if encontrados == 0:
        messagebox.showwarning(
            "Busqueda finalizada",
            "No se encontro ningun tesoro accesible."
        )

    elif encontrados == total_tesoros:
        messagebox.showinfo(
            "Busqueda finalizada",
            "Se encontraron todos los tesoros accesibles.\n\n"
            "Tesoros encontrados: "
            + str(encontrados)
            + " de "
            + str(total_tesoros)
            + "."
        )

    else:
        messagebox.showwarning(
            "Busqueda finalizada",
            "No todos los tesoros son accesibles.\n\n"
            "Tesoros encontrados: "
            + str(encontrados)
            + " de "
            + str(total_tesoros)
            + "."
        )


def obtener_texto_posiciones_tesoros(tesoros_encontrados):
    """
    Construye un texto con las posiciones de los tesoros encontrados.
    """

    if len(tesoros_encontrados) == 0:
        return "Posiciones de tesoros encontrados: ninguna."

    texto = "Posiciones de tesoros encontrados:"

    for indice in range(len(tesoros_encontrados)):
        tesoro = tesoros_encontrados[indice]

        texto = (
            texto
            + "\nTesoro "
            + str(indice + 1)
            + ": fila "
            + str(tesoro[0])
            + ", columna "
            + str(tesoro[1])
        )

    return texto

# =========================================================
# GUARDADO DE RESULTADOS DE BUSQUEDA
# =========================================================

def registrar_ultimo_resultado_busqueda(
    tipo_busqueda,
    mapa_original,
    mapa_final,
    total_tesoros,
    tesoros_encontrados,
    resultado_final
):
    """
    Guarda en memoria los datos de la ultima busqueda realizada.
    Estos datos se usaran cuando el usuario presione Guardar resultado.
    """

    global ultimo_resultado_busqueda

    ultimo_resultado_busqueda = {
        "tipo_busqueda": tipo_busqueda,
        "mapa_original": copiar_matriz(mapa_original),
        "mapa_final": copiar_matriz(mapa_final),
        "total_tesoros": total_tesoros,
        "tesoros_encontrados": copiar_lista_posiciones(tesoros_encontrados),
        "resultado_final": resultado_final,
        "fecha_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }


def copiar_lista_posiciones(lista_posiciones):
    """
    Crea una copia independiente de una lista de posiciones.
    """

    copia = []

    for posicion in lista_posiciones:
        copia.append([posicion[0], posicion[1]])

    return copia


def generar_texto_reporte_resultado():
    """
    Genera el contenido completo del reporte de busqueda.
    """

    if ultimo_resultado_busqueda is None:
        return None

    texto = ""

    texto = texto + "EXPLORADORES DEL LABERINTO PERDIDO\n"
    texto = texto + "REPORTE DE BUSQUEDA\n"
    texto = texto + "====================================\n\n"

    texto = texto + "Fecha y hora de generacion:\n"
    texto = texto + ultimo_resultado_busqueda["fecha_hora"] + "\n\n"

    texto = texto + "Tipo de busqueda:\n"
    texto = texto + ultimo_resultado_busqueda["tipo_busqueda"] + "\n\n"

    texto = texto + "Mapa original:\n"
    texto = texto + convertir_mapa_a_texto(ultimo_resultado_busqueda["mapa_original"])
    texto = texto + "\n"

    texto = texto + "Mapa final despues de la busqueda:\n"
    texto = texto + convertir_mapa_a_texto(ultimo_resultado_busqueda["mapa_final"])
    texto = texto + "\n"

    texto = texto + "Tesoros totales:\n"
    texto = texto + str(ultimo_resultado_busqueda["total_tesoros"]) + "\n\n"

    texto = texto + "Tesoros encontrados:\n"
    texto = texto + str(len(ultimo_resultado_busqueda["tesoros_encontrados"])) + "\n\n"

    texto = texto + "Posiciones de tesoros encontrados:\n"

    if len(ultimo_resultado_busqueda["tesoros_encontrados"]) == 0:
        texto = texto + "Ninguna.\n"
    else:
        for indice in range(len(ultimo_resultado_busqueda["tesoros_encontrados"])):
            tesoro = ultimo_resultado_busqueda["tesoros_encontrados"][indice]

            texto = (
                texto
                + "Tesoro "
                + str(indice + 1)
                + ": fila "
                + str(tesoro[0])
                + ", columna "
                + str(tesoro[1])
                + "\n"
            )

    texto = texto + "\nResultado:\n"
    texto = texto + ultimo_resultado_busqueda["resultado_final"] + "\n"

    return texto


def guardar_resultado():
    """
    Guarda en un archivo .txt el resultado de la ultima busqueda realizada.
    """

    if ultimo_resultado_busqueda is None:
        messagebox.showerror(
            "Guardar resultado",
            "No hay ningun resultado de busqueda para guardar.\n\n"
            "Primero ejecute Buscar primer tesoro o Buscar todos los tesoros."
        )

        escribir_informacion(
            "No se puede guardar resultado.\n"
            "Primero debe ejecutar una busqueda."
        )
        return

    ruta_archivo = filedialog.asksaveasfilename(
        title="Guardar resultado de busqueda",
        defaultextension=".txt",
        filetypes=[
            ("Archivos de texto", "*.txt"),
            ("Todos los archivos", "*.*")
        ]
    )

    if ruta_archivo == "":
        escribir_informacion(
            "Guardado de resultado cancelado.\n"
            "No se selecciono ninguna ubicacion."
        )
        return

    try:
        texto_reporte = generar_texto_reporte_resultado()

        archivo = open(ruta_archivo, "w", encoding="utf-8")
        archivo.write(texto_reporte)
        archivo.close()

        escribir_informacion(
            "Resultado guardado correctamente.\n"
            "Archivo: "
            + ruta_archivo
        )

        messagebox.showinfo(
            "Resultado guardado",
            "El resultado de la busqueda se guardo correctamente."
        )

    except Exception as error:
        escribir_informacion(
            "Error al guardar el resultado.\n"
            + str(error)
        )

        messagebox.showerror(
            "Error al guardar resultado",
            "No se pudo guardar el resultado.\n\n"
            + str(error)
        )

# =========================================================
# ACCIONES TEMPORALES
# =========================================================

def accion_pendiente():
    escribir_informacion(
        "Estado: accion pendiente de implementar.\n"
        "La base visual ya esta lista para conectar esta funcion en la siguiente fase."
    )

    messagebox.showinfo(
        "Proxima fase",
        "Esta accion se implementara despues de dejar lista la base visual."
    )


def abrir_editor_placeholder():
    escribir_informacion(
        "Estado: modo editar mapa seleccionado.\n"
        "Las herramientas de celdas no estaran en el menu principal. "
        "Se abriran en una seccion separada para editar el mapa con orden."
    )

    messagebox.showinfo(
        "Editar mapa",
        "Correcto: las herramientas de celdas no iran en el menu principal.\n\n"
        "En la siguiente fase abriremos un modo de edicion separado con sus propias herramientas."
    )


def salir():
    confirmar = messagebox.askyesno(
        "Salir del programa",
        "Desea cerrar Exploradores del Laberinto Perdido?"
    )

    if confirmar:
        ventana.destroy()


# =========================================================
# INICIO DEL PROGRAMA
# =========================================================

ventana = tk.Tk()
ventana.title("Exploradores del Laberinto Perdido")
ventana.geometry("800x990")
ventana.minsize(800, 820)
ventana.configure(bg=COLOR_FONDO)

mapa = crear_mapa_demo_20x20()

crear_interfaz()
dibujar_mapa()
mostrar_informacion_inicial()

ventana.protocol("WM_DELETE_WINDOW", salir)
ventana.mainloop()