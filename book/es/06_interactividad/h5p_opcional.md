# H5P (Opcional)

**H5P** es una plataforma de contenido interactivo que ofrece cuestionarios, actividades de arrastrar y soltar, interacciones de video y mucho más.

```{warning}
H5P es **opcional** y **no es una dependencia** de esta plantilla. Requiere un servidor externo para alojar el contenido (H5P.com, Moodle, WordPress con plugin H5P, etc.). No es autocontenido.
```

## ¿Qué ofrece H5P?


La tabla siguiente resume los elementos principales de esta sección.

**Tabla. ¿Qué ofrece H5P?.**

| Tipo de actividad | Descripción |
|-------------------|-------------|
| Cuestionarios | Preguntas de elección múltiple, rellenar huecos |
| Drag & Drop | Arrastrar elementos a zonas correctas |
| Video interactivo | Añadir pausas con preguntas sobre un video |
| Presentación interactiva | Slides con preguntas integradas |
| Resumen | Texto con preguntas intercaladas |

## Cómo incrustar H5P en tu TeachBook

Crea tu contenido en la plataforma H5P y usa un `iframe` para mostrarlo:

````md
```{raw} html
<iframe src="https://H5P_URL_AQUI" width="800" height="600" frameborder="0" allowfullscreen="allowfullscreen" style="border: 1px solid #e5e7eb; border-radius: 8px;"></iframe>
```

```{raw} latex
\textbf{Actividad interactiva H5P:} Disponible en la versión web del libro.
Enlace: \url{https://H5P_URL_AQUI}
```
````

## Plataformas compatibles

- **H5P.com**: Servicio oficial (de pago para uso avanzado).
- **Moodle**: Plugin gratuito, ideal si tu universidad ya usa Moodle.
- **WordPress**: Plugin gratuito H5P.
- **Lumi**: Aplicación de escritorio para crear H5P sin servidor.

```{admonition} Alternativa recomendada
:class: tip
Si no necesitas la complejidad de H5P, los **ejercicios con solución** (usando `{admonition}` con `dropdown`) cubren la mayoría de necesidades de evaluación y funcionan tanto en HTML como en PDF, sin servidor externo.
```
