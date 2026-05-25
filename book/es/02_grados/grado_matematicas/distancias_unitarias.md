# Conjuntos de puntos planos con muchas distancias unitarias

Esta página explica el manuscrito *Planar Point Sets with Many Unit Distances* {cite:p}`openai2026planarunitdistances` desde el punto de vista de un curso de matemáticas. El objetivo no es reproducir cada detalle técnico de teoría de números algebraica, sino dejar clara la arquitectura de la demostración: cómo una construcción aritmética en cuerpos de números termina produciendo conjuntos finitos de puntos en el plano con muchas parejas a distancia exactamente uno.

## El problema de distancias unitarias

Sea $P \subset \mathbb{R}^2$ un conjunto finito de puntos. Definimos

$$
\nu(P)=\#\bigl\{\{p,q\}\subset P:\lVert p-q\rVert_2=1\bigr\},
$$

es decir, el número de pares no ordenados de puntos de $P$ separados por distancia euclídea uno. También se define

$$
\nu(n)=\max_{|P|=n}\nu(P),
$$

el máximo número posible de distancias unitarias entre $n$ puntos del plano.

La conjetura discutida en el manuscrito se remonta a Erdős. En una forma asintótica, esperaba que existiera una constante absoluta $C$ tal que, para $n$ suficientemente grande,

$$
\nu(n)\leq n^{1+C/\log\log n}.
$$ (eq-unit-distance-erdos)

El resultado principal del manuscrito afirma lo contrario: existe una constante fija $\delta>0$ y hay infinitos valores de $n$ para los que

$$
\nu(n)\geq n^{1+\delta}.
$$ (eq-unit-distance-main)

La desigualdad {eq}`eq-unit-distance-main` es mucho más fuerte que una mejora pequeña de una cota conocida: dice que, a lo largo de una sucesión infinita de tamaños, el número de distancias unitarias crece con un exponente estrictamente mayor que uno.

```{admonition} Lectura conceptual
:class: note
El argumento no da una receta elemental para dibujar pocos puntos a mano. Es una prueba de existencia: construye conjuntos planos a partir de torres infinitas de cuerpos de números y después los proyecta al plano.
```

## Mapa de la demostración

La demostración tiene dos mitades. La primera es geométrica: si disponemos de ciertos elementos algebraicos de norma uno, podemos convertirlos en traslaciones de longitud uno. La segunda es aritmética: construye cuerpos de números donde existen muchísimos de esos elementos.

**Tabla. Mapa lógico del argumento.**

| Bloque | Objeto principal | Qué aporta |
|---|---|---|
| Problema plano | Conjunto finito $P\subset\mathbb{R}^2$ | Queremos muchos pares a distancia $1$ |
| Geometría de números | Retícula de Minkowski en $\mathbb{C}^f$ | Permite contar puntos y traslaciones en una ventana acotada |
| Aritmética | Cuerpos $L$, $K=L(i)$ y primos que escinden | Produce muchos elementos $u$ con $u\,c(u)=1$ |
| Proyección | Una coordenada compleja $\mathbb{C}^f\to\mathbb{C}$ | Convierte traslaciones algebraicas en segmentos unitarios del plano |

## Datos admisibles

El bloque geométrico parte de un dato admisible:

- un cuerpo totalmente real $L$ de grado $f=[L:\mathbb{Q}]$;
- el cuerpo CM $K=L(i)$, con conjugación compleja relativa $c$;
- primos racionales distintos $q_1,\ldots,q_t$, todos congruentes con $1$ módulo $4$ y que escinden completamente en $L$.

Si $Q=\prod_b q_b$, la escisión completa de esos primos produce muchos pares de ideales primos conjugados en $K$:

$$
\{P_s,cP_s\},\qquad s=1,\ldots,m,\qquad m=tf.
$$

Para cada vector binario $\varepsilon\in\{0,1\}^m$ se elige un ideal

$$
A_\varepsilon=\prod_{\varepsilon_s=1}P_s
\prod_{\varepsilon_s=0}cP_s.
$$

Hay $2^m$ elecciones, pero solo $h(K)$ clases de ideales. Por el principio del palomar, muchas de esas elecciones caen en la misma clase. Comparando una de ellas con otra se obtienen elementos

$$
u_\varepsilon=\frac{\alpha_\varepsilon}{c(\alpha_\varepsilon)}
$$

