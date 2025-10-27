> Los argumentos de Python son equivalentes a argumentos de opción larga (`--arg`), a menos que se especifique lo contrario. Las banderas son argumentos True/False en Python. El manual para cualquier herramienta gget se puede llamar desde la línea de comandos usando la bandera `-h` `--help`.  
# gget dataverse 🗄️
Descargar conjuntos de datos de repositorios [Dataverse](https://dataverse.harvard.edu/) usando IDs de conjuntos de datos.  
Formato de devolución: Archivos descargados al directorio especificado.

**Argumento posicional**  
`table`  
Archivo que contiene los IDs de los conjuntos de datos para descargar (formato CSV/TSV). El archivo debe contener las siguientes columnas:
- `id`: El identificador único para el archivo de datos en Dataverse
- `name`: El nombre del conjunto de datos para el archivo único
- `type`: El tipo de archivo (p. ej., csv, tsv, pkl, tab)

**Argumentos opcionales**  
`-o` `--out`    
Ruta al directorio donde se guardarán los conjuntos de datos. Por defecto: directorio de trabajo actual.

`-c` `--checksum`  
Verificar sumas de verificación MD5 de archivos descargados contra las sumas de verificación remotas. Esto garantiza la integridad del archivo comparando la suma de verificación del archivo local con la suma de verificación almacenada en Dataverse. Nota: Esto requiere llamadas adicionales a la API y puede ralentizar el proceso.

**Banderas**   
`-q` `--quiet`   
Solo línea de comandos. Evita que se muestre información de progreso.  
Python: Use `verbose=False` para evitar que se muestre información de progreso.

Banderas solo para Python:  
`verify_checksum`  
Verificar sumas de verificación MD5 de archivos descargados contra las sumas de verificación remotas. Por defecto: False.
  
  
### Ejemplos

**Descargar conjuntos de datos desde un archivo CSV**

```bash
gget dataverse datasets.csv
```

```python
import gget
gget.dataverse("datasets.csv")
```

Donde `datasets.csv` contiene:
```
id,name,type
6180617,protein_network_nodes,tab
6180618,protein_interactions,csv
```

&rarr; Descarga los archivos de datos especificados desde Dataverse al directorio actual.

<br/><br/>

**Descargar conjuntos de datos a un directorio específico**

```bash
gget dataverse datasets.tsv -o /ruta/al/directorio/descarga
```

```python
import gget
gget.dataverse("datasets.tsv", path="/ruta/al/directorio/descarga")
```

&rarr; Descarga los archivos de datos especificados desde Dataverse al directorio especificado.

<br/><br/>

**Descargar conjuntos de datos usando un DataFrame (solo Python)**

```python
import gget
import pandas as pd

# Crear DataFrame con información del conjunto de datos
df = pd.DataFrame({
    'id': ['6180617', '6180618'],
    'name': ['protein_nodes', 'protein_edges'],
    'type': ['tab', 'csv']
})

gget.dataverse(df, path="./data")
```

&rarr; Descarga los archivos de datos especificados desde Dataverse usando un DataFrame de pandas.

<br/><br/>

**Descargar conjuntos de datos con verificación de suma de verificación**

```bash
gget dataverse datasets.csv --checksum
```

```python
import gget
gget.dataverse("datasets.csv", verify_checksum=True)
```

&rarr; Descarga los archivos de datos especificados y verifica sus sumas de verificación MD5 contra las sumas de verificación remotas almacenadas en Dataverse para garantizar la integridad del archivo.

<br/><br/>

### Notas

- Los archivos se descargan con barras de progreso que muestran el estado de descarga
- Si un archivo ya existe localmente, la descarga se omite
- El módulo valida que la tabla de entrada contenga las columnas requeridas (`id`, `name`, `type`)
- Soporta archivos de entrada tanto CSV (separado por comas) como TSV (separado por tabulaciones)
- El manejo de errores proporciona mensajes claros para problemas comunes como archivos faltantes o formatos inválidos
- **Verificación de suma de verificación**: Cuando está habilitada, los archivos se verifican contra sus sumas de verificación MD5 remotas almacenadas en Dataverse. Esta característica:
  - Garantiza que los archivos descargados están completos y no corruptos
  - Funciona tanto para archivos recién descargados como para archivos locales existentes
  - Requiere llamadas adicionales a la API para recuperar metadatos
  - Muestra resultados de verificación en la salida del registro
  - Actualmente soporta solo sumas de verificación MD5
