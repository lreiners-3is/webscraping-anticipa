"""Ejecuta solo el módulo 7 (SENAMHI Alertas) de Webscraping_Consolidado.ipynb.

El sitio del SENAMHI no responde desde los servidores de GitHub, así que este
módulo corre aparte, en un runner propio (flujo .github/workflows/senamhi.yml).
Corre las celdas igual que ejecutar_notebook.py, pero tras la configuración
apaga los demás módulos y enciende SENAMHI. El notebook no se modifica.
"""
import json
import sys
from pathlib import Path

NOTEBOOK = Path(__file__).resolve().parent.parent / "Webscraping_Consolidado.ipynb"
OTROS_MODULOS = ["EJECUTAR_OSPA", "EJECUTAR_BOLETINES", "EJECUTAR_MONITOR", "EJECUTAR_INAMHI",
                 "EJECUTAR_INAMHI_BOLETINES", "EJECUTAR_INAMHI_PRONOSTICO"]


def main():
    cuaderno = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    entorno = {"__name__": "__main__"}

    for celda in cuaderno["cells"]:
        fuente = "".join(celda["source"])
        if celda["cell_type"] != "code" or "%pip" in fuente:
            continue
        exec(compile(fuente, celda.get("id", "celda"), "exec"), entorno)
        if "EJECUTAR_SENAMHI" in entorno and "EJECUTAR_SENAMHI" in fuente:
            faltan = [m for m in OTROS_MODULOS if m not in entorno]
            if faltan:
                raise RuntimeError(f"La configuración no define: {', '.join(faltan)}")
            entorno.update({m: False for m in OTROS_MODULOS}, EJECUTAR_SENAMHI=True)

    fallidos = [m["Módulo"] for m in entorno["resumen_modulos"] if m["Estado"] == "FALLÓ"]
    if fallidos:
        print("Módulos con fallo:", ", ".join(fallidos))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
