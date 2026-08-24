from .data_atenc_veterinarias.persistencia import cargar_atenciones

from rich.console import Console
from rich.table import Table
from rich import box

from atenciones_veterinarias.ui import (titulo, error, advertencia)

console = Console(highlight=False)


def mostrar_atencion(atencion):

    titulo("📋 DETALLE DE LA ATENCIÓN")

    tabla = Table(show_header=False, box=box.ROUNDED)

    tabla.add_column("Campo",style="bold #C77DFF")

    tabla.add_column("Valor")

    tabla.add_row("🔢 Número", str(atencion["Numero"])    )

    tabla.add_row("🆔 ID Animal", str(atencion["ID Animal"]))

    tabla.add_row("🐾 Nombre", atencion["Nombre"])

    tabla.add_row( "📅 Fecha", atencion["Fecha"])

    tabla.add_row("🩺 Tipo", atencion["Tipo de atencion"])

    tabla.add_row("📝 Observaciones", atencion["Observaciones"])



    tabla.add_row("⏳ Próxima atención",
        (str(atencion["Proxima atencion"]) 
            if atencion["Proxima atencion"]
            else "Sin seguimiento")
    )

    console.print(tabla)


def filtrar_por_id():

    atenciones = cargar_atenciones()

    if len(atenciones) == 0:

        advertencia(" No hay atenciones registradas.")
        return

    while True:

        console.print("\n🆔 Ingrese el ID del animal:", end=" ")

        id_animal = input()

        if id_animal.isdigit():

            id_animal = int(id_animal)
            break

        error(" Debe ingresar un número.")

    encontrado = False

    for atencion in atenciones:

        if atencion["ID Animal"] == id_animal:

            mostrar_atencion(atencion)
            encontrado = True

    if not encontrado:

        advertencia(" No se encontraron atenciones para ese animal.")


def filtrar_por_nombre():

    atenciones = cargar_atenciones()

    if len(atenciones) == 0:

        advertencia(" No hay atenciones registradas.")
        return

    while True:

        console.print("\n🐾 Ingrese el nombre del animal:",end=" ")

        nombre = input().strip()

        if nombre != "":
            break

        error(" Debe ingresar un nombre.")

    encontrado = False

    for atencion in atenciones:

        if atencion["Nombre"].lower() == nombre.lower():

            mostrar_atencion(atencion)
            encontrado = True

    if not encontrado:

        advertencia(" No se encontraron atenciones para ese animal.")


def filtrar_por_tipo():

    atenciones = cargar_atenciones()

    if len(atenciones) == 0:

        advertencia(" No hay atenciones registradas.")
        return

    tipos_validos = [
        "vacuna",
        "desparasitacion",
        "control",
        "cirugia",
        "otro"
    ]

    while True:

        console.print("\n🩺 Ingrese el tipo de atención:", style="bold #C77DFF", end=" ")

        tipo = input().lower().strip()

        if tipo in [
            "vacunas",
            "vacunacion",
            "vacunación"
        ]:
            tipo = "vacuna"

        elif tipo in [
            "desparasitacion",
            "desparasitar"
        ]:
            tipo = "desparasitacion"

        elif tipo in ["controles"]:
            tipo = "control"

        elif tipo in [
            "cirugía",
            "operacion",
            "cirugias",
            "cirugías",
            "operación"
        ]:
            tipo = "cirugia"

        if tipo in tipos_validos:
            break

        error(" Tipo inválido.")

    encontrado = False

    for atencion in atenciones:

        if atencion["Tipo de atencion"].lower() == tipo:

            mostrar_atencion(atencion)
            encontrado = True

    if not encontrado:

        advertencia(" No se encontraron atenciones de ese tipo.")


def menu_buscar_atenciones():

    while True:

        titulo("🔍 BUSCAR ATENCIONES")

        console.print("1. 🆔 Filtrar por ID de animal")

        console.print("2. 🐾 Filtrar por nombre")

        console.print("3. 🩺 Filtrar por tipo")

        console.print("0. 🚪 Volver")

        opcion = input("\n👉 Elige una opción: ")

        match opcion:

            case "1":
                filtrar_por_id()

            case "2":
                filtrar_por_nombre()

            case "3":
                filtrar_por_tipo()

            case "0":
                break

            case _:

                error(
                    " Opción inválida."
                )
