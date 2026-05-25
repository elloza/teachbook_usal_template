---
name: teachbook-generate-thebe-binder-page
description: >
  Crea páginas o notebooks con código Python ejecutable mediante Thebe conectado a Binder.
  El estudiante puede editar y ejecutar código desde la web usando un kernel remoto.
  Trigger phrases: "thebe", "binder", "código live", "live code", "ejecutar en navegador",
  "código interactivo".
---

# Skill: Generar página con Thebe + Binder

## Objetivo

Crear una página o notebook donde el estudiante pueda ejecutar Python desde la versión web del libro usando **Thebe** y un **kernel remoto en Binder**.

## Regla importante

En este proyecto, **Thebe usa Binder**, NO Pyodide.

Por tanto:

- depende de conexión a internet
- puede tardar en arrancar la primera vez
- levanta un entorno remoto

## Requisitos

- `sphinx-thebe` instalado
- Config `_config_*.yml` con `sphinx_thebe` en `extra_extensions`
- `thebe_config` con repositorio Binder configurado

## Estructura recomendada

```md
# Título de la página

Breve introducción.

```{admonition} Activar código interactivo
:class: tip

Pulsa el botón "Live Code" para conectar con Binder y activar las celdas interactivas.
La primera carga puede tardar unos segundos.
```

```{thebe-button}
```

```{code-block} python
:class: thebe

import numpy as np
print(np.mean([1, 2, 3, 4]))
```
```

## Reglas

1. Siempre incluir `{thebe-button}`.
2. Usar `code-block` con `:class: thebe`.
3. Priorizar ejemplos simples y robustos: `numpy`, `matplotlib`, `math`, `random`.
4. Evitar depender de paquetes raros o entornos pesados.
5. Añadir siempre texto suficiente para que la página tenga sentido también en PDF.

## Compatibilidad PDF

Thebe es **solo HTML**.

En PDF:
- el botón no aparece
- el código se verá como bloque estático
- no hay ejecución

## Nota didáctica

No prometas "ejecución en el navegador sin backend". En este proyecto, la ejecución real se hace a través de Binder.
