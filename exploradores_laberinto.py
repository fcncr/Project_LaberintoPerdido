# Exploradores del Laberinto Perdido
# Interfaz grafica base - version procedural ajustada
# Lenguaje: Python
# Interfaz: Tkinter

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog, messagebox

# =========================================================
# CONSTANTES DE DISENO
# =========================================================

AREA_MAPA = 620
TAM_MAX_CELDA = 90
TAM_MIN_CELDA = 20

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


# =========================================================
# VARIABLES GLOBALES
# =========================================================

ventana = None
canvas_mapa = None
texto_informacion = None
mapa = []


# =========================================================
# MAPAS EN ARCHIVOS
# =========================================================

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



# =========================================================
# CREACION DE INTERFAZ
# =========================================================

def crear_interfaz():
    crear_encabezado()
    crear_menu_superior()
    crear_zona_principal()


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

    subtitulo = tk.Label(
        encabezado,
        text="Matrices · Archivos · Tkinter · Backtracking recursivo",
        font=("Arial", 10, "bold"),
        bg=COLOR_FONDO,
        fg=COLOR_TEXTO_SUAVE
    )
    subtitulo.pack(anchor="center", pady=(1, 4))


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

    fila_1 = tk.Frame(menu, bg=COLOR_PANEL)
    fila_1.pack(anchor="center", pady=(7, 3))

    crear_boton_menu(fila_1, "Crear mapa", accion_pendiente, COLOR_AZUL)
    crear_boton_menu(fila_1, "Cargar mapa", accion_pendiente, COLOR_AZUL_2)
    crear_boton_menu(fila_1, "Guardar mapa", accion_pendiente, COLOR_AZUL)
    crear_boton_menu(
        fila_1,
        "Editar mapa",
        abrir_editor_placeholder,
        COLOR_AMARILLO,
        color_texto="black"
    )

    fila_2 = tk.Frame(menu, bg=COLOR_PANEL)
    fila_2.pack(anchor="center", pady=(3, 7))

    crear_boton_menu(fila_2, "Buscar primer tesoro", accion_pendiente, COLOR_VERDE, ancho=20)
    crear_boton_menu(fila_2, "Buscar todos los tesoros", accion_pendiente, COLOR_VERDE_2, ancho=22)
    crear_boton_menu(fila_2, "Limpiar marcas", accion_pendiente, COLOR_GRIS)
    crear_boton_menu(fila_2, "Guardar resultado", accion_pendiente, COLOR_MORADO, ancho=18)
    crear_boton_menu(fila_2, "Salir", salir, COLOR_ROJO, ancho=10)


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

    boton.bind(
        "<Enter>",
        lambda evento: boton.config(
            bg=COLOR_HOVER,
            fg=COLOR_TEXTO_HOVER
        )
    )

    boton.bind(
        "<Leave>",
        lambda evento: boton.config(
            bg=color,
            fg=color_texto
        )
    )


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
        text="INFORMACION DEL SISTEMA",
        font=("Arial", 9, "bold"),
        bg=COLOR_PANEL_2,
        fg=COLOR_DORADO
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


# =========================================================
# DIBUJO DEL MAPA
# =========================================================

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

    # Marco dorado tipo ruina antigua
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

    for fila in range(filas):
        for col in range(columnas):
            simbolo = mapa[fila][col]

            x1 = inicio_x + col * tam_celda
            y1 = inicio_y + fila * tam_celda
            x2 = x1 + tam_celda
            y2 = y1 + tam_celda

            dibujar_celda(x1, y1, x2, y2, simbolo, tam_celda)

    canvas_mapa.create_text(
        AREA_MAPA // 2,
        AREA_MAPA - 14,
        text="Vista actual: " + str(filas) + " x " + str(columnas) + " | Celda: " + str(tam_celda) + "px",
        font=("Arial", 9, "bold"),
        fill="#d6d3d1"
    )


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

    canvas_mapa.create_text(
        AREA_MAPA // 2,
        20,
        text="RUINAS ANTIGUAS - MAPA DE EXPLORACION",
        font=("Arial", 10, "bold"),
        fill="#a16207"
    )


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

    # Textura de losas
    if tam >= 24:
        canvas_mapa.create_line(
            x1 + 4,
            y1 + tam * 0.62,
            x2 - 5,
            y1 + tam * 0.62,
            fill="#a89568",
            width=1
        )

        canvas_mapa.create_line(
            x1 + tam * 0.36,
            y1 + 5,
            x1 + tam * 0.36,
            y2 - 5,
            fill="#a89568",
            width=1
        )

        # Pequeñas grietas
        canvas_mapa.create_line(
            x1 + tam * 0.60,
            y1 + tam * 0.20,
            x1 + tam * 0.75,
            y1 + tam * 0.32,
            fill="#8a7b58",
            width=1
        )

        canvas_mapa.create_line(
            x1 + tam * 0.20,
            y1 + tam * 0.78,
            x1 + tam * 0.34,
            y1 + tam * 0.68,
            fill="#8a7b58",
            width=1
        )


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

    if tam >= 24:
        # Separaciones tipo ladrillo
        canvas_mapa.create_line(
            x1 + 4,
            y1 + tam * 0.52,
            x2 - 4,
            y1 + tam * 0.52,
            fill="#111827",
            width=1
        )

        canvas_mapa.create_line(
            x1 + tam * 0.50,
            y1 + 4,
            x1 + tam * 0.50,
            y2 - 4,
            fill="#111827",
            width=1
        )

        # Grieta
        canvas_mapa.create_line(
            x1 + tam * 0.20,
            y1 + tam * 0.18,
            x1 + tam * 0.36,
            y1 + tam * 0.34,
            x1 + tam * 0.28,
            y1 + tam * 0.52,
            fill="#020617",
            width=1
        )


