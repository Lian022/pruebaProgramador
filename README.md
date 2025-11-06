# Solución - Prueba Técnica GERPRO

Este repositorio contiene la solución a la prueba técnica para la posición de Programador 1 en GERPRO. El proyecto aborda las dos partes solicitadas en el documento:

1. **Lógica (Python):** Un script que calcula el flujo de financiación (desembolsos de crédito y aportes de capital) basado en un FCO y reglas de crédito específicas.
2. **Modelos (Django):** Un archivo `models.py` que define la estructura de la base de datos para el proyecto inmobiliario.

---

## 1. Lógica (Script de Python)

El archivo `finance.py` contiene la función principal `calcular_flujo_financiacion`.

### Cómo Ejecutar

El script está diseñado para ejecutarse directamente y probar la lógica con los datos de ejemplo proporcionados en la prueba.

**a. Instalación de dependencias:**
El script requiere la librería `requests` para descargar los datos de ejemplo desde la URL.

```bash
pip install requests
```

**b. Ejecución del script:**

```bash
python activo/finance
```

### Estructura del Proyecto

```
pruebaProgramador/
├── README.md
├── manage.py
├── activo/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── finance          # Script principal de lógica financiera
│   ├── models.py        # Modelos Django
│   ├── tests.py
│   ├── views.py
│   └── migrations/
│       └── __init__.py
└── mysite/
    ├── __init__.py
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

### Funcionalidad Principal

La función `calcular_flujo_financiacion` recibe los siguientes parámetros:

- `datos`: Lista de registros con información de ingresos y costos por período
- `cupo_credito`: Monto máximo del crédito disponible
- `porcentaje_max_desembolso`: Porcentaje máximo que se puede desembolsar mensualmente
- `periodo_inicial_credito`: Período en que inicia la disponibilidad del crédito
- `periodo_final_credito`: Período en que termina la disponibilidad del crédito
- `tasa_interes`: Tasa de interés anual

### Resultados

El script retorna dos listas:
- **Desembolsos de crédito**: Montos y períodos en los que se realizan desembolsos
- **Aportes de capital**: Montos y períodos en los que se requieren aportes adicionales

---

## 2. Modelos Django

El archivo `activo/models.py` contiene la definición de los modelos para manejar la información del proyecto inmobiliario, incluyendo:

- Estructura de la base de datos
- Relaciones entre entidades
- Campos necesarios para el flujo de financiación

### Configuración del Proyecto Django

Para usar los modelos Django:

1. **Instalar Django y Psycopg2-binary:**
```bash
pip install django psycopg2-binary
```

2. **Realizar migraciones:**
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Tecnologías Utilizadas

- **Python 3.13+**
- **Django** (para los modelos)
- **requests** (para obtener datos de la API)

## Autor

Solución desarrollada para la prueba técnica de GERPRO - Programador 1.
