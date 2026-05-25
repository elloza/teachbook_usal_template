# Balances y conservación

## Planteamiento del problema

En un reactor continuo de tanque agitado (CSTR) se alimenta una solución de reactivo A con concentración $C_{A0} = 2.0 \; \text{mol/L}$ y caudal volumétrico $Q = 10 \; \text{L/min}$. La reacción es:

$$A \longrightarrow B \quad \text{con} \quad r_A = -k \, C_A$$

donde $k = 0.5 \; \text{min}^{-1}$. El volumen del reactor es $V = 100 \; \text{L}$.

Determinar la concentración de salida $C_A$.

Este problema es el ejemplo mínimo de una estrategia muy general: definir una frontera de sistema, listar entradas y salidas, y aplicar conservación de materia. Es el primer paso de muchos problemas de Ingeniería Química y de modelado compartimental {cite:p}`felder2016elementary_principles`.

```{admonition} Imagen mental del reactor
:class: dropdown
Imagina el CSTR como una caja perfectamente mezclada: todo lo que sale tiene la misma concentración que hay dentro. Por eso el término de reacción usa $C_A$ del reactor y no $C_{A0}$.
```

## Ecuación del balance de masa

El balance de masa en estado estacionario para el componente A es:

$$0 = Q \, C_{A0} - Q \, C_A + r_A \, V$$

Sustituyendo la expresión de la velocidad de reacción:

$$0 = Q \, C_{A0} - Q \, C_A - k \, C_A \, V$$

## Resolución paso a paso

**Paso 1**: Agrupar términos con $C_A$.

$$Q \, C_{A0} = C_A \left( Q + k V \right)$$

**Paso 2**: Despejar $C_A$.

$$C_A = \frac{Q \, C_{A0}}{Q + k V}$$

**Paso 3**: Sustituir los valores numéricos.

$$C_A = \frac{10 \times 2.0}{10 + 0.5 \times 100} = \frac{20}{60} = 0.333 \; \text{mol/L}$$

## Conversión

La conversión del reactor se define como:

$$X = 1 - \frac{C_A}{C_{A0}} = 1 - \frac{0.333}{2.0} = 0.833 \; (83.3\%)$$

```{admonition} Verificación rápida
:class: tip
Tiempo de residencia: $\tau = V / Q = 100 / 10 = 10 \; \text{min}$. Para un reactor CSTR de primer orden: $X = k\tau / (1 + k\tau) = 5 / 6 = 0.833$. Los resultados coinciden.
```

```{admonition} Prueba con otro escenario
:class: dropdown
Si duplicas el volumen a $V=200 \; \text{L}$, el tiempo de residencia aumenta y la conversión prevista pasa a $X = 10/11 = 0.909$. El balance muestra de inmediato la relación entre tamaño de equipo y conversión.
```

## Aplicaciones transversales

- **Ingeniería Química**: diseño de reactores, cálculos estequiométricos
- **Biología y medioambiente**: modelos de biorreactores, ecosistemas y depuradoras
- **Medicina**: farmacocinética y modelos de compartimentos
- **Economía**: flujos de ingresos, gastos, deuda y acumulación
- **Logística**: entradas, salidas y almacenamiento de materiales
- **Energía**: balances de potencia, consumo y pérdidas