def dibujar_entrada(x1, y1, x2, y2, tam):
    # Portal verde
    canvas_mapa.create_rectangle(
        x1 + 4,
        y1 + 4,
        x2 - 4,
        y2 - 4,
        fill="#052e16",
        outline="#86efac",
        width=2
    )

    canvas_mapa.create_arc(
        x1 + 7,
        y1 + 5,
        x2 - 7,
        y2 + tam * 0.60,
        start=0,
        extent=180,
        fill="#14532d",
        outline="#bbf7d0",
        width=2
    )

    canvas_mapa.create_text(
        (x1 + x2) / 2,
        (y1 + y2) / 2 + tam * 0.06,
        text="E",
        fill="#22c55e",
        font=("Arial", max(10, int(tam * 0.52)), "bold")
    )


def dibujar_tesoro(x1, y1, x2, y2, tam):
    # Sombra
    canvas_mapa.create_oval(
        x1 + tam * 0.18,
        y2 - tam * 0.20,
        x2 - tam * 0.18,
        y2 - tam * 0.08,
        fill="#78350f",
        outline=""
    )

    # Cuerpo del cofre
    canvas_mapa.create_rectangle(
        x1 + tam * 0.18,
        y1 + tam * 0.45,
        x2 - tam * 0.18,
        y2 - tam * 0.18,
        fill="#92400e",
        outline="#451a03",
        width=2
    )

    # Tapa
    canvas_mapa.create_arc(
        x1 + tam * 0.18,
        y1 + tam * 0.18,
        x2 - tam * 0.18,
        y2 - tam * 0.22,
        start=0,
        extent=180,
        fill="#facc15",
        outline="#78350f",
        width=2
    )

    # Brillo
    canvas_mapa.create_rectangle(
        x1 + tam * 0.43,
        y1 + tam * 0.25,
        x1 + tam * 0.57,
        y2 - tam * 0.18,
        fill="#fde68a",
        outline="#92400e"
    )

    # Cerradura
    canvas_mapa.create_rectangle(
        x1 + tam * 0.43,
        y1 + tam * 0.58,
        x1 + tam * 0.57,
        y1 + tam * 0.72,
        fill="#111827",
        outline="#030712"
    )


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

        canvas_mapa.create_polygon(
            p2 - tam * 0.05,
            y1 + tam * 0.22,
            p2,
            y1 + tam * 0.18,
            p2 + tam * 0.05,
            y1 + tam * 0.22,
            fill="#fee2e2",
            outline=""
        )

    canvas_mapa.create_text(
        (x1 + x2) / 2,
        y1 + tam * 0.72,
        text="!",
        fill="white",
        font=("Arial", max(7, int(tam * 0.32)), "bold")
    )


def dibujar_salida(x1, y1, x2, y2, tam):
    # Portal azul de salida
    canvas_mapa.create_rectangle(
        x1 + 4,
        y1 + 4,
        x2 - 4,
        y2 - 4,
        fill="#172554",
        outline="#bfdbfe",
        width=2
    )

    canvas_mapa.create_oval(
        x1 + tam * 0.22,
        y1 + tam * 0.18,
        x2 - tam * 0.22,
        y2 - tam * 0.18,
        fill="#2563eb",
        outline="#93c5fd",
        width=2
    )

    canvas_mapa.create_text(
        (x1 + x2) / 2,
        (y1 + y2) / 2,
        text="S",
        fill="white",
        font=("Arial", max(10, int(tam * 0.48)), "bold")
    )


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


def calcular_tamano_celda(filas, columnas):
    mayor_dimension = max(filas, columnas)
    tam = AREA_MAPA // mayor_dimension

    if tam > TAM_MAX_CELDA:
        tam = TAM_MAX_CELDA

    if tam < TAM_MIN_CELDA:
        tam = TAM_MIN_CELDA

    return tam


# =========================================================
# AREA DE INFORMACION
# =========================================================

def escribir_informacion(mensaje, limpiar=True):
    texto_informacion.config(state="normal")

    if limpiar:
        texto_informacion.delete("1.0", "end")

    texto_informacion.insert("end", mensaje)
    texto_informacion.config(state="disabled")


def agregar_informacion(mensaje):
    texto_informacion.config(state="normal")
    texto_informacion.insert("end", "\n" + mensaje)
    texto_informacion.see("end")
    texto_informacion.config(state="disabled")


def mostrar_informacion_inicial():
    filas = len(mapa)
    columnas = 0

    if filas > 0:
        columnas = len(mapa[0])

    mensaje = (
        "Aqui se mostraran mensajes como: mapa cargado, busqueda iniciada, "

    )

    escribir_informacion(mensaje)


def contar_simbolo(simbolo):
    cantidad = 0

    for fila in mapa:
        for celda in fila:
            if celda == simbolo:
                cantidad = cantidad + 1

    return cantidad


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