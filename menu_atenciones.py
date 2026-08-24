from .registrar_atencion import registrar_atencion
from .ver_atenciones import historial_atenciones
from .buscar_atencion import menu_buscar_atenciones
from rich.console import Console
from .ui import ( titulo, error)

console = Console(highlight=False)


def menu_atenciones():

    while True:

        titulo("🏥 ATENCIÓN VETERINARIA")

        console.print("1. 🩺 Registrar atención")
        console.print("2. 📋 Historial")
        console.print("3. 🔍 Buscar atención")
        console.print("0. 🚪 Volver al menú principal")

        opcion = input("\n👉 Elige una opción: ")

        match opcion:

            case "1":
                registrar_atencion()

            case "2":
                historial_atenciones()

            case "3":
                menu_buscar_atenciones()

            case "0":
                break

            case _:
                error("Opción inválida.")