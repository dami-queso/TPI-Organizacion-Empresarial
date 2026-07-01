import csv

ARCHIVO_USUARIOS = "USUARIOS.csv"
ARCHIVO_SOLICITUDES = "SOLICITUDES.csv"


# ==========================
# USUARIOS
# ==========================

def cargar_usuarios():
    """Lee el archivo usuarios.csv"""

    usuarios = []

    try:
        with open(ARCHIVO_USUARIOS, mode="r", encoding="utf-8") as archivo:

            lector = csv.DictReader(archivo)

            for fila in lector:
                fila["saldo_vacaciones"] = int(fila["saldo_vacaciones"])
                usuarios.append(fila)

    except FileNotFoundError:
        print("Error: no se encontró usuarios.csv")

    return usuarios


def guardar_usuarios(usuarios):
    """Guarda la lista de usuarios."""

    with open(
        ARCHIVO_USUARIOS,
        mode="w",
        newline="",
        encoding="utf-8"
    ) as archivo:

        campos = [
            "user_id",
            "nombre",
            "saldo_vacaciones"
        ]

        escritor = csv.DictWriter(
            archivo,
            fieldnames=campos
        )

        escritor.writeheader()

        escritor.writerows(usuarios)


# ==========================
# SOLICITUDES
# ==========================

def cargar_solicitudes():
    """Lee el archivo solicitudes.csv"""

    solicitudes = []

    try:

        with open(
            ARCHIVO_SOLICITUDES,
            mode="r",
            encoding="utf-8"
        ) as archivo:

            lector = csv.DictReader(archivo)

            for fila in lector:

                fila["dias"] = int(fila["dias"])

                solicitudes.append(fila)

    except FileNotFoundError:

        print("Error: no se encontró solicitudes.csv")

    return solicitudes


def guardar_solicitudes(solicitudes):
    """Guarda las solicitudes."""

    with open(
        ARCHIVO_SOLICITUDES,
        mode="w",
        newline="",
        encoding="utf-8"
    ) as archivo:

        campos = [
            "solicitud_id",
            "user_id",
            "fecha_inicio",
            "fecha_fin",
            "dias",
            "estado",
            "aprobador_id",
            "comentario",
            "fecha_creacion"
        ]

        escritor = csv.DictWriter(
            archivo,
            fieldnames=campos
        )

        escritor.writeheader()

        escritor.writerows(solicitudes)