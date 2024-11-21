# Extracción de Datos del BORME para Análisis de Aperturas de Empresas

Este proyecto automatiza la extracción y análisis de información sobre aperturas de empresas y cambios sociales registrados en el Boletín Oficial del Registro Mercantil (BORME). Está diseñado para analizar archivos PDF publicados diariamente, identificar eventos relevantes y estructurar los datos para su posterior procesamiento.

## Tabla de Contenidos
- [Descripción](#descripción)
- [Datos](#datos)
- [Metodología](#metodología)
- [Resultados](#resultados)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Scripts Adicionales](#scripts-adicionales)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

## Descripción

El proyecto permite identificar y extraer información clave sobre la constitución de empresas, cambios de objeto social y traslados de domicilio social en el BORME. La lógica de extracción ha sido adaptada a la actualización de la API del BORME del **1 de noviembre de 2024**, lo que garantiza compatibilidad con los nuevos formatos y estructuras de datos publicados.

## Datos

El proyecto utiliza los datos abiertos del BORME proporcionados por el sitio oficial del Boletín Oficial del Estado (BOE). Estos datos están disponibles en formato XML y PDF, permitiendo analizar:

- **Eventos legales**: constitución, cambios de domicilio social, y más.
- **Información geográfica**: ubicación de empresas por provincia.
- **Datos administrativos**: nombres de administradores, presidentes o responsables legales.

## Metodología

El proyecto se estructura en las siguientes fases:

1. **Extracción de Datos**:
   - Descarga automática de archivos XML y PDF desde el BOE.
   - Conversión del contenido en texto legible.

2. **Procesamiento de la Información**:
   - Identificación de eventos relevantes mediante palabras clave configurables.
   - Extracción de domicilios sociales y nombres de administradores.

3. **Análisis de Actividades**:
   - Extracción de las actividades principales mencionadas en el BORME.
   - Identificación de frases frecuentes para estudios sectoriales.

4. **Automatización**:
   - Ejecución diaria para procesar datos del día anterior.

5. **Estructuración de los Datos**:
   - Organización en un formato estructurado (diccionarios, JSON, o bases de datos).
   - Asignación de metadatos, como provincia y fecha.

## Resultados

El proyecto extrae información relevante con alta precisión y permite:

- Identificar empresas constituidas recientemente por provincia.
- Extraer información clave como actividades principales y cambios legales.
- Generar bases de datos organizadas para análisis más profundos.

## Requisitos

- **Python 3.x**
- Bibliotecas necesarias:
  - `requests`
  - `PyPDF4`
  - `fitz` (PyMuPDF)
  - `lxml`
  - `datetime`

## Instalación

1. Clona este repositorio:
 ```bash
   git clone https://github.com/tu-usuario/extraccion-borme.git
 ```
3. Navega al directorio del proyecto:
```bash
cd extraccion-borme
 ```
3.Instala las dependencias:
 ```bash
pip install -r requirements.txt
 ```
## Uso
1. Configura el script:
Define las palabras clave relacionadas con el sector en la lista palabras_clave dentro del código.

2. Ejecuta el script principal:

Para extraer información del BORME de hoy:
 ```bash
python main.py
 ```
Para una fecha específica:
 ```bash
python main.py --date YYYYMMDD
 ```
3. Resultados:

Los resultados procesados estarán disponibles en un archivo JSON o CSV en el directorio de salida.

## Scripts Adicionales
frasesfrecuentesBORME.py
Este script analiza un archivo PDF del BORME para extraer frases frecuentes relacionadas con las actividades principales de las empresas.

**Uso:**
- Asegúrate de tener el archivo PDF en la ruta especificada.
- Ejecuta el script para identificar actividades principales:
 ```bash
python frasesfrecuentesBORME.py
 ```
- Resultado: un listado de actividades principales únicas extraídas del PDF.
 ```bash
test_borme.py
 ```
Automatiza la extracción de datos del BORME para el día anterior y añade un identificador único a cada apertura.

**Uso:**
- Ejecuta el script para obtener datos del día anterior:
```bash
python test_borme.py
 ```
- Resultado: una lista de aperturas con detalles organizados por provincia.

## Contribuciones
Las contribuciones son bienvenidas. Por favor, crea un fork del repositorio, realiza tus cambios y envía un pull request.

## Licencia
Este proyecto está licenciado bajo la Licencia MIT.

