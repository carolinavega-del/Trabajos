import os
import json
from rich.console import Console
from rich.table import Table
import registro_animales.validaciones_animales as validaciones
from voluntarios_y_donantes import colaboradores
from ui_menu_general import exito, error, advertencia, modificar, eliminar, titulo

# ==========================================
# CONSTANTES
# ==========================================

BASE_DIR = os.path.dirname(__file__)
NOMBRE_ARCHIVO = os.path.join(BASE_DIR, "datos", "animales.json")

ESTADO_EN_REFUGIO = 'en_refugio'
ESTADO_EN_ADOPCION = 'en_adopcion'
ESTADO_ADOPTADO = 'adoptado'

# ==========================================
# ARCHIVOS JSON
# ==========================================
def leer_archivo():
    if os.path.exists(NOMBRE_ARCHIVO):
        with open(NOMBRE_ARCHIVO, 'rt', encoding='UTF-8') as archivo:
            datos = json.load(archivo)
            return datos
    else:
        return []

def guardar_archivo(datos):
    with open(NOMBRE_ARCHIVO, 'wt', encoding='UTF-8') as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)


# ==========================================
# RICH 
# ==========================================

console = Console(highlight=False)

def mostrar_tabla_animales(animales):

    if len(animales) == 0:
        advertencia('Todavia no hay animales cargados en el sistema')
        validaciones.pausar()
        return
    

    tabla = Table(
        title='🐶 ANIMALES DEL REFUGIO',
        header_style='bold bright_cyan',
        show_lines=True,
        expand=True
)

    tabla.add_column('ID')
    tabla.add_column('Nombre')
    tabla.add_column('Especie')
    tabla.add_column('Edad')
    tabla.add_column('Fecha de ingreso')
    tabla.add_column('Estado')
    tabla.add_column('Historia')
    tabla.add_column('Rescatado por')

    for animal in animales:
        tabla.add_row(
            str(animal['id']),
            animal['nombre_animal'],
            animal['especie'],
            str(animal['edad_aproximada']),
            str(animal['fecha_ingreso']),
            animal['estado'],
            animal['historia'],
            obtener_nombre_colaborador(animal.get('colaborador_rescate'))
            
        )

    console.print(tabla)


# ==========================================
# FUNCIONES AUXILIARES
# ==========================================


def elegir_colaborador_rescate():
    colaboradores_lista = colaboradores.leer_archivo()

    if not colaboradores_lista:
        advertencia('No hay colaboradores disponibles en este momento..')
        validaciones.pausar()
        return 

    colaboradores.mostrar_tabla_colaboradores(colaboradores_lista)

    id_colaborador = validaciones.ingresar_entero('ID del colaborador que rescató o "0" en caso que no se encuentre en la lista: ', 0)

    if id_colaborador == 0:
        return 

    for colaborador in colaboradores_lista:
        if colaborador["id"] == id_colaborador:
            return id_colaborador 

    error('El ID no pertenece a un colaborador registrado')
    validaciones.pausar()
    return 

def obtener_nombre_colaborador(id_colaborador):
    if id_colaborador is None:
        return 'Desconocido'

    colaboradores_lista = colaboradores.leer_archivo()

    for colab in colaboradores_lista:
        if colab['id'] == id_colaborador:
            return colab['nombre_completo']

    return 'Desconocido'


# ==========================================
# LISTADOS Y FILTROS
# ==========================================
def filtrar_animales_por_estado(estado):
    animales = leer_archivo()
    filtrados = []

    for animal in animales:
        if animal['estado'] == estado:
            filtrados.append(animal)

    if len(filtrados) == 0:
        advertencia('No se encontraron animales en esta lista')
        validaciones.pausar()
        return

    mostrar_tabla_animales(filtrados)
    

def mostrar_lista_animales(): 
    animales = leer_archivo()
    mostrar_tabla_animales(animales)
    


def mostrar_en_refugio():
    filtrar_animales_por_estado(ESTADO_EN_REFUGIO)

def mostrar_en_adopcion():
    filtrar_animales_por_estado(ESTADO_EN_ADOPCION)

def mostrar_adoptados():
    filtrar_animales_por_estado(ESTADO_ADOPTADO)



