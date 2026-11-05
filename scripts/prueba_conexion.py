"""Comprueba si este entorno puede conectarse a las fuentes del proyecto.

No usa claves ni guarda nada. Termina con error si alguna fuente no responde.
"""
import sys
import time

import requests

USER_AGENT = "IDEAM-OSPA-Research/1.0"
INTENTOS = 3
PAUSA_SEGUNDOS = 10

FUENTES = {
    "OSPA, robots.txt": "https://bart.ideam.gov.co/robots.txt",
    "OSPA, carpeta de alertas": "https://bart.ideam.gov.co/ospa/DatosAbiertos/Alertas_Meteomarinas/",
    "OSPA, archivo CSV": "https://bart.ideam.gov.co/ospa/DatosAbiertos/Alertas_Meteomarinas/alertas_meteomarinas.csv",
    "Boletines, robots.txt": "https://www.ideam.gov.co/robots.txt",
    "Boletines, página principal": "https://www.ideam.gov.co/sala-de-prensa/boletines",
    "Monitor, GitHub": "https://api.github.com/repos/3is-global/echo_dp_amazon_monitor",
}

# OSPA no publica robots.txt: responder 404 también demuestra que hay conexión.
CODIGOS_VALIDOS = {"OSPA, robots.txt": {200, 404}}


def probar(nombre, url):
    validos = CODIGOS_VALIDOS.get(nombre, {200})
    for intento in range(1, INTENTOS + 1):
        inicio = time.monotonic()
        try:
            with requests.get(
                url, headers={"User-Agent": USER_AGENT},
                timeout=(15, 45), stream=True,
            ) as respuesta:
                next(respuesta.iter_content(4096), b"")
                codigo = respuesta.status_code
            duracion = time.monotonic() - inicio
            print(f"  Intento {intento}: HTTP {codigo} en {duracion:.1f} s")
            if codigo in validos:
                return True
        except requests.RequestException as error:
            duracion = time.monotonic() - inicio
            print(f"  Intento {intento}: {type(error).__name__} en {duracion:.1f} s")
        if intento < INTENTOS:
            time.sleep(PAUSA_SEGUNDOS)
    return False


def main():
    resultados = {}
    for nombre, url in FUENTES.items():
        print(f"{nombre}\n  {url}", flush=True)
        resultados[nombre] = probar(nombre, url)

    print("\nRESUMEN")
    for nombre, correcto in resultados.items():
        print(f"  {'OK   ' if correcto else 'FALLA'} {nombre}")

    return 0 if all(resultados.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
