import os
import json
from rich.console import Console
from rich.table import Table
from voluntarios_y_donantes import validaciones_animales as validaciones
from ui_menu_general import exito, error, advertencia, modificar, eliminar, titulo

# ==========================================
# CONSTANTES
# ==========================================

BASE_DIR = os.path.dirname(__file__)
NOMBRE_ARCHIVO = os.path.join(BASE_DIR, "datos", "colaboradores.json")

TIPO_VOLUNTARIO = "voluntario"
TIPO_DONANTE = "donante"
TIPO_AMBOS = "ambos"

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

def mostrar_tabla_colaboradores(colaboradores):
    tabla = Table(
        title='🤝 VOLUNTARIO/DONANTE',
        header_style='bold cyan',
        show_lines=True,
        expand=True
    )

    tabla.add_column('ID')
    tabla.add_column('Nombre completo')
    tabla.add_column('Teléfono')
    tabla.add_column('Tipo de aporte')
    tabla.add_column('Tarea o recurso')
    tabla.add_column('Último aporte')
    tabla.add_column('Total aportes')

    for colaborador in colaboradores:
        tabla.add_row(
            str(colaborador['id']),
            colaborador['nombre_completo'],
            str(colaborador['telefono']),
            colaborador['tipo_aporte'],
            colaborador['tarea_o_recurso'],
            str(colaborador['ultimo_aporte']),
            str(colaborador['total_aportes'])
        )

    console.print(tabla)



# ==========================================
# LISTADOS Y FILTROS
# ==========================================

def mostrar_lista_colaboradores():
    colaboradores = leer_archivo()
    mostrar_tabla_colaboradores(colaboradores)
    validaciones.pausar()


def filtrar_colaboradores_por_tipo(tipo: str):
    colaboradores = leer_archivo()
    filtrados = []

    for colaborador in colaboradores:
        if colaborador['tipo_aporte'] == tipo:
            filtrados.append(colaborador)


    if len(filtrados) == 0:
        advertencia(' No se encontraron colaboradores en esta lista')
        validaciones.pausar()
        return
   
    mostrar_tabla_colaboradores(filtrados)
    validaciones.pausar()



def menu_filtrar_colaboradores():
    
    while True:

        colaboradores = leer_archivo()

        if len(colaboradores) == 0:
            advertencia('Todavía no hay colaboradores registrados en el sistema')
            validaciones.pausar()
            return

        print('═══════════════════════════════════════════════════')
        titulo('📋 LISTADO DE COLABORADORES')
        print('═══════════════════════════════════════════════════')
        print('1. Ver todos los colaboradores')
        print('2. Ver voluntarios')
        print('3. Ver donantes')
        print('4. Ver ambos')
        print('0. Volver al menú')

        opcion = validaciones.ingresar_entero('Seleccione una opción: ', 0, 4)

        match opcion:

            case 0:
                print('Volviendo al menú anterior..')
                return            
            case 1:
                mostrar_lista_colaboradores()
            case 2:
                filtrar_colaboradores_por_tipo(TIPO_VOLUNTARIO)
            case 3:
                filtrar_colaboradores_por_tipo(TIPO_DONANTE)
            case 4:
                filtrar_colaboradores_por_tipo(TIPO_AMBOS)
            case _:
                error('Opción inválida')

        
        
# ==========================================
# CARGA DE COLABORADORES
# ==========================================

def pedir_tipo_colaborador() -> str:
    print('═══════════════════════════════════════════════════')
    titulo('Seleccione el tipo de Colaborador')
    print('═══════════════════════════════════════════════════')
    print('1. Voluntario')
    print('2. Donante')
    print('3. Ambos')
    
    
    
    opcion= validaciones.ingresar_entero('Seleccione una opción: ', 0, 3)

    match opcion:      
  
        case 1:
            return TIPO_VOLUNTARIO        
        case 2:
            return TIPO_DONANTE        
        case 3: 
            return TIPO_AMBOS



