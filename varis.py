import os

carpetes = [
    "ADG32O_02.01",
    "ADG32O_02.02",
    "ADG32O_02.03",
    "ADG32O_02.04",
    "ADG32O_02.05",
    "ADG32O_02.06",
    "ADG32O_02.07",
    "ADG32O_02.08",
    "ADG32O_02.09",
    "ADG32O_02.10",
    "ADG32O_02.11",
    "ADG32O_02.13",
    "ADG32O_02.14",
    "ADG32O_02.15",
    "ADG32O_02.16",
    "ADG32O_02.17",
    "ADG32O_02.18",
    "ADG32O_02.19",
    "ADG32O_02.20",
    "ADG32O_02.21",
    "ADG32O_02.22",
    "ADG32O_02.23",
    "ADG32O_02.24",
    "ADG32O_02.25",
    "ADG32O_02.26",
    "ADG32O_02.27",
    "ADG32O_02.28",
    "ADG32O_02.29",
    "ADG32O_02.30",
    "ADG32O_02.31",
    "ADG32O_02.32",
    "ADG32O_02.33",
    "ADG32O_02.34",
    "ADG32O_02.35",
    "ADG32O_02.36",
    "ADG32O_02.37",
    "ADG32O_02.38",
    "ADG32O_02.39",
    "ADG32O_02.40",
    "ADG32O_02.41",
    "ADG32O_02.42",
    "ADG32O_02.43",
    "ADG32O_02.44",
    "ADG32O_02.45",
    "ADG32O_02.46",
    "ADG32O_02.47",
    "ADG32O_02.48",
    "ADG32O_02.49",
    "ADG32O_02.50",
    "ADG21O_02.01",
    "ADG21O_02.02",
    "ADG21O_02.03",
    "ADG21O_02.04",
    "ADG21O_02.05",
    "ADG21O_02.06",
    "ADG21O_02.07",
    "ADG21O_02.08",
    "ADG21O_02.09",
    "ADG21O_02.10",
    "ADG21O_02.11",
    "ADG21O_02.13",
    "ADG21O_02.14",
    "ADG21O_02.15",
    "ADG21O_02.16",
    "ADG21O_02.17",
    "ADG21O_02.18",
    "ADG21O_02.19",
    "ADG21O_02.20",
    "ADG21O_02.21",
    "ADG21O_02.22",
    "ADG21O_02.23",
    "ADG21O_02.24",
    "ADG21O_02.25",
    "ADG21O_02.26",
    "ADG21O_02.27",
    "ADG21O_02.28",
    "ADG21O_02.29",
    "ADG21O_02.30",
    "ADG21O_02.31",
    "ADG21O_02.32",
    "ADG21O_02.33",
    "ADG21O_02.34",
    "ADG21O_02.35",
    "ADG21O_02.36",
    "ADG21O_02.37",
    "ADG21O_02.38",
    "ADG21O_02.39",
    "ADG21O_02.40",
    "ADG21O_02.41",
    "ADG21O_02.42",
    "ADG21O_02.43",
    "ADG21O_02.44",
    "ADG21O_02.45",
    "ADG21O_02.46",
    "ADG21O_02.47",
    "ADG21O_02.48",
    "ADG21O_02.49",
    "ADG21O_02.50",
]


def creaDirectori(carpetes):
    for carpeta in carpetes:
        rutaFinsInput = os.getcwd() + "/" + "LLISTATS_INPUT"
        rutaFinsOutput = os.getcwd() + "/" + "LLISTATS_OUTPUT"
        os.mkdir(rutaFinsInput + "/" + carpeta)
        ruta = rutaFinsInput + "/" + carpeta
        # Instrucción para crear el .gitkeep
        with open(ruta + "/.gitkeep", "w") as f:
            pass
        os.mkdir(rutaFinsOutput + "/" + carpeta)
        ruta = rutaFinsOutput + "/" + carpeta
        # Instrucción para crear el .gitkeep
        with open(ruta + "/.gitkeep", "w") as f:
            pass
    return carpetes


creaDirectori(carpetes)