def menu_filtrar_animales():

    while True:     
        animales = leer_archivo() 
    
        if len(animales) == 0:
            advertencia('Todavía no hay animales registrados en el sistema')
            validaciones.pausar()
            return
        
    
        print('═══════════════════════════════════════════════════')
        titulo ('📋 LISTADO DE ANIMALES')
        print('═══════════════════════════════════════════════════')
        print('1. Ver todos los animales')
        print('2. Ver animales en refugio')
        print('3. Ver animales en adopción')
        print('4. Ver animales adoptados')
        print('0. Volver al menú anterior')

        opcion = validaciones.ingresar_entero('Seleccione una opción: ', 0 , 4)

        match opcion:

            case 0:
                return            
            case 1:
                mostrar_lista_animales()             
            case 2:
                mostrar_en_refugio()
            case 3:
                mostrar_en_adopcion()
            case 4:
                mostrar_adoptados()
            case _:
                error('Opción inválida')


# ==========================================
# CARGA DE ANIMALES
# ==========================================
def pedir_estado_validado() -> str:
    print('═══════════════════════════════════════════════════')
    modificar('Seleccione el nuevo estado del animal')
    print('═══════════════════════════════════════════════════')
    print('1. En refugio')
    print('2. En adopcion')
    print('3. Adoptado')
    
    
    opcion= validaciones.ingresar_entero('Seleccione una opción: ', 1, 3)

    match opcion:
        
        case 1:
            return ESTADO_EN_REFUGIO
        case 2:
            return ESTADO_EN_ADOPCION
        case 3: 
            return ESTADO_ADOPTADO
        case _:
                console.print('Opción inválida')
             



def solicitar_datos_animal():

    nombre = validaciones.validar_texto('Ingrese el nombre del animal: ')
    especie = validaciones.validar_texto('Ingrese la especie del animal (perro, gato, otro): ')
    edad_aproximada = validaciones.ingresar_entero('Ingrese la edad aproximada animal (redondear a enteros): ',1)

    fecha_ingreso = validaciones.validar_fecha('Escriba la fecha de ingreso del animal: ')

    estado = pedir_estado_validado()
    historia = validaciones.entrada_vacia('Cuente cómo llegó el animal al refugio: ')

    return {
        'nombre_animal': nombre,
        'especie': especie,
        'edad_aproximada': edad_aproximada,
        'fecha_ingreso': fecha_ingreso,
        'estado': estado,
        'historia': historia
    }

def cargar_animal():

    while True:
        animales = leer_archivo()
        datos_nuevos = solicitar_datos_animal()
        colaborador_rescate = elegir_colaborador_rescate()

        nuevo_id = 1   
        if len(animales) > 0:
            ultimo_animal = animales[-1]
            nuevo_id = ultimo_animal['id'] + 1
  
    
        animal= {
        'id': nuevo_id,
        'nombre_animal': datos_nuevos['nombre_animal'],
        'especie': datos_nuevos['especie'],
        'edad_aproximada': datos_nuevos['edad_aproximada'],
        'fecha_ingreso': datos_nuevos['fecha_ingreso'],
        'estado': datos_nuevos['estado'],
        'historia': datos_nuevos['historia'],
        'colaborador_rescate': colaborador_rescate

    }

    
        animales.append(animal)
        guardar_archivo(animales)
        exito(f"{datos_nuevos['nombre_animal']} se cargó con éxito con el ID {nuevo_id}")

        if not validaciones.confirmar('¿Desea cargar otro animal? (si/no): '):
            break


# ==========================================
# BÚSQUEDAS
# ==========================================
def busqueda_general_animales(criterio, valor):

    animales = leer_archivo()
    coincidencias = []
    valor_buscado = str(valor).strip().lower()

    for animal in animales:
        dato_animal = str(animal.get(criterio, "")).strip().lower()
        
        if criterio == 'id':
            if valor_buscado == dato_animal:
                coincidencias.append(animal)
        else: 
            if valor_buscado in dato_animal:
                coincidencias.append(animal)
                
    return coincidencias

def buscar_animal_por_nombre():
    nombre = validaciones.validar_texto('Ingrese el nombre del animal: ')
    coincidencias = busqueda_general_animales('nombre_animal', nombre)
    
    if coincidencias:
        mostrar_tabla_animales(coincidencias)        
        return coincidencias
    else:
        advertencia('No existe un animal con ese nombre')
        validaciones.pausar()
    return None

def buscar_animal_por_id():
    id_buscado = validaciones.ingresar_entero('Ingrese el ID del animal: ', 1, None)
    coincidencias = busqueda_general_animales('id', id_buscado)
    
    if coincidencias:
        mostrar_tabla_animales(coincidencias)
        return coincidencias[0]
        
    else:
        advertencia('No existe un animal con ese ID')
        validaciones.pausar()

    return None


