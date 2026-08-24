import json
import os

RUTA_ARCHIVO = os.path.join(
    os.path.dirname(__file__),
    "atenciones.json"
)


def guardar_atenciones(atenciones):

    with open(
        RUTA_ARCHIVO,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            atenciones,
            archivo,
            indent=4,
            ensure_ascii=False
        )


def cargar_atenciones():

    try:

        with open(
            RUTA_ARCHIVO,
            "r",
            encoding="utf-8"
        ) as archivo:

            return json.load(archivo)

    except FileNotFoundError:

        return []