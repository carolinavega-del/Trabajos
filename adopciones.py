#importaciones
import json
import os
from .validaciones import validar_entero
from .validaciones import validar_fecha
from .estilos import (console, exito, error, advertencia, titulo)


BASE_DIR = os.path.dirname(__file__)
NOMBRE_ARCHIVO = os.path.join(BASE_DIR, "datos", "adopciones.json")


def leer_archivo(nombre_archivo):
        if os.path.exists(nombre_archivo):
        with open(nombre_archivo,"rt",encoding="UTF-8") as archivo:
            datos= json.load(archivo)
            return datos
    else:
        return []
    

def guardar_archivo(nombre_archivo,datos):
     with open(nombre_archivo, "w", encoding="UTF-8") as archivo:
         #indent=5 es para que el json no quede todo junto, ensure corrige correctamnete las ñ y las tilde
         json.dump(datos, archivo, indent=5,ensure_ascii=False)
    
    

def generar_id_adopcion(adopciones):
    if not adopciones:
        return 1 
    else : 
      return adopciones[-1]["id"] + 1
       
        
def cargar_adopcion():
    adopciones=leer_archivo(NOMBRE_ARCHIVO)
    # guardo el id de la nueva adopcion en la variable para que no se pierda
    nuevo_id=generar_id_adopcion(adopciones) 
    id_animal=validar_entero("Ingrese el ID del animal: ")
    id_adoptante=validar_entero("ingrese el ID del adoptante: ")
    fecha_adopcion=validar_fecha("Ingresar la fecha de adopcion (dd/mm/aaaa): ")
    
    adopcion= {
        "id":nuevo_id,
        "id_animal":id_animal,
        "id_adoptante":id_adoptante,
        "fecha_adopcion":fecha_adopcion,
        "seguimientos":[],
        "estado":"activa"
    }
    adopciones.append(adopcion)
    #el archivo debe guardarse en el json
    guardar_archivo(NOMBRE_ARCHIVO, adopciones)
    exito("Adopción registrada correctamente.")


def listar_adopciones():
    adopciones=leer_archivo(NOMBRE_ARCHIVO)
    if not adopciones:
     print("No hay adopciones registradas.")
     return
 
    for adopcion in adopciones:
     print("ID:", adopcion["id"])
     print("Animal: ", adopcion["id_animal"])
     print("Familia: ", adopcion["id_adoptante"])
     print("Fecha: ", adopcion["fecha_adopcion"])
     print("Estado: " ,adopcion["estado"])
     print()
        

def  buscar_adopcion_animal(adopciones,id_animal):
  
    for adopcion in adopciones:
        if adopcion["id_animal"] == id_animal: 
            return adopcion
            
    return None


def buscar_por_animal():
    adopciones = leer_archivo(NOMBRE_ARCHIVO)
    id_animal = validar_entero("Ingrese ID del animal: ")

    adopcion = buscar_adopcion_animal(adopciones, id_animal)

    if not adopcion:
        error("Adopción no encontrada")
        return

    print(adopcion)

def  buscar_adopcion_familia(adopciones,id_adoptante):
    
    for adopcion in adopciones:
        if adopcion["id_adoptante"] == id_adoptante: 
            return adopcion
            
    return None

def buscar_por_familia():
    adopciones = leer_archivo(NOMBRE_ARCHIVO)
    id_adoptante = validar_entero("Ingrese ID de la familia: ")

    adopcion = buscar_adopcion_familia(adopciones, id_adoptante)

    if not adopcion:
        error("Adopción no encontrada")
        return

    print(adopcion)


def agregar_seguimiento():

    id_animal = validar_entero("Ingrese el ID del animal: ")

    adopciones = leer_archivo(NOMBRE_ARCHIVO)
    
    adopcion = buscar_adopcion_animal(adopciones, id_animal)

    for adopcion in adopciones:

        if adopcion["id_animal"] == id_animal:

            nota = input("Ingrese el seguimiento: ")

            adopcion["seguimientos"].append(nota)

            guardar_archivo(NOMBRE_ARCHIVO, adopciones)

            exito("Seguimiento agregado correctamente")
            return

    print("La adopcion no esta registrada")


def cancelar_adopcion():
    
    id_animal=validar_entero("Ingresar ID del animal: ")
    
    adopciones=leer_archivo(NOMBRE_ARCHIVO)
    
    adopcion= buscar_adopcion_animal(adopciones,id_animal)
    
    if not adopcion:
        error("Adopcion no encontrada")
        return
    
    adopcion["estado"] = "cancelada"
    guardar_archivo(NOMBRE_ARCHIVO,adopciones)
    exito("Estado actualizado")
    return
    
#menu
#---------------------------------------------------------

def menu_adopciones():
    while True:
         print("\n════════════════════════════════════════")
         print("📋 ADOPCIONES")
         print("════════════════════════════════════════")
         print("1. Registrar adopción")
         print("2. Ver adopciones")
         print("3. Buscar por animal")
         print("4. Buscar por familia")
         print("5. Agregar seguimiento")
         print("6. Cancelar adopción")
         print("0. Volver al menú principal")

         opcion = input("¿Qué querés hacer? ")
         
         if opcion == "1":
             cargar_adopcion()
             
         elif opcion == "2":
             listar_adopciones()
             
         elif opcion == "3":
             buscar_por_animal()
             
         elif opcion == "4":
             buscar_por_familia()
             
         elif opcion == "5":
             agregar_seguimiento()
             
         elif opcion == "6":
             cancelar_adopcion()
             
         elif opcion == "0":
             break
        
         else:
            print("Opción inválida. Intentá nuevamente.")


"""=====================================================
PERSISTENCIA
====================================================="""

def leer_archivo(nombre_archivo):
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "rt", encoding="UTF-8") as archivo:
            return json.load(archivo)
    return []


def guardar_archivo(nombre_archivo, datos):
    with open(nombre_archivo, "w", encoding="UTF-8") as archivo:
        json.dump(datos, archivo, indent=5, ensure_ascii=False)


"""=====================================================
LÓGICA
====================================================="""

def generar_id_adopcion(adopciones):
    return 1 if not adopciones else adopciones[-1]["id"] + 1


def cargar_adopcion():
    adopciones = leer_archivo(NOMBRE_ARCHIVO)
    nuevo_id = generar_id_adopcion(adopciones)

    id_animal = validar_entero("Ingrese el ID del animal: ")
    id_adoptante = validar_entero("Ingrese el ID del adoptante: ")
    fecha_adopcion = validar_fecha("Ingresar la fecha de adopción (dd/mm/aaaa): ")

    adopcion = {
        "id": nuevo_id,
        "id_animal": id_animal,
        "id_adoptante": id_adoptante,
        "fecha_adopcion": fecha_adopcion,
        "seguimientos": [],
        "estado": "activa"
    }

    adopciones.append(adopcion)
    guardar_archivo(NOMBRE_ARCHIVO, adopciones)

    exito(f"Adopción registrada correctamente con ID {nuevo_id}")


"""=====================================================
LISTADO
====================================================="""

def listar_adopciones():
    adopciones = leer_archivo(NOMBRE_ARCHIVO)

    titulo("📋 ADOPCIONES REGISTRADAS")

    if not adopciones:
        advertencia("No hay adopciones registradas.")
        return

    for adopcion in adopciones:
        console.print(f"[bold cyan]ID:[/bold cyan] {adopcion['id']}")
        console.print(f"[bold cyan]Animal:[/bold cyan] {adopcion['id_animal']}")
        console.print(f"[bold cyan]Familia:[/bold cyan] {adopcion['id_adoptante']}")
        console.print(f"[bold cyan]Fecha:[/bold cyan] {adopcion['fecha_adopcion']}")
        console.print(f"[bold cyan]Estado:[/bold cyan] {adopcion['estado']}")
        console.print("-" * 40)


"""=====================================================
BÚSQUEDAS
====================================================="""

def buscar_adopcion_animal(adopciones, id_animal):
    for adopcion in adopciones:
        if adopcion["id_animal"] == id_animal:
            return adopcion
    return None


def buscar_por_animal():
    adopciones = leer_archivo(NOMBRE_ARCHIVO)
    id_animal = validar_entero("Ingrese ID del animal: ")

    adopcion = buscar_adopcion_animal(adopciones, id_animal)

    if not adopcion:
        error("Adopción no encontrada")
        return

    titulo("🔍 RESULTADO")
    console.print(adopcion)


def buscar_adopcion_familia(adopciones, id_adoptante):
    for adopcion in adopciones:
        if adopcion["id_adoptante"] == id_adoptante:
            return adopcion
    return None


def buscar_por_familia():
    adopciones = leer_archivo(NOMBRE_ARCHIVO)
    id_adoptante = validar_entero("Ingrese ID de la familia: ")

    adopcion = buscar_adopcion_familia(adopciones, id_adoptante)

    if not adopcion:
        error("Adopción no encontrada")
        return

    titulo("🔍 RESULTADO")
    console.print(adopcion)


"""=====================================================
SEGUIMIENTOS
====================================================="""

def agregar_seguimiento():
    adopciones = leer_archivo(NOMBRE_ARCHIVO)
    id_animal = validar_entero("Ingrese el ID del animal: ")

    for adopcion in adopciones:
        if adopcion["id_animal"] == id_animal:

            nota = input("Ingrese el seguimiento: ")
            adopcion["seguimientos"].append(nota)

            guardar_archivo(NOMBRE_ARCHIVO, adopciones)

            exito("Seguimiento agregado correctamente")
            return

    error("La adopción no está registrada")


"""=====================================================
CANCELACIÓN
====================================================="""

def cancelar_adopcion():
    adopciones = leer_archivo(NOMBRE_ARCHIVO)
    id_animal = validar_entero("Ingresar ID del animal: ")

    adopcion = buscar_adopcion_animal(adopciones, id_animal)

    if not adopcion:
        error("Adopción no encontrada")
        return

    adopcion["estado"] = "cancelada"
    guardar_archivo(NOMBRE_ARCHIVO, adopciones)

    advertencia("Adopción cancelada correctamente")


"""=====================================================
MENÚ
====================================================="""

def menu_adopciones():
    while True:
        titulo("📋 MENÚ ADOPCIONES")

        print("1. Registrar adopción")
        print("2. Ver adopciones")
        print("3. Buscar por animal")
        print("4. Buscar por familia")
        print("5. Agregar seguimiento")
        print("6. Cancelar adopción")
        print("0. Volver al menú principal")

        opcion = input("¿Qué querés hacer? ")

        if opcion == "1":
            cargar_adopcion()

        elif opcion == "2":
            listar_adopciones()

        elif opcion == "3":
            buscar_por_animal()

        elif opcion == "4":
            buscar_por_familia()

        elif opcion == "5":
            agregar_seguimiento()

        elif opcion == "6":
            cancelar_adopcion()

        elif opcion == "0":
            break

        else:
            error("Opción inválida. Intentá nuevamente.")

if __name__ == '__main__':
    print("EJECUTANDO MENU ADOPCIONES")
    menu_adopciones()