def solicitar_datos_colaborador():

    nombre_completo = validaciones.validar_texto('Ingrese el nombre completo del colaborador: ')
    telefono = validaciones.ingresar_entero('Ingrese el teléfono del colaborador: ')
    tipo_aporte = pedir_tipo_colaborador()
    tarea_o_recurso = validaciones.validar_texto('Ingrese la tarea realizada por el colaborador: ')

    ultimo_aporte = validaciones.validar_fecha('Ingrese la fecha del aporte: ')
    

    return {
        'nombre_completo': nombre_completo,
        'telefono': telefono,
        'tipo_aporte': tipo_aporte,
        'tarea_o_recurso': tarea_o_recurso,
        'ultimo_aporte': ultimo_aporte,
        'total_aportes': 1
    }

def cargar_colaborador():
    
    while True:

        colaboradores = leer_archivo()        
        datos_nuevos = solicitar_datos_colaborador()

        nuevo_id = 1   
        if len(colaboradores) > 0:
            ultimo_colaborador = colaboradores[-1]
            nuevo_id = ultimo_colaborador['id'] + 1
  
    
        colaborador= {
        'id': nuevo_id,
        'nombre_completo': datos_nuevos['nombre_completo'],
        'telefono': datos_nuevos['telefono'],
        'tipo_aporte': datos_nuevos['tipo_aporte'],
        'tarea_o_recurso': datos_nuevos['tarea_o_recurso'],
        'ultimo_aporte': datos_nuevos['ultimo_aporte'],
        'total_aportes': 1
       
    }

    
        colaboradores.append(colaborador)
        guardar_archivo(colaboradores)
        exito(f"{datos_nuevos['nombre_completo']} se cargó con éxito con el ID {nuevo_id}")

        if not validaciones.confirmar('¿Desea cargar otro colaborador? (si/no): '):
            break


# ==========================================
# BÚSQUEDAS
# ==========================================
def busqueda_general_colaboradores(criterio, valor):

    colaboradores = leer_archivo()
    coincidencias = []
    valor_buscado = str(valor).strip().lower()

    for colaborador in colaboradores:
        dato_colaborador = str(colaborador.get(criterio, "")).strip().lower()
        
        if criterio == 'id':
            if valor_buscado == dato_colaborador:
                coincidencias.append(colaborador)
        else:
            if valor_buscado in dato_colaborador:
                coincidencias.append(colaborador)
                
    return coincidencias

def buscar_colaborador_por_nombre():
    nombre = validaciones.validar_texto('Ingrese el nombre del colaborador: ')
    coincidencias = busqueda_general_colaboradores('nombre_completo', nombre)
    
    if coincidencias:
        mostrar_tabla_colaboradores(coincidencias)
        return coincidencias
    else: 
        advertencia('No existe un Colaborador con ese nombre')
        validaciones.pausar()

    return None

def buscar_colaborador_por_id():
    id_buscado = validaciones.ingresar_entero('Ingrese el ID del colaborador: ', 1, None)
    coincidencias = busqueda_general_colaboradores('id', id_buscado)
    
    if coincidencias:
        mostrar_tabla_colaboradores(coincidencias)
        return coincidencias[0] 
    advertencia('No existe un colaborador con ese ID')
    validaciones.pausar()

    return None



def menu_busqueda_colaboradores():

    colaboradores = leer_archivo()
    if len(colaboradores) == 0:
        advertencia('Todavía no hay colaboradores registrados en el sistema')
        validaciones.pausar()
        return


    while True:
        print('═══════════════════════════════════════════════════')
        titulo('🔍 BUSCAR COLABORADOR 🔍')
        print('═══════════════════════════════════════════════════')
        print('1. Buscar por nombre')
        print('2. Buscar por ID')
        print('0. Volver al menú anterior')
    

        opcion = validaciones.ingresar_entero('Seleccione una opción: ',0,2)
        match opcion:

            case 0:
                print('Volviendo al menú..')
                return        
            case 1:
                buscar_colaborador_por_nombre()                
            case 2:
                buscar_colaborador_por_id()
            case _:
                error('Opción inválida')
                

        

# ==========================================
# MODIFICACIONES
# ==========================================


def elegir_colaborador_por_id(coincidencias: list) -> int:
    
    while True:
        id_elegido = validaciones.ingresar_entero('Ingrese el ID decolaborador: ', 1)

        for colaborador in coincidencias:
            if colaborador['id'] == id_elegido:
                return id_elegido

        advertencia('El ID ingresado no corresponde a ningún colaborador del refugio')


