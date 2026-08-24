import json
import os
from .ui import titulo, menu, exito, error, advertencia, modificar, eliminar

BASE_DIR = os.path.dirname(__file__)
ARCHIVO_ADOPTANTES = os.path.join(BASE_DIR, "adoptantes.json")
RAIZ_PROYECTO = os.path.dirname(BASE_DIR)

ARCHIVO_ADOPCIONES = os.path.join(
    RAIZ_PROYECTO,
    "adopciones",
    "datos",
    "adopciones.json"
)

ARCHIVO_ANIMALES = os.path.join(
    RAIZ_PROYECTO,
    "registro_animales",
    "datos",
    "animales.json"
)


def cargar_adoptantes():
    if not os.path.exists(ARCHIVO_ADOPTANTES):
        return []

    with open(ARCHIVO_ADOPTANTES, "r", encoding="utf-8") as archivo:
        try:
            return json.load(archivo)
        except json.JSONDecodeError:
            return []


def guardar_adoptantes():
    with open(ARCHIVO_ADOPTANTES, "w", encoding="utf-8") as archivo:
        json.dump(adoptantes, archivo, indent=4, ensure_ascii=False)

def cargar_json(ruta_archivo):
    if not os.path.exists(ruta_archivo):
        return []

    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        try:
            return json.load(archivo)
        except json.JSONDecodeError:
            return []


def cargar_adopciones():
    return cargar_json(ARCHIVO_ADOPCIONES)


def cargar_animales():
    return cargar_json(ARCHIVO_ANIMALES)

adoptantes = cargar_adoptantes()


def mostrar_menu():
    titulo("FAMILIAS ADOPTANTES")
    menu("1. Registrar familia adoptante")
    menu("2. Lista de familias adoptantes")
    menu("3. Buscar familia adoptiva")
    menu("4. Modificar dato de contacto")
    menu("5. Eliminar familia adoptante")
    menu("0. Volver al menú principal")


def obtener_proximo_id():
    mayor_id = 0

    for adoptante in adoptantes:
        if adoptante["id"] > mayor_id:
            mayor_id = adoptante["id"]

    for adopcion in cargar_adopciones():
        if adopcion["id_adoptante"] > mayor_id:
            mayor_id = adopcion["id_adoptante"]

    return mayor_id + 1


def registrar_adoptante():
    titulo("REGISTRAR FAMILIA ADOPTANTE")

    nuevo_id = obtener_proximo_id()

    dni = pedir_dni("DNI: ")

    if dni is None:
        advertencia("Operación cancelada.")
        return

    while existe_dni(dni):
        advertencia("Ya existe una familia adoptante registrada con ese DNI.")
        dni = pedir_dni("DNI: ")

        if dni is None:
            advertencia("Operación cancelada.")
            return

    dni = normalizar_dni(dni)

    nombre_completo = pedir_dato_obligatorio("Nombre completo: ")

    if nombre_completo is None:
        advertencia("Operación cancelada.")
        return

    telefono = pedir_telefono("Teléfono: ")

    if telefono is None:
        advertencia("Operación cancelada.")
        return

    email = pedir_email("Email: ")

    if email is None:
        advertencia("Operación cancelada.")
        return

    vivienda = pedir_vivienda()

    if vivienda is None:
        advertencia("Operación cancelada.")
        return

    tiene_otras_mascotas = pedir_si_no("¿Tiene otras mascotas? si/no: ")

    if tiene_otras_mascotas is None:
        advertencia("Operación cancelada.")
        return

    adoptante = {
        "id": nuevo_id,
        "dni": dni,
        "nombre_completo": nombre_completo,
        "telefono": telefono,
        "email": email,
        "vivienda": vivienda,
        "tiene_otras_mascotas": tiene_otras_mascotas
    }

    adoptantes.append(adoptante)
    guardar_adoptantes()

    exito("Familia adoptante registrada correctamente.")


def listar_adoptantes():
    titulo("LISTADO DE FAMILIAS ADOPTANTES")

    if len(adoptantes) == 0:
        advertencia("No hay familias adoptantes registradas.")
        return

    exito(f"Cantidad de familias registradas: {len(adoptantes)}")
    print("------------------------------")

    for adoptante in adoptantes:
        mostrar_datos_adoptante(adoptante)
        print("------------------------------")


