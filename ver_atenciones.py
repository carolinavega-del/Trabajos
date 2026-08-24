from .data_atenc_veterinarias.persistencia import (
    guardar_atenciones,
    cargar_atenciones
)
from .buscar_atencion import menu_buscar_atenciones

from rich.console import Console
from rich.table import Table
from rich import box

from atenciones_veterinarias.ui import (
    titulo,
    exito,
    error,
    advertencia,
    modificar,
    eliminar
)

console = Console(highlight=False)


def historial_atenciones():

    while True:

        titulo("📋 HISTORIAL DE ATENCIONES")

        console.print(
            "1. 📄 Ver todas las atenciones"
        )

        console.print(
            "2. 🔍 Buscar atención"
        )

        console.print(
            "0. 🚪 Volver"
        )

        opcion = input(
            "\n👉 Elige una opción: "
        )

        match opcion:

            case "1":
                ver_atenciones()

            case "2":
                menu_buscar_atenciones()

            case "0":
                break

            case _:

                error(
                    " Opción inválida."
                )


def ver_atenciones():

    atenciones = cargar_atenciones()

    if len(atenciones) == 0:

        advertencia(
            " No se encuentran atenciones registradas."
        )
        return

    while True:

        titulo("📄 LISTADO DE ATENCIONES")

        tabla = Table(
            box=box.ROUNDED,
            header_style="bold #8A2BE2"
        )

        tabla.add_column(
            "N° Atención"
        )

        tabla.add_column(
            "Animal"
        )

        tabla.add_column(
            "Tipo"
        )

        tabla.add_column(
            "Fecha"
        )

        for atencion in atenciones:

            tabla.add_row(
                str(atencion["Numero"]),
                atencion["Nombre"],
                atencion["Tipo de atencion"],
                atencion["Fecha"]
            )

        console.print(tabla)

        console.print(
            "\n 0. Volver"
        )

        opcion = input(
            "\n👉 Ingrese el número de atención: "
        )

        if not opcion.isdigit():

            error(
                " Debe ingresar un número."
            )
            continue

        opcion = int(opcion)

        if opcion == 0:

            return

        atencion = None

        for registro in atenciones:

            if registro["Numero"] == opcion:

                atencion = registro
                break

        if atencion is None:

            error(
                "No existe una atención con ese número."
            )
            continue

        titulo("📋 DETALLE DE LA ATENCIÓN")

        detalle = Table(
            show_header=False,
            box=box.ROUNDED
        )

        detalle.add_column(
            "Campo",
            style="bold #C77DFF"
        )

        detalle.add_column(
            "Valor"
        )

        detalle.add_row(
            "🔢 Número",
            str(atencion["Numero"])
        )

        detalle.add_row(
            "🆔 ID Animal",
            str(atencion["ID Animal"])
        )

        detalle.add_row(
            "🐾 Nombre",
            atencion["Nombre"]
        )

        detalle.add_row(
            "📅 Fecha",
            atencion["Fecha"]
        )

        detalle.add_row(
            "🩺 Tipo",
            atencion["Tipo de atencion"]
        )

        detalle.add_row(
            "📝 Observaciones",
            atencion["Observaciones"]
        )

        detalle.add_row(
            "⏳ Próxima atención",
            (
                str(atencion["Proxima atencion"])
                if atencion["Proxima atencion"]
                else "Sin seguimiento"
            )
        )

        console.print(detalle)

        console.print(
            "\n1. ✏️ Modificar observaciones",
            style="magenta"
        )

        console.print(
            "2. 🗑️ Eliminar registro",
            style="bold red"
        )

        console.print(
            "0. 🔙 Volver al listado"
        )

        accion = input(
            "\n👉 Opción: "
        )

        if accion == "1":

            while True:

                nueva = input(
                    "📝 Nueva observación: "
                ).strip()

                if nueva != "":
                    break

                error(
                    " La observación no puede estar vacía."
                )

            atencion["Observaciones"] = nueva

            guardar_atenciones(
                atenciones
            )

            exito(
                " Observación modificada correctamente."
            )

        elif accion == "2":

            confirmar = input( error(
                "🗑️ ¿Eliminar atención? (S/N): "
            )).upper()

            if confirmar == "S":

                atenciones.remove(
                    atencion
                )

                guardar_atenciones(
                    atenciones
                )

                exito(
                    " Atención eliminada correctamente."
                )

            else:

                advertencia(
                    " Eliminación cancelada."
                )

        elif accion == "0":

            continue

        else:

            error(
                " Opción inválida."
            )