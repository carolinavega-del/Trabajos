from datetime import date, datetime

from rich.console import Console
from rich.table import Table
from rich import box

from .data_atenc_veterinarias.persistencia import (
    guardar_atenciones,
    cargar_atenciones
)
from registro_animales.animales import leer_archivo

from .ui import (
    titulo,
    exito,
    error,
    advertencia
)

console = Console(highlight=False)


def registrar_atencion():

    titulo("🏥 REGISTRAR ATENCIÓN VETERINARIA")

    atenciones = cargar_atenciones()

    if len(atenciones) > 0:

        numero_atencion = max(
            atencion["Numero"]
            for atencion in atenciones
        ) + 1

    else:

        numero_atencion = 1

    animales = leer_archivo()

    if len(animales) == 0:

        error("No hay animales registrados.")
        return

    titulo("🐾 ANIMALES REGISTRADOS")

    tabla_animales = Table(
        header_style="bold #8A2BE2",
        box=box.ROUNDED
    )

    tabla_animales.add_column(
        "ID",
        justify="center"
    )

    tabla_animales.add_column(
        "Nombre"
    )

    for animal in animales:

        tabla_animales.add_row(
            str(animal["id"]),
            animal["nombre_animal"]
        )

    console.print(tabla_animales)

    while True:
        console.print(
            "0. Volver"
        )

        console.print(
            "\n👉 Ingrese el ID del animal o 0 para volver:",
            end=" "
        )

        id_animal = input()

        if not id_animal.isdigit():

            error(
                " Debe ingresar un número."
            )
            continue

        id_animal = int(id_animal)

        if id_animal == 0:

            advertencia(
                " Registro cancelado."
            )
            return

        animal_encontrado = None

        for animal in animales:

            if animal["id"] == id_animal:

                animal_encontrado = animal
                break

        if animal_encontrado is None:

            error(
                " No existe un animal con ese ID."
            )
            continue

        break

    fecha = str(date.today())

    tipos_validos = [
        "vacuna",
        "desparasitacion",
        "control",
        "cirugia",
        "otro"
    ]

    while True:

        titulo("🩺 TIPOS DE ATENCIÓN")

        console.print("💉 vacuna")
        console.print("🦠 desparasitacion")
        console.print("📋 control")
        console.print("🏥 cirugia")
        console.print("📌 otro")

        tipo = input(
            "\nTipo de atención: "
        ).lower().strip()

        if tipo in [
            "vacunas",
            "vacunacion",
            "vacunación"
        ]:
            tipo = "vacuna"

        elif tipo in [
            "desparasitación",
            "desparasitar"
        ]:
            tipo = "desparasitacion"

        elif tipo in ["controles"]:
            tipo = "control"

        elif tipo in [
            "cirugía",
            "cirugias",
            "cirugías",
            "operacion",
            "operación"
        ]:
            tipo = "cirugia"

        if tipo in tipos_validos:
            break

        error("Tipo inválido.")

    while True:

        fecha_ingresada = input(
            "📅 Próxima atención (DD/MM/AAAA) o Enter si no corresponde: "
        )

        if fecha_ingresada == "":

            proxima_atencion = None
            break

        try:

            fecha_ingresada = fecha_ingresada.replace(
                "/",
                "-"
            )

            proxima_atencion = datetime.strptime(
                fecha_ingresada,
                "%d-%m-%Y"
            ).date()

            if proxima_atencion <= date.today():

                advertencia(
                    "La fecha debe ser posterior a hoy."
                )

                continue

            proxima_atencion = proxima_atencion.strftime(
                "%d/%m/%Y"
            )

            break

        except ValueError:

            error(
                "Fecha inválida. Use DD/MM/AAAA."
            )
    while True:

        observaciones = input(
            " Indique las observaciones de la atención: "
        ).strip()

        if observaciones != "":
            break

        error(
            " Las observaciones no pueden estar vacías."
        )

    titulo("📋 RESUMEN DE LA ATENCIÓN")

    tabla = Table(
        show_header=False,
        box=box.ROUNDED
    )

    tabla.add_column(
        "Campo",
        style="bold #C77DFF"
    )

    tabla.add_column(
        "Valor"
    )

    tabla.add_row(
        "🔢 Número",
        str(numero_atencion)
    )

    tabla.add_row(
        "🆔 ID Animal",
        str(animal_encontrado["id"])
    )

    tabla.add_row(
        "🐾 Nombre",
        animal_encontrado["nombre_animal"]
    )

    tabla.add_row(
        "📅 Fecha",
        fecha
    )

    tabla.add_row(
        "🩺 Tipo",
        tipo
    )

    tabla.add_row(
        "📝 Observaciones",
        observaciones
    )

    tabla.add_row(
        "⏳ Próxima atención",
        proxima_atencion
        if proxima_atencion
        else "Sin seguimiento"
    )

    console.print(tabla)

    console.print(
        "\n💾 [bold green]¿Desea guardar esta atención?[/bold green]"
    )

    while True:

        confirmar = input(
            "(S/N): "
        ).upper()

        if confirmar in ["S", "N"]:
            break

        error(
            " Ingrese solamente S o N."
        )

    if confirmar == "N":

        error(
            " Registro cancelado."
        )
        return

    atencion = {
        "Numero": numero_atencion,
        "ID Animal": animal_encontrado["id"],
        "Nombre": animal_encontrado["nombre_animal"],
        "Fecha": fecha,
        "Tipo de atencion": tipo,
        "Observaciones": observaciones,
        "Proxima atencion": proxima_atencion
    }

    atenciones.append(atencion)

    guardar_atenciones(atenciones)

    exito(
        f" Atención N° {numero_atencion} registrada correctamente."
    )