def buscar_adoptante():
    titulo("BUSCAR FAMILIA ADOPTANTE")

    if len(adoptantes) == 0:
        advertencia("No hay familias adoptantes registradas.")
        return

    menu("1. Buscar por DNI")
    menu("2. Buscar por nombre")
    menu("0. Cancelar")

    opcion_busqueda = input("Seleccione una opción: ").strip()

    while opcion_busqueda != "1" and opcion_busqueda != "2" and opcion_busqueda != "0":
        error("Opción inválida. Debe seleccionar 1, 2 o 0.")
        opcion_busqueda = input("Seleccione una opción: ").strip()

    if opcion_busqueda == "0":
        advertencia("Operación cancelada.")
        return

    encontrado = False

    if opcion_busqueda == "1":
        dni_buscado = pedir_dni("Ingrese el DNI: ")

        if dni_buscado is None:
            advertencia("Operación cancelada.")
            return

        adoptante = buscar_por_dni(dni_buscado)

        if adoptante is not None:
            exito("Familia encontrada:")
            mostrar_datos_adoptante(adoptante)
            mostrar_adopciones_realizadas(adoptante)
            encontrado = True

    elif opcion_busqueda == "2":
        nombre_buscado = pedir_dato_obligatorio("Ingrese el nombre o parte del nombre: ")

        if nombre_buscado is None:
            advertencia("Operación cancelada.")
            return

        resultados = buscar_por_nombre(nombre_buscado)

        if len(resultados) > 0:
            exito(f"Cantidad de coincidencias encontradas: {len(resultados)}")

        for adoptante in resultados:
            exito("Familia encontrada:")
            mostrar_datos_adoptante(adoptante)
            mostrar_adopciones_realizadas(adoptante)
            encontrado = True

    if not encontrado:
        advertencia("No se encontró ninguna familia adoptante.")


def normalizar_dni(dni):
    return dni.replace(".", "").replace(" ", "")


def dni_es_valido(dni):
    dni_limpio = normalizar_dni(dni)

    if dni_limpio == "":
        return False

    return dni_limpio.isdigit()


def existe_dni(dni):
    for adoptante in adoptantes:
        if normalizar_dni(adoptante["dni"]) == normalizar_dni(dni):
            return True

    return False


def buscar_por_dni(dni):
    for adoptante in adoptantes:
        if normalizar_dni(adoptante["dni"]) == normalizar_dni(dni):
            return adoptante

    return None


def buscar_por_nombre(nombre):
    resultados = []

    for adoptante in adoptantes:
        if nombre.lower() in adoptante["nombre_completo"].lower():
            resultados.append(adoptante)

    return resultados

def obtener_adopciones_de_adoptante(id_adoptante):
    adopciones_de_la_familia = []

    for adopcion in cargar_adopciones():
        if adopcion["id_adoptante"] == id_adoptante:
            adopciones_de_la_familia.append(adopcion)

    return adopciones_de_la_familia


def obtener_nombre_animal(id_animal):
    for animal in cargar_animales():
        if animal["id"] == id_animal:
            return animal["nombre_animal"]

    return f"Animal con ID {id_animal} no encontrado"


def mostrar_adopciones_realizadas(adoptante):
    adopciones_de_la_familia = obtener_adopciones_de_adoptante(adoptante["id"])

    if len(adopciones_de_la_familia) == 0:
        advertencia("Esta familia no registra adopciones.")
        return

    exito("Adopciones realizadas por esta familia:")

    for adopcion in adopciones_de_la_familia:
        nombre_animal = obtener_nombre_animal(adopcion["id_animal"])

        print("Adopción ID:", adopcion["id"])
        print("Animal:", nombre_animal)
        print("Fecha:", adopcion["fecha_adopcion"])
        print("Estado:", adopcion["estado"])

        if len(adopcion["seguimientos"]) > 0:
            print("Seguimientos:")

            for seguimiento in adopcion["seguimientos"]:
                print("-", seguimiento)

        print("------------------------------")

def texto_mascotas(tiene_otras_mascotas):
    if tiene_otras_mascotas is True:
        return "Tiene"
    else:
        return "No tiene"


def mostrar_datos_adoptante(adoptante):
    print("ID:", adoptante["id"])
    print("DNI:", adoptante["dni"])
    print("Nombre:", adoptante["nombre_completo"])
    print("Teléfono:", adoptante["telefono"])
    print("Email:", adoptante["email"])
    print("Vivienda:", adoptante["vivienda"])
    print("Tiene otras mascotas:", texto_mascotas(adoptante["tiene_otras_mascotas"]))


def pedir_dato_obligatorio(mensaje):
    dato = input(mensaje).strip()

    if dato == "0":
        return None

    while dato == "":
        error("Este dato no puede quedar vacío.")
        dato = input(mensaje).strip()

        if dato == "0":
            return None

    return dato


def pedir_dni(mensaje):
    dni = pedir_dato_obligatorio(mensaje)

    if dni is None:
        return None

    while not dni_es_valido(dni):
        error("DNI inválido. Ingrese solo números, con o sin puntos.")
        dni = pedir_dato_obligatorio(mensaje)

        if dni is None:
            return None

    return dni


def telefono_es_valido(telefono):
    telefono_limpio = telefono.replace(" ", "").replace("-", "").replace("+", "")

    if telefono_limpio == "":
        return False

    return telefono_limpio.isdigit()


def pedir_telefono(mensaje):
    telefono = pedir_dato_obligatorio(mensaje)

    if telefono is None:
        return None

    while not telefono_es_valido(telefono):
        error("Teléfono inválido. Ingrese solo números. Puede usar espacios, guiones o +.")
        telefono = pedir_dato_obligatorio(mensaje)

        if telefono is None:
            return None

    return telefono


def pedir_email(mensaje):
    email = pedir_dato_obligatorio(mensaje)

    if email is None:
        return None

    while "@" not in email:
        error("Email inválido. Debe contener @.")
        email = pedir_dato_obligatorio(mensaje)

        if email is None:
            return None

    return email


def pedir_vivienda():
    menu("\nTipo de vivienda:")
    menu("1. Casa con patio")
    menu("2. Departamento")
    menu("3. Casa sin patio")
    menu("0. Cancelar")

    opcion_vivienda = input("Seleccione una opción: ").strip()

    if opcion_vivienda == "0":
        return None

    while opcion_vivienda != "1" and opcion_vivienda != "2" and opcion_vivienda != "3":
        error("Opción inválida. Debe seleccionar 1, 2, 3 o 0.")
        opcion_vivienda = input("Seleccione una opción: ").strip()

        if opcion_vivienda == "0":
            return None

    if opcion_vivienda == "1":
        return "casa con patio"
    elif opcion_vivienda == "2":
        return "departamento"
    else:
        return "casa sin patio"


def pedir_si_no(mensaje):
    respuesta = input(mensaje).strip().lower()

    if respuesta == "0":
        return None

    while respuesta != "si" and respuesta != "sí" and respuesta != "no":
        error("Respuesta inválida. Ingrese si, no o 0 para cancelar.")
        respuesta = input(mensaje).strip().lower()

        if respuesta == "0":
            return None

    if respuesta == "si" or respuesta == "sí":
        return True
    else:
        return False


def modificar_adoptante():
    modificar("MODIFICAR DATOS DE CONTACTO")

    if len(adoptantes) == 0:
        advertencia("No hay familias adoptantes registradas.")
        return

    dni_buscado = pedir_dni("Ingrese el DNI de la familia adoptante: ")

    if dni_buscado is None:
        advertencia("Operación cancelada.")
        return

    adoptante = buscar_por_dni(dni_buscado)

    if adoptante is None:
        advertencia("No se encontró ninguna familia con ese DNI.")
        return

    exito("Familia encontrada:")
    print("Nombre:", adoptante["nombre_completo"])
    print("Teléfono actual:", adoptante["telefono"])
    print("Email actual:", adoptante["email"])

    modificar("¿Qué dato desea modificar?")
    modificar("1. Teléfono")
    modificar("2. Email")
    modificar("3. Teléfono y email")
    modificar("0. Cancelar")

    opcion_modificar = input("Seleccione una opción: ").strip()

    while opcion_modificar != "1" and opcion_modificar != "2" and opcion_modificar != "3" and opcion_modificar != "0":
        error("Opción inválida. Debe seleccionar 1, 2, 3 o 0.")
        opcion_modificar = input("Seleccione una opción: ").strip()

    if opcion_modificar == "0":
        advertencia("Operación cancelada.")
        return

    if opcion_modificar == "1" or opcion_modificar == "3":
        nuevo_telefono = pedir_telefono("Nuevo teléfono: ")

        if nuevo_telefono is None:
            advertencia("Operación cancelada.")
            return

        adoptante["telefono"] = nuevo_telefono

    if opcion_modificar == "2" or opcion_modificar == "3":
        nuevo_email = pedir_email("Nuevo email: ")

        if nuevo_email is None:
            advertencia("Operación cancelada.")
            return

        adoptante["email"] = nuevo_email

    guardar_adoptantes()

    exito("Datos de contacto modificados correctamente.")


def eliminar_adoptante():
    eliminar("ELIMINAR FAMILIA ADOPTANTE")

    if len(adoptantes) == 0:
        advertencia("No hay familias adoptantes registradas.")
        return

    dni_buscado = pedir_dni("Ingrese el DNI de la familia adoptante: ")

    if dni_buscado is None:
        advertencia("Operación cancelada.")
        return

    adoptante = buscar_por_dni(dni_buscado)

    if adoptante is None:
        advertencia("No se encontró ninguna familia con ese DNI.")
        return

    exito("Familia encontrada:")
    mostrar_datos_adoptante(adoptante)

    adopciones_de_la_familia = obtener_adopciones_de_adoptante(adoptante["id"])

    if len(adopciones_de_la_familia) > 0:
        advertencia("No se puede eliminar a esta familia porque tiene adopciones registradas.")
        return

    confirmacion = pedir_si_no("¿Está seguro que desea eliminar esta familia? si/no: ")

    if confirmacion is None:
        advertencia("Operación cancelada.")
        return

    if confirmacion:
        adoptantes.remove(adoptante)
        guardar_adoptantes()
        exito("Familia adoptante eliminada correctamente.")
    else:
        advertencia("Operación cancelada.")


def menu_adoptantes():
    while True:
        mostrar_menu()
        opcion = input("Ingrese una opción: ").strip()

        if opcion == "1":
            registrar_adoptante()
        elif opcion == "2":
            listar_adoptantes()
        elif opcion == "3":
            buscar_adoptante()
        elif opcion == "4":
            modificar_adoptante()
        elif opcion == "5":
            eliminar_adoptante()
        elif opcion == "0":
            advertencia("Volviendo al menú principal...")
            return
        else:
            error("Opción incorrecta")


if __name__ == "__main__":
    menu_adoptantes()