que satisfacen

$$
u_\varepsilon\,c(u_\varepsilon)=1.
$$ (eq-unit-distance-norm-one)

Como $L$ es totalmente real, bajo cualquier inmersión compleja $\sigma:K\hookrightarrow \mathbb{C}$ la conjugación $c$ se ve como la conjugación compleja usual. Por tanto, de {eq}`eq-unit-distance-norm-one` se deduce

$$
|\sigma(u_\varepsilon)|=1.
$$

Esta es la idea decisiva: los elementos algebraicos construidos tienen longitud uno en todas las coordenadas complejas relevantes.

## Ventana de Minkowski y conteo

Elegimos una inmersión de Minkowski

$$
\Phi:K\longrightarrow \mathbb{C}^f,\qquad
\Phi(x)=(\sigma_1(x),\ldots,\sigma_f(x)).
$$

El ideal fraccionario $D^{-1}\mathcal{O}_K$, con $D=Q^2$, se convierte en una retícula $\Lambda\subset\mathbb{C}^f$. Los elementos $u\in U$ obtenidos antes pertenecen a esa retícula y tienen cada coordenada de módulo uno.

Ahora se toma una ventana

$$
B_R=\{z\in\mathbb{C}^f:\lVert z\rVert_\infty\leq R\},
$$

que es un producto de discos de radio $R$. Para una traslación $a+\Lambda$, se consideran los puntos

$$
X_a=(a+\Lambda)\cap B_R.
$$

El manuscrito promedia sobre el toro $\mathbb{C}^f/\Lambda$. La idea intuitiva es sencilla: si se desplaza la retícula al azar, el número medio de puntos dentro de la ventana es proporcional al volumen de $B_R$, y el número medio de pares $(x,x+u)$ con $u\in U$ depende del solapamiento de $B_R$ con $B_R-u$.

Si $\gamma=t\log 2-\log H>0$, este promedio garantiza una traslación con muchos pares:

$$
E_a\geq e^{\gamma f/2}|X_a|.
$$ (eq-unit-distance-many-pairs)

Después se proyecta $X_a\subset\mathbb{C}^f$ a la primera coordenada compleja. La proyección es inyectiva sobre la clase de retícula considerada: si dos puntos tienen la misma primera coordenada, su diferencia procede de un entero algebraico con una inmersión nula, y por tanto es cero. Así se obtiene un conjunto plano

$$
P=\pi_1(X_a)\subset\mathbb{C}\simeq \mathbb{R}^2.
$$

Cada par contado en {eq}`eq-unit-distance-many-pairs` se proyecta en un segmento de longitud uno, porque la primera coordenada de cada $u\in U$ tiene módulo uno.

## Control del tamaño de $P$

Para convertir la cota en una afirmación sobre $n=|P|$, hace falta controlar cuántos puntos caben en la ventana. El manuscrito usa un argumento de empaquetamiento: dos puntos distintos de la retícula no pueden estar demasiado cerca en todas las coordenadas a la vez, porque el producto de sus diferencias está controlado por la norma algebraica.

El resultado es una cota exponencial uniforme

$$
|P|\leq e^{Bf}
$$

para una constante $B$ fija una vez elegidos los parámetros. Combinada con la cota de pares unitarios, da

$$
\nu(P)\geq \frac{1}{2}|P|e^{\gamma f/2}.
$$

Como $|P|\leq e^{Bf}$, se puede reescribir el factor $e^{\gamma f/2}$ como una potencia positiva de $|P|$. Absorbiendo constantes para grados grandes, se obtiene

$$
\nu(P)\geq |P|^{1+\delta}
$$

para algún $\delta>0$.

## Construcción aritmética de los cuerpos

El paso aritmético produce una sucesión de cuerpos totalmente reales

$$
F=F_0\subset F_1\subset F_2\subset\cdots
$$

con grados $f_j=[F_j:\mathbb{Q}]$ que tienden a infinito. La torre se construye de forma no ramificada y con grupos de Galois de potencia de $3$. Esto es importante por dos razones:

1. al ser no ramificada, la raíz discriminante permanece controlada;
2. al trabajar con grupos pro-$3$, el conteo de generadores y relaciones puede mantener la torre infinita.

