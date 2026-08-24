from datetime import datetime

# validar numero
def validar_entero(mensaje):
    while True:
        dato = input(mensaje)

        if dato.isdigit():
            return int(dato)

        print("❌ Error. Debe ingresar un número.")


# validar fecha real


def validar_fecha(mensaje):
    while True:
        fecha = input(mensaje)

        try:
            fecha_dt = datetime.strptime(fecha, "%d/%m/%Y")
            hoy = datetime.now()

            # 🔥 comparar SOLO fecha (sin hora)
            if fecha_dt.date() > hoy.date():
                print("❌ La fecha no puede ser futura.")
                continue

            return fecha

        except ValueError:
            print("❌ Fecha inválida. Use dd/mm/aaaa")