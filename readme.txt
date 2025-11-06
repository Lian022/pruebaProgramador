# Solución - Prueba Técnica GERPRO

Este repositorio contiene la solución a la prueba técnica para la posición de Programador 1 en GERPRO. El proyecto aborda las dos partes solicitadas en el documento:

1.  **Lógica (Python):** Un script que calcula el flujo de financiación (desembolsos de crédito y aportes de capital) basado en un FCO y reglas de crédito específicas.
2.  **Modelos (Django):** Un archivo `models.py` que define la estructura de la base de datos para el proyecto inmobiliario.

---

## 1. Lógica (Script de Python)

El archivo `finance.py` contiene la función principal `calcular_flujo_financiacion`.

### Cómo Ejecutar

El script está diseñado para ejecutarse directamente y probar la lógica con los datos de ejemplo proporcionados en la prueba.

**a. Instalación de dependencias:**
El script requiere la librería `requests` para descargar los datos de ejemplo desde la URL.

```bash
pip install requests