"""Ejecuta Webscraping_Consolidado.ipynb fuera de Colab.

Corre las celdas de código en orden, omitiendo las instalaciones con %pip.
Termina con error si algún módulo falló, para que GitHub lo marque y avise.
"""
import json
import sys
from pathlib import Path

NOTEBOOK = Path(__file__).resolve().parent.parent / "Webscraping_Consolidado.ipynb"


def main():
    cuaderno = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    entorno = {"__name__": "__main__"}

    for celda in cuaderno["cells"]:
        fuente = "".join(celda["source"])
        if celda["cell_type"] == "code" and "%pip" not in fuente:
            exec(compile(fuente, celda.get("id", "celda"), "exec"), entorno)

    fallidos = [
        m["Módulo"] for m in entorno["resumen_modulos"] if m["Estado"] == "FALLÓ"
    ]
    if fallidos:
        print("Módulos con fallo:", ", ".join(fallidos))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
