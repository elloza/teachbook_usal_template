---
name: teachbook-generate-quiz
description: >
  Crea páginas de preguntas/cuestionarios para el libro con respuestas ocultas.
  Usa admonitions dropdown y HTML details/summary. No es auto-evaluado, es herramienta de estudio.
  Trigger phrases: "preguntas", "quiz", "cuestionario", "test", "examen", "pregunta",
  "preguntas de repaso", "autoevaluación", "ejercicios de comprobación".
---

# Skill: Generar Cuestionarios

## Importante

Estos cuestionarios son **herramientas de estudio**, no un sistema LMS. No hay auto-evaluación ni puntuación automática. El estudiante piensa la respuesta y la compara.

## Patrón 1: Admonition con dropdown

Usa la directiva `{admonition}` con `:class: dropdown`. Funciona en HTML (colapsable) y PDF (se muestra expandido).

````markdown
```{admonition} Pregunta 1: ¿Cuál es la velocidad de la luz?
:class: dropdown

La velocidad de la luz en el vacío es aproximadamente $3 \times 10^8$ m/s.

**Explicación:** La constante $c$ es una de las constantes fundamentales de la física y define el límite de velocidad en el universo.
```
````

### Plantilla de cuestionario completo (Patrón 1)

````markdown
# Cuestionario: Tema X

Responde mentalmente antes de desplegar cada respuesta.

```{admonition} Pregunta 1: ¿Qué es la fotosíntesis?
:class: dropdown

Es el proceso por el cual los organismos autótrofos convierten la energía luminosa en energía química.

**Explicación:** Ocurre principalmente en los cloroplastos y produce glucosa y oxígeno a partir de CO₂ y agua.
```

```{admonition} Pregunta 2: ¿Cuál es la ecuación de la fotosíntesis?
:class: dropdown

$$6CO_2 + 6H_2O + \text{luz} \rightarrow C_6H_{12}O_6 + 6O_2$$

**Explicación:** Seis moléculas de dióxido de carbono y seis de agua, con energía lumínica, producen una molécula de glucosa y seis de oxígeno.
```
````

## Patrón 2: HTML details/summary

Usa HTML directo con `{raw}`. Más flexible para estilos personalizados.

````markdown
```{raw} html
<details>
<summary><strong>Pregunta 1: ¿Cuál es la unidad del SI para la fuerza?</strong></summary>
<p><strong>Respuesta:</strong> Newton (N).</p>
<p><em>Explicación:</em> 1 N = 1 kg·m/s². Se define como la fuerza necesaria para acelerar 1 kg a 1 m/s².</p>
</details>
```

```{raw} latex
\textbf{Pregunta 1: ¿Cuál es la unidad del SI para la fuerza?}

\textbf{Respuesta:} Newton (N).

\textit{Explicación:} 1 N = 1 kg$\cdot$m/s$^2$.
```
````

## Patrón 3: Elección múltiple

Combina pregunta con opciones y respuesta oculta:

````markdown
```{admonition} Pregunta 1: ¿Cuál de las siguientes NO es una fuerza fundamental?
:class: dropdown

**Opciones:**
- a) Gravedad
- b) Electromagnetismo
- c) Fricción
- d) Fuerza nuclear fuerte

**Respuesta correcta:** c) Fricción

**Explicación:** La fricción es una fuerza derivada del electromagnetismo a nivel microscópico. Las cuatro fuerzas fundamentales son: gravedad, electromagnetismo, nuclear fuerte y nuclear débil.
```
````

### Plantilla de cuestionario múltiple completo

````markdown
# Test: Conceptos básicos

Elige la respuesta correcta y luego despliega para comprobar.

```{admonition} Pregunta 1
:class: dropdown

**¿Cuál es la fórmula de la ley de Ohm?**

- a) $V = IR$
- b) $F = ma$
- c) $E = mc^2$

**Respuesta:** a) $V = IR$

**Explicación:** La ley de Ohm relaciona voltaje (V), corriente (I) y resistencia (R).
```

```{admonition} Pregunta 2
:class: dropdown

**¿Qué partícula tiene carga negativa?**

- a) Protón
- b) Neutrón
- c) Electrón

**Respuesta:** c) Electrón

**Explicación:** El electrón tiene carga $-1.6 \times 10^{-19}$ C. El protón tiene carga positiva y el neutrón es neutro.
```
````

## Reglas

| Regla | Detalle |
|---|---|
| Cantidad | Entre **5 y 10 preguntas** por página de cuestionario. |
| Respuesta | Siempre incluir la respuesta correcta (nunca dejar sin responder). |
| Explicación | Añadir una explicación breve de 1-3 líneas tras cada respuesta. |
| Formato | Funciona tanto en `.md` como en `.ipynb`. |
| Multi-idioma | Crear el cuestionario en TODOS los idiomas. |
| No es LMS | Aclarar que es herramienta de estudio, no evaluación automática. |

## Flujo de trabajo

1. Preguntar el tema y el número de preguntas deseadas.
2. Elegir el patrón (dropdown admonition, HTML details, o múltiple).
3. Generar las preguntas con respuestas y explicaciones.
4. Crear el archivo en todos los idiomas.
5. Añadir al `_toc_<lang>.yml` correspondiente.
