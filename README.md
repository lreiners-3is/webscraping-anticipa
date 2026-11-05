# Webscraping Anticipa

Recolección automatizada de alertas y boletines públicos para un sistema de consulta documental. Las salidas se guardan en Google Drive.

## Contenido

| Archivo | Para qué sirve |
|---|---|
| `Webscraping_Consolidado.ipynb` | Proceso de extracción, con sus tres módulos |
| `scripts/ejecutar_notebook.py` | Ejecuta el notebook en GitHub Actions |
| `.github/workflows/extraccion.yml` | Flujo principal de extracción |
| `.github/workflows/prueba-conexion.yml` | Prueba manual de conexión con las fuentes |

## Ejecución

Desde la pestaña **Actions**, flujo **Extracción**, botón **Run workflow**. Si un módulo falla, los demás siguen y la ejecución queda marcada con error.

## Claves

Este repositorio es público y no debe contener claves, datos ni salidas. El acceso a Drive se guarda en el GitHub Secret `RCLONE_CONF`.