def menu_busqueda_animales():

    animales = leer_archivo()
    if len(animales) == 0:
        advertencia('Todavía no hay animales registrados en el sistema')
        validaciones.pausar()
        return


    while True:
        print('═══════════════════════════════════════════════════')
        titulo('🔍 BUSCAR ANIMAL 🔍')
        print('═══════════════════════════════════════════════════')
        print('1. Buscar por nombre')
        print('2. Buscar por ID')
        print('0. Volver al menú anterior')
    

        opcion = validaciones.ingresar_entero('Seleccione una opción: ',0,2)
        match opcion:

            case 0:
                return        
            case 1:
                buscar_animal_por_nombre()            
            case 2:
                buscar_animal_por_id()
            case _:
                error('Opción inválida')
                
        


# ==========================================
# MODIFICACIONES
# ==========================================
def actualizar_estado_en_json(id_animal: int, nuevo_estado: str):
    animales_completos = leer_archivo()
    for animal in animales_completos:
        if animal['id'] == id_animal:
            animal['estado'] = nuevo_estado
            
            guardar_archivo(animales_completos)
  
            print('═══════════════════════════════════════════════════')
            exito('ESTADO ACTUALIZADO CORRECTAMENTE')
            print('═══════════════════════════════════════════════════')


            mostrar_tabla_animales([animal])
            break


def elegir_animal_por_id(coincidencias: list) -> int:
    
    ids_validos = [animal['id'] for animal in coincidencias]

    while True:
        id_elegido = validaciones.ingresar_entero('Ingrese el ID del animal: ', 1)

        if id_elegido in ids_validos:
            return id_elegido

        error('El ID no pertenece a la lista mostrada')


def cambiar_estado_animal():

    animales = leer_archivo()

    if len(animales) == 0:
        advertencia('Todavía no hay animales registrados en el sistema')
        return

    while True:
        coincidencias = buscar_animal_por_nombre()

        if not coincidencias:
            return

    
        id_elegido = elegir_animal_por_id(coincidencias)
        nuevo_estado = pedir_estado_validado()

        actualizar_estado_en_json(id_elegido, nuevo_estado)

        if not validaciones.confirmar('¿Desea cambiar el estado de otro animal? (si/no): '):
            return


# ==========================================
# BAJAS
# ==========================================
def eliminar_animal_en_json(id_animal):

    animales = leer_archivo()

    posicion = -1
        

    for i in range(len(animales)):
        if animales[i]["id"] == id_animal:
            posicion = i
            break


    if posicion != -1:
        nombre = animales[posicion]["nombre_animal"]
        del animales[posicion]
        guardar_archivo(animales)

        exito(f"El animal '{nombre}' fue eliminado correctamente")

    else:
        error('No se encontró el animal')   


def baja_animal():

    animales = leer_archivo()

    if len(animales) == 0:
        advertencia('Todavía no hay animales registrados en el sistema')
        return

    while True:
        print('═══════════════════════════════════════════════════')
        eliminar('PROCESO DE ELIMINACIÓN DEFINITIVA')
        print('═══════════════════════════════════════════════════')
    
        coincidencias = buscar_animal_por_nombre()
        if coincidencias is None:
            return
        
        id_elegido = elegir_animal_por_id(coincidencias)
    
        eliminar('ADVERTENCIA: SI CONTINÚA EL REGISTRO SERÁ ELIMINADO COMPLETAMENTE')
            
        if validaciones.confirmar(f'¿Está completamente seguro de eliminar el ID #{id_elegido}? (si/no): '):
            eliminar_animal_en_json(id_elegido)
        else:
            exito('Operación cancelada. El registro no sufrió modificaciones')


        if not validaciones.confirmar('¿Desea eliminar otro animal? (si/no): '):
            return


# ==========================================
# MENÚ PRINCIPAL ANIMALES
# ==========================================
def menu_pantalla():
    print('═══════════════════════════════════════════════════')
    titulo('🐶 ANIMALES DEL REFUGIO 🐶')
    print('═══════════════════════════════════════════════════')
    print('1 -➕ Cargar animal nuevo')
    print('2 -📋 Ver listado de animales')
    print('3 -🔍 Buscar animal')
    print('4 -🔄 Actualizar estado de un animal')
    print('5 -❌ Dar de baja un animal')
    print('0 -🔙 Volver a la pantalla principal')
    print('═══════════════════════════════════════════════════')    
    print('¿Qué querés hacer?')


def menu_animales():
    while True:
        menu_pantalla()
        opcion= validaciones.ingresar_entero (' Ingresá una Opción: ',0 ,5)
        match opcion:
            case 0:
                print('Volviendo al menú principal... ')
                return  
            case 1:
                cargar_animal()
            case 2:
                menu_filtrar_animales()
            case 3:
                menu_busqueda_animales()
            case 4:
                cambiar_estado_animal()
            case 5:
                baja_animal()
            case _:
                error('Opción inválida')
