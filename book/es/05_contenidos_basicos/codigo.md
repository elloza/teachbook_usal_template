(codigo)=
# Bloques de código

Los bloques de código son fundamentales en ciencias: muestran fórmulas computacionales, scripts de análisis y procedimientos paso a paso.

## Código con resaltado de sintaxis

Añade el lenguaje después de las comillas invertidas:

````md
```python
import numpy as np

datos = np.array([3.2, 4.1, 3.8, 4.5, 3.9])
media = np.mean(datos)
print(f"Media: {media:.2f}")
```
````

Resultado:

```python
import numpy as np

datos = np.array([3.2, 4.1, 3.8, 4.5, 3.9])
media = np.mean(datos)
print(f"Media: {media:.2f}")
```

## Números de línea

Usa la directiva `{code-block}` con `:linenos:` para mostrar números. Esta opción no funciona dentro de un bloque normal escrito como ```` ```python ````; en ese caso se interpreta como una línea más del código.

````md
```{code-block} python
:linenos:

def calcular_desviacion(datos):
    n = len(datos)
    media = sum(datos) / n
    varianza = sum((x - media) ** 2 for x in datos) / n
    return varianza ** 0.5
```
````

Resultado:

```{code-block} python
:linenos:

def calcular_desviacion(datos):
    n = len(datos)
    media = sum(datos) / n
    varianza = sum((x - media) ** 2 for x in datos) / n
    return varianza ** 0.5
```

## Resaltar líneas específicas

Usa `:emphasize-lines:` dentro de `{code-block}` para destacar líneas concretas:

````md
```{code-block} python
:emphasize-lines: 3

def leer_datos(archivo):
    with open(archivo, 'r') as f:
        lineas = f.readlines()  # Esta linea se resaltara
    return [float(l.strip()) for l in lineas]
```
````

Resultado:

```{code-block} python
:emphasize-lines: 3

def leer_datos(archivo):
    with open(archivo, 'r') as f:
        lineas = f.readlines()
    return [float(l.strip()) for l in lineas]
```

## Otros lenguajes

El resaltado funciona con muchos lenguajes:

```bash
# Ejemplo en Bash
curl -O https://ejemplo.com/datos.csv
head -5 datos.csv
```

```sql
-- Ejemplo en SQL
SELECT nombre, nota
FROM estudiantes
WHERE nota >= 5.0
ORDER BY nota DESC;
```

## Lenguajes más usados en ciencias


La tabla siguiente resume los elementos principales de esta sección.

**Tabla. Lenguajes más usados en ciencias.**

| Lenguaje | Cuándo usarlo |
|----------|--------------|
| `python` | Análisis de datos, cálculo numérico |
| `r` | Estadística, bioestadística |
| `matlab` | Ingeniería, procesamiento de señales |
| `sql` | Consultas a bases de datos |
| `bash` | Automatización de tareas |
| `json` / `yaml` | Archivos de configuración |

```{tip}
Esta plantilla incluye `sphinx-copybutton`: aparece un botón **Copiar** en la esquina de cada bloque de código. El lector puede copiar el código con un clic.
```
