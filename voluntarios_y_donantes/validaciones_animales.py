
from datetime import date

# ==========================================
# VALIDACIONES PARA ANIMALES Y COLABORADORES
# ==========================================


def validar_fecha(mensaje: str, anio_min: int = 2023) -> str:
    print(mensaje)
    hoy = date.today()

    anio = ingresar_entero(f'Escriba el año: ', anio_min, hoy.year)

    mes_maximo = hoy.month if anio == hoy.year else 12

    mes = ingresar_entero(f'Escriba el mes: ', 1, mes_maximo)

    if mes in [4, 6, 9, 11]:
        dias_maximos = 30
    elif mes == 2:
        dias_maximos = 29 if anio % 4 == 0 else 28
    else:
        dias_maximos = 31

    if anio == hoy.year and mes == hoy.month:
        dias_maximos = hoy.day

    dia = ingresar_entero(f'Escriba el día : ', 1, dias_maximos)

    return date(anio, mes, dia).isoformat()


def ingresar_entero(msj: str, minimo: int = 0, maximo: int = None) ->int:
    while True: 
        a_retornar = input(msj).strip()

        if not a_retornar.isnumeric():
            print('El valor ingresado no es numerico: ')
            continue

        numero = int(a_retornar)
        
        if numero < minimo:
                print(f'El valor ingresado debe ser mayor o igual a {minimo}: ')
                continue 
        
        if maximo is not None and numero > maximo:
                print(f'El valor ingresado no puede ser mayor a {maximo}')
                continue
        return numero
    

def validar_texto(msj:str)->str:
    while True:
        a_retornar = input(msj).strip()
        if a_retornar != "" and a_retornar.replace(" ", "").isalpha():
            return a_retornar.title()
        print('El valor ingresado debe contener solo letras y no quedar vacío.' )  




def entrada_vacia (msj:str)->str:
    while True:
        a_retornar = input(msj).strip()
        if a_retornar == '':
            print('El campo no puede quedar vacío, ingrese un valor: ')
            continue
       
        return a_retornar
    


# ==========================================
# FUNCION AUXILIAR PARA ANIMALES Y COLABORADORES
# ==========================================

def confirmar(mensaje: str) -> bool:
    while True:
        respuesta = input(mensaje).strip().lower()

        if respuesta in ('s', 'si'):
            return True
        elif respuesta in ('n', 'no'):
            return False
        else:
            print('Ingrese si o no')


        
def pausar():
    input('Presione Enter para continuar...')