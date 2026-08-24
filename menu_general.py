from registro_animales.animales import menu_animales
from atenciones_veterinarias.menu_atenciones import menu_atenciones
from familias_adoptantes.familias_adoptantes import menu_adoptantes
from voluntarios_y_donantes.colaboradores import menu_colaboradores
from adopciones.adopciones import menu_adopciones
from rich.console import Console
from ui_menu_general import ( titulo, error, modificar)
console = Console(highlight=False)


"""console = Console()"""

def menu_general():

    while True:

        titulo('🐾 REFUGIO PATITAS DEL LITORAL 🐾')
    
        print('1 -🐶 Animales del refugio')
        print('2 -👤 Familias adoptantes')
        print('3 -🏡 Adopciones')
        print('4 -🩺 Atención veterinaria')
        print('5 -🤝 Voluntarios y donantes')
        print('0 -🚪 Salir del programa')
        print('═══════════════════════════════════════════════════')
        print('¿Qué querés hacer?')

        opcion = input("Elige una opción: ")

        match opcion:

            case "0":
                print('Saliendo del sistema..')
                break

            case "1":
                menu_animales()

            case "2":
                menu_adoptantes()

            case "3":
                menu_adopciones()

            case "4":
                menu_atenciones()

            case "5":
                menu_colaboradores()

            case _:
                error("Opción inválida.")

menu_general()