El punto de partida es un cuerpo cúbico cíclico $F$ obtenido a partir de caracteres cúbicos y cuerpos ciclotómicos. Después se eligen primos racionales $q_b$ mediante Chebotarev para que escindan completamente en todos los niveles de la torre. Para imponer esa escisión se anulan clases de Frobenius situadas en el subgrupo de Frattini. La desigualdad de Golod-Shafarevich asegura que, aunque añadamos esas relaciones, el grupo pro-$3$ resultante sigue siendo infinito.

Al final se toma

$$
K_j=F_j(i).
$$

La raíz discriminante de $K_j$ queda acotada por una constante que no depende de $j$, y una cota de Minkowski para números de clase da

$$
h(K_j)\leq H^{f_j}.
$$

El parámetro $t$ se elige del orden de $\ell^2$, mientras que $\log H$ crece solo como $O(\ell\log\ell)$. Por eso, para $\ell$ grande,

$$
t\log 2-\log H>0.
$$

Esta desigualdad es la que alimenta el parámetro $\gamma>0$ de la parte geométrica.

```{admonition} Idea para el estudiante
:class: tip
La prueba parece muy abstracta porque mezcla combinatoria geométrica, retículas, cuerpos de números y grupos pro-$p$. Una forma razonable de leerla es seguir solo la cadena de pérdidas y ganancias: se ganan $2^{tf}$ elecciones de ideales, se pierde un factor controlado por el número de clase, y después se convierte esa ganancia exponencial en muchas distancias unitarias.
```

## Contexto bibliográfico

El problema original y las cotas clásicas de distancias unitarias se apoyan en Erdős, Kővári-Sós-Turán, Spencer-Szemerédi-Trotter, Székely, Ágoston-Pálvölgyi y Guth-Katz {cite:p}`erdos1946distances,kovari1954zarankiewicz,spencer1984unitdistances,szekely1997crossing,agoston2022unitdistanceconstant,guth2015distinctdistances`. Las variantes para normas y problemas convexos relacionados aparecen en Brass, Brass-Moser-Pach, Eisenbrand-Pach-Rothvoß-Sopher, Bílka-Buchin-Fulek-Kiyomi-Okamoto-Tanigawa-Tóth, Matoušek, Alon-Bucić-Sauermann, Greilhuber-Schildkraut-Tidor, Valtr y Erdős-Fishburn {cite:p}`brass1996normedspaces,brass2005researchproblems,eisenbrand2008convexlyindependent,bilka2010convexlyindependent,matousek2011unitdistancesnorms,alon2025typicalnorms,greilhuber2025unitdistancesnorms,valtr2005strictlyconvex,erdos1997equidistance`. La parte algebraica usa herramientas estándar de torres de cuerpos de clases, teoría pro-$p$, Chebotarev, cuerpos ciclotómicos, discriminantes y números de clase {cite:p}`golod1964classfieldtower,golod1965classfieldtowers,shafarevich1963extensions,shafarevich1966extensions,neukirch1999algebraicnumbertheory,neukirch2008cohomology,koch2002galois,ribes2010profinite,dixon1999analyticpropgroups,washington1997cyclotomic,lang1994algebraicnumbertheory,davenport2000multiplicative,tschebotareff1926dichtigkeit,hajir2001globalfieldtowers,hajir2021cuttingtowers`.

````{only} html
## Referencias de esta página

```{bibliography}
:filter: key in {"openai2026planarunitdistances", "erdos1946distances", "kovari1954zarankiewicz", "spencer1984unitdistances", "szekely1997crossing", "agoston2022unitdistanceconstant", "guth2015distinctdistances", "brass1996normedspaces", "brass2005researchproblems", "eisenbrand2008convexlyindependent", "bilka2010convexlyindependent", "matousek2011unitdistancesnorms", "alon2025typicalnorms", "greilhuber2025unitdistancesnorms", "valtr2005strictlyconvex", "erdos1997equidistance", "golod1964classfieldtower", "golod1965classfieldtowers", "shafarevich1963extensions", "shafarevich1966extensions", "neukirch1999algebraicnumbertheory", "neukirch2008cohomology", "koch2002galois", "ribes2010profinite", "dixon1999analyticpropgroups", "washington1997cyclotomic", "lang1994algebraicnumbertheory", "davenport2000multiplicative", "tschebotareff1926dichtigkeit", "hajir2001globalfieldtowers", "hajir2021cuttingtowers"}
```
````