def registrar_colaboracion(id_colaborador, tarea, fecha):
    colaboradores = leer_archivo()

    for colaborador in colaboradores:
        if colaborador['id'] == id_colaborador:

            colaborador['ultimo_aporte'] = fecha
            colaborador['total_aportes'] += 1
            colaborador['tarea_o_recurso'] = tarea

            guardar_archivo(colaboradores)

            exito('Nueva colaboración registrada')
            mostrar_tabla_colaboradores([colaborador])
            return
        
    
    advertencia('Colaborador no encontrado')


def menu_registrar_colaboracion():
    while True:
        coincidencias = buscar_colaborador_por_nombre()

        if not coincidencias:
            return

        id_elegido = elegir_colaborador_por_id(coincidencias)

        tarea = validaciones.validar_texto('Tarea o recurso: ')
        fecha = validaciones.validar_fecha('Ingrese la fecha del aporte: ')

        registrar_colaboracion(id_elegido, tarea, fecha)
        if not validaciones.confirmar('¿Desea agregar otra colaboración? (si/no): '):
            return

# ==========================================
# BAJAS
# ==========================================

def eliminar_colaborador_en_json(id_colaborador):

    colaboradores = leer_archivo()

    posicion = -1

    for i in range(len(colaboradores)):
        if colaboradores[i]['id'] == id_colaborador:
            posicion = i
            break

    if posicion != -1:
        nombre_completo = colaboradores[posicion]['nombre_completo']
        del colaboradores[posicion]
        guardar_archivo(colaboradores)

        exito(f"El colaborador '{nombre_completo}' fue eliminado correctamente")
    
    else:
        error('No se encontró el colaborador')



def baja_colaborador():

    colaboradores = leer_archivo()

    if len(colaboradores) == 0:
        advertencia('Todavía no hay colaboradores registrados en el sistema')
        validaciones.pausar()
        return

    while True:
        print('═══════════════════════════════════════════════════')
        titulo('🚨PROCESO DE ELIMINACIÓN DEFINITIVA🚨')
        print('═══════════════════════════════════════════════════')
    
        coincidencias = buscar_colaborador_por_nombre()
        if coincidencias is None:
            return
        
        id_elegido = elegir_colaborador_por_id(coincidencias)
    
        eliminar('ADVERTENCIA: SI CONTINÚA EL REGISTRO SERÁ ELIMINADO COMPLETAMENTE')
        seguro = input(f'¿Está completamente seguro de eliminar el ID #{id_elegido}? (si/no): ').strip().lower()
    
        if seguro == 'si':
            eliminar_colaborador_en_json(id_elegido)
        else:
            exito('Operación cancelada. El registro no sufrió modificaciones')


        if not validaciones.confirmar('¿Desea eliminar otro colaborador? (si/no): '):
            return


# ==========================================
# MENÚ PRINCIPAL COLABORADORES
# ==========================================

def menu_pantalla():
    print('═══════════════════════════════════════════════════')
    titulo('🤝 COLABORADORES DEL REFUGIO 🤝')
    print('═══════════════════════════════════════════════════')
    print('1 -➕ Cargar colaborador nuevo')
    print('2 -📋 Ver listado de colaboradores')
    print('3 -🔍 Buscar colaborador')
    print('4 -🔄 Actualizar la fecha de colaboración')
    print('5 -❌ Dar de baja un colaborador')
    print('0 -🔙 Volver a la pantalla principal')
    print('═══════════════════════════════════════════════════')    
    print('¿Qué querés hacer?')


def menu_colaboradores():
    while True:
        menu_pantalla()
        opcion = validaciones.ingresar_entero ('Ingresá una Opción: ',0 ,5)
        match opcion: 

            case 0:
                print('Volviendo al menú principal... ')
                return
            case 1:
                cargar_colaborador()
            case 2:
                menu_filtrar_colaboradores()
            case 3:
                menu_busqueda_colaboradores()
            case 4:
                menu_registrar_colaboracion()
            case 5:
                baja_colaborador()
            case _:
                error('Opción inválida')



