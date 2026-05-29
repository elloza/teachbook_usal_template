# 4. Mi primer libro desde cero

Esta página muestra un primer recorrido completo para crear un libro nuevo desde esta plantilla: crear el repositorio, abrirlo en el ordenador, pedir ayuda al agente, ver una previsualización local, generar PDF y publicar la web.

La idea no es que aprendas Git, Python, LaTeX o GitHub en profundidad antes de empezar. La idea es que entiendas qué está pasando en cada pantalla, qué le puedes pedir al agente y dónde mirar si necesitas comprobar que todo ha salido bien.

```{note}
Los GIFs de esta página están acelerados para que el proceso se vea de forma compacta. La instalación inicial del entorno y la generación del PDF pueden tardar bastante más, sobre todo la primera vez que se instala el motor de LaTeX.
```

## Paso 0. Preparar los requisitos básicos

Antes de tocar la plantilla conviene comprobar que el ordenador tiene lo mínimo para trabajar: una cuenta de GitHub, Python instalado, Git disponible y un editor con agente de IA, como Antigravity o VS Code. Como muestra la {numref}`fig-primer-libro-04-00-es`, este paso consiste en dejar listo el punto de partida antes de crear el repositorio.

GitHub será el sitio donde se guardará el libro en internet. Python permitirá ejecutar los scripts de la plantilla. Git es la herramienta que guarda el historial de cambios y permite subirlos a GitHub. Antigravity o VS Code serán el lugar de trabajo: ahí abriremos la carpeta del libro, pediremos tareas al agente y revisaremos los archivos.

También es importante configurar Git para su primer uso. Si nunca lo has hecho en ese ordenador, abre una terminal y ejecuta:

```powershell
git config --global user.name "Tu nombre"
git config --global user.email "tu.correo@ejemplo.es"
```

Estos datos son los que aparecerán en los commits. Un commit es una "foto" del estado del proyecto en un momento concreto. No tienes que escribir aquí una contraseña ni un token: solo tu nombre y tu correo. El correo debería estar asociado a tu cuenta de GitHub si quieres que GitHub reconozca que esos cambios son tuyos.

Si no sabes si Git ya está configurado, puedes comprobarlo con:

```powershell
git config --global user.name
git config --global user.email
```

Si esos comandos devuelven tu nombre y tu correo, puedes continuar. Si no devuelven nada, configura Git con los comandos anteriores. Este paso solo suele hacerse una vez por ordenador.

```{figure} ../../_static/tutorial_gifs/first_book/04_00_requirements.gif
---
name: fig-primer-libro-04-00-es
alt: GIF con los requisitos básicos para crear el primer libro desde cero
width: 95%
align: center
---
Requisitos básicos: GitHub, Python, Git configurado y un editor con agente de IA.
```

## Paso 1. Crear un repositorio desde la plantilla

El siguiente paso es abrir la URL de la plantilla en GitHub y usar el botón **Use this template** para crear un repositorio propio. En este primer recorrido lo haremos **público**, como se ve en la {numref}`fig-primer-libro-04-01-es`, porque simplifica la publicación inicial en GitHub Pages. Más adelante se puede estudiar el caso de repositorios privados.

Un repositorio es la carpeta del proyecto dentro de GitHub. Al usar el botón de plantilla, GitHub no modifica este repositorio original: crea una copia independiente en tu cuenta. Esa copia será tu libro. Puedes cambiar el título, borrar ejemplos, añadir capítulos y publicar la web sin afectar a nadie más.

Cuando GitHub te pida los datos del repositorio, fíjate especialmente en tres campos:

- **Owner**: la cuenta u organización donde se creará el libro.
- **Repository name**: el nombre técnico del repositorio. Evita espacios y caracteres raros; por ejemplo, `mi-primer-libro`.
- **Public**: en este primer ejercicio conviene marcarlo como público para que GitHub Pages sea más sencillo de activar.

Después de crear el repositorio, GitHub te llevará a una página cuya dirección tendrá una forma parecida a:

```text
https://github.com/tu-usuario/mi-primer-libro
```

Guarda mentalmente esa página: es la página principal de tu proyecto en GitHub. Desde ahí podrás copiar la URL para clonar, entrar en **Settings**, ver las **Actions** y comprobar si la web se ha publicado correctamente.

```{figure} ../../_static/tutorial_gifs/first_book/04_01_use_template.gif
---
name: fig-primer-libro-04-01-es
alt: GIF mostrando la creación de un repositorio público desde el botón de template
width: 95%
align: center
---
Creación de un repositorio público nuevo usando el botón de plantilla de GitHub.
```

## Paso 2. Activar GitHub Actions y GitHub Pages

Una vez creado el repositorio, hay que permitir que GitHub ejecute los workflows del proyecto y publique la web. La {numref}`fig-primer-libro-04-02-es` muestra la configuración de **GitHub Pages** con la fuente **GitHub Actions**.

GitHub Actions es el sistema de automatización de GitHub. En esta plantilla se encarga de hacer en la nube lo que tú podrías hacer en tu ordenador: instalar el entorno, comprobar el proyecto, generar los PDF, compilar la web y publicarla. GitHub Pages es el servicio que toma esa web compilada y la pone disponible en una URL pública.

Para configurarlo, entra en tu repositorio de GitHub y ve a:

```text
Settings -> Pages -> Build and deployment -> Source -> GitHub Actions
```

Si es el primer uso de Actions en esa cuenta o repositorio, GitHub puede pedir una confirmación adicional para habilitar workflows. Ese detalle puede no verse en el GIF, pero hay que aceptarlo para que el libro pueda compilarse y publicarse automáticamente.

La URL pública de la web no siempre aparece inmediatamente. Normalmente aparece después del primer despliegue correcto. Hay dos sitios donde puedes encontrarla:

- En **Settings -> Pages**, GitHub suele mostrar un enlace a la web publicada cuando ya existe un despliegue correcto.
- En la pestaña **Actions**, abre la ejecución del workflow de despliegue y busca el resumen del deploy. Cuando todo está en verde, suele haber un enlace al sitio publicado.

La URL típica de GitHub Pages para un repositorio de proyecto tiene esta forma:

```text
https://tu-usuario.github.io/mi-primer-libro/
```

Si el repositorio pertenece a una organización, la primera parte cambia por el nombre de la organización. Si más adelante usas un dominio propio, como `libro.usal.es`, esa URL puede ser distinta.

```{figure} ../../_static/tutorial_gifs/first_book/04_02_enable_pages_actions.gif
---
name: fig-primer-libro-04-02-es
alt: GIF mostrando la activación de GitHub Pages con GitHub Actions
width: 95%
align: center
---
Activación de GitHub Pages con GitHub Actions como fuente de publicación.
```

## Paso 3. Clonar el repositorio en Antigravity

Con el repositorio creado en GitHub, copia su URL y clónalo desde Antigravity. La {numref}`fig-primer-libro-04-03-es` muestra el flujo general: abrir el editor, elegir la opción de clonar y pegar la URL del repositorio.

Clonar significa descargar una copia completa del repositorio en tu ordenador. No es una simple descarga de un ZIP: al clonar, la carpeta local queda conectada con GitHub. Eso permite trabajar en local y, cuando estés conforme, subir los cambios con `commit` y `push`.

Para encontrar la URL que necesitas, vuelve a la página principal del repositorio en GitHub y pulsa el botón verde **Code**. En la pestaña **HTTPS** verás una dirección parecida a:

```text
https://github.com/tu-usuario/mi-primer-libro.git
```

Copia esa URL y pégala en la opción de clonar de Antigravity. El editor te preguntará en qué carpeta del ordenador quieres guardar el proyecto. Elige una carpeta fácil de encontrar, por ejemplo `Documentos`, `Desktop` o una carpeta dedicada a tus cursos.

En este punto GitHub puede pedir autenticación. Es normal: el editor necesita permiso para descargar el repositorio y, más adelante, para subir los cambios. Si aparece una ventana del navegador o una pantalla de inicio de sesión de GitHub, sigue el flujo de autenticación. No pegues contraseñas dentro de archivos del proyecto.

```{figure} ../../_static/tutorial_gifs/first_book/04_03_clone_repository.gif
---
name: fig-primer-libro-04-03-es
alt: GIF mostrando cómo clonar el repositorio en Antigravity usando la URL de GitHub
width: 95%
align: center
---
Clonado del repositorio desde GitHub en Antigravity.
```

## Paso 4. Pedir al agente que configure el entorno

Al abrir el proyecto por primera vez, pide al agente que prepare el entorno. Conviene usar un modelo de coste bajo, por ejemplo **Gemini 3.1 Pro (Low)** si está disponible, porque esta tarea es bastante mecánica y puede requerir varias interacciones.

Un mensaje útil sería:

```text
Configura este proyecto por primera vez siguiendo las instrucciones del repositorio.
Usa el entorno .venv y continúa con las instalaciones necesarias.
```

El entorno `.venv` es una carpeta local donde se instalan las herramientas de Python que necesita este libro. Sirve para no mezclar las dependencias del proyecto con otros programas del ordenador. Para una persona no informática, lo importante es esto: si el agente usa `.venv`, el proyecto queda más ordenado y es más fácil repetir la instalación en otro equipo.

Como muestra la {numref}`fig-primer-libro-04-04-es`, el agente irá ejecutando comandos y puede preguntar varias veces si puede continuar. En este primer arranque normalmente hay que responder que sí. Puede pedir permiso para instalar `uv`, crear `.venv`, instalar dependencias, preparar LaTeX o sincronizar skills. Esas preguntas son esperables.

Este paso dura más que el GIF. Depende de la conexión, del ordenador y de si Python, Git o `uv` ya estaban instalados. Durante la instalación evita cerrar el editor o apagar el ordenador. Si parece que no ocurre nada durante unos minutos, revisa si el agente está esperando una confirmación en la terminal.

Cuando termine, lo normal es que el proyecto tenga una carpeta `.venv` y que el agente pueda ejecutar los scripts de comprobación. Si algo falla, no intentes arreglarlo a mano copiando comandos al azar: pide al agente que lea el error, revise `AGENTS.md` y vuelva a ejecutar el setup de forma limpia.

```{figure} ../../_static/tutorial_gifs/first_book/04_04_setup_environment.gif
---
name: fig-primer-libro-04-04-es
alt: GIF mostrando la configuración inicial del entorno con ayuda del agente
width: 95%
align: center
---
Configuración inicial del entorno del proyecto mediante el agente.
```

## Paso 5. Hacer una primera edición con el agente

Cuando el entorno ya está listo, podemos pedir un primer cambio real. En el ejemplo de la {numref}`fig-primer-libro-04-05-es`, se le pide al agente que oculte los capítulos actuales de la plantilla y deje solo un capítulo de muestra sobre el **Teorema del Límite Central**, escrito con LaTeX y MyST.

Este primer cambio sirve para aprender la dinámica de trabajo. No hace falta empezar escribiendo todo el libro. Es mejor pedir una modificación pequeña, comprobar que aparece en la web local y después publicar. Así se entiende el ciclo completo antes de invertir muchas horas en contenido.

La petición debe indicar claramente que el cambio tiene que hacerse en ambos idiomas:

```text
Oculta temporalmente los capítulos actuales de la plantilla y deja solo un capítulo
de muestra que explique el Teorema del Límite Central con LaTeX y MyST.
Hazlo en español e inglés y mantén sincronizados los TOC.
```

Hay dos ideas importantes en esa petición. La primera es **ocultar**, no borrar. El agente puede quitar secciones del menú comentando o ajustando los TOC, pero conviene conservar los archivos de ejemplo porque más adelante pueden servir como referencia. La segunda es **en español e inglés**. Esta plantilla está pensada para varios idiomas, así que cada cambio visible debe tener su equivalente en los idiomas configurados.

También conviene pedir al agente que valide el resultado:

```text
Cuando termines, revisa la codificación, la estructura multi-idioma y compila la web.
```

Si el agente modifica una página en español pero olvida la inglesa, el libro puede quedar incoherente. Por eso las comprobaciones automáticas son parte del flujo normal, no un extra para usuarios avanzados.

```{figure} ../../_static/tutorial_gifs/first_book/04_05_first_agent_edit.gif
---
name: fig-primer-libro-04-05-es
alt: GIF mostrando una primera edición con el agente para dejar un capítulo de muestra
width: 95%
align: center
---
Primera edición asistida: ocultar contenido de ejemplo y dejar un capítulo mínimo en ambos idiomas.
```

## Paso 6. Ver la previsualización local

Después de editar, pide al agente que levante una previsualización local. La {numref}`fig-primer-libro-04-06-es` muestra cómo el agente monta un servidor en el ordenador y después informa de la URL donde se puede abrir el libro.

Puedes pedirlo de forma sencilla:

```text
Quiero ver una preview local del libro. Levanta el servidor y dime la URL exacta.
```

La URL suele ser local, por ejemplo `http://127.0.0.1:8000` o `http://localhost:8000`. Eso significa que la web todavía no está publicada en internet: se está sirviendo desde tu propio PC para revisar los cambios antes de subirlos. Esa dirección solo funciona en tu ordenador mientras el servidor local esté abierto.

Es importante distinguir estas dos URLs:

- `http://localhost:8000` o `http://127.0.0.1:8000`: vista previa local en tu PC.
- `https://tu-usuario.github.io/mi-primer-libro/`: web publicada en GitHub Pages.

Si el puerto `8000` está ocupado, el agente puede usar otro, como `8001` o `8080`. No pasa nada: abre exactamente la URL que te indique. Si ves una versión antigua, pide al agente que recompilie el libro y reinicie la preview. En esta plantilla la preview debe construirse con el mismo flujo que producción, para evitar revisar una web desactualizada.

```{figure} ../../_static/tutorial_gifs/first_book/04_06_local_preview.gif
---
name: fig-primer-libro-04-06-es
alt: GIF mostrando cómo lanzar la previsualización local y abrir el libro en el navegador
width: 95%
align: center
---
Previsualización local del libro mediante un servidor ejecutado en el propio ordenador.
```

## Paso 7. Generar los PDF

Cuando la web local se ve bien, pide al agente que genere los PDF del libro. En la {numref}`fig-primer-libro-04-07-es` se ve el flujo resumido, pero este proceso puede tardar más que el GIF, especialmente la primera vez.

Puedes pedirlo así:

```text
Genera los PDF del libro en todos los idiomas y comprueba que se han creado bien.
```

La plantilla genera normalmente un PDF por idioma y los deja en `book/_static/`, por ejemplo:

```text
book/_static/ElaboracionDeLibrosElectronicosMedianteCodigoYAsistentesDeInteligenciaArtificial.pdf
book/_static/CreatingElectronicBooksWithCodeAndArtificialIntelligenceAssistants.pdf
```

El motivo de la espera inicial es que el proyecto necesita un motor de LaTeX para convertir el libro a PDF. LaTeX es el sistema que produce documentos académicos con buena tipografía, ecuaciones, índices y referencias. No hace falta aprender LaTeX para usar la plantilla, pero sí hay que dejar instalado el motor que compila el documento.

Durante la primera generación puede parecer que se están instalando muchas cosas. Es normal. En ejecuciones posteriores suele ser más rápido porque la instalación ya está preparada. Si falla, lo importante es guardar el mensaje de error y pedir al agente que lo revise. No conviene borrar carpetas o reinstalar herramientas a mano sin diagnóstico.

```{figure} ../../_static/tutorial_gifs/first_book/04_07_generate_pdfs.gif
---
name: fig-primer-libro-04-07-es
alt: GIF mostrando la generación de PDF y la instalación inicial de LaTeX
width: 95%
align: center
---
Generación de los PDF del libro, con instalación inicial de LaTeX si es necesaria.
```

## Paso 8. Publicar los cambios

Por último, pide al agente que publique los cambios. Como muestra la {numref}`fig-primer-libro-04-08-es`, publicar en esta plantilla significa hacer un ciclo completo de Git: añadir archivos, crear un commit y hacer `push` a GitHub.

Una petición adecuada sería:

```text
Guarda los cambios, haz commit, haz push y comprueba que el despliegue de GitHub Pages funciona.
```

El commit guarda una versión concreta del proyecto con un mensaje descriptivo. El push sube esa versión a GitHub. Al llegar a GitHub, se dispara el workflow de despliegue. Ese workflow compila el libro en la nube, regenera los PDF y publica la web.

Después del push, entra en tu repositorio de GitHub y abre la pestaña **Actions**. Allí verás una ejecución nueva del workflow. Mientras está en marcha puede aparecer en amarillo o con un icono de progreso. Cuando termina correctamente, aparece en verde. Si aparece en rojo, el despliegue ha fallado y hay que abrir esa ejecución para leer el error.

Para encontrar la URL de la web publicada, revisa estos sitios:

- **Settings -> Pages**: después de un despliegue correcto, GitHub suele mostrar aquí la URL pública del sitio.
- **Actions -> ejecución del deploy**: la ejecución que ha publicado la web puede incluir un enlace al despliegue.
- **Patrón habitual de URL**: si no usas dominio propio, será parecido a `https://tu-usuario.github.io/mi-primer-libro/`.

Ten en cuenta que la web publicada no siempre se actualiza en el navegador en el mismo segundo. Si el workflow está en verde pero sigues viendo contenido antiguo, espera un poco y recarga la página. También puedes abrir una ventana privada del navegador para evitar caché.

Como en esta plantilla el workflow genera primero los PDF y después la web, los botones o enlaces de descarga del sitio deberían apuntar a los PDF actualizados. Ese es el motivo por el que no conviene subir solo HTML manualmente: el despliegue completo mantiene sincronizados web y documentos imprimibles.

```{figure} ../../_static/tutorial_gifs/first_book/04_08_publish_changes.gif
---
name: fig-primer-libro-04-08-es
alt: GIF mostrando la publicación de cambios mediante commit, push y GitHub Actions
width: 95%
align: center
---
Publicación del libro mediante commit, push y despliegue automático con GitHub Actions.
```

Al terminar este recorrido ya tienes el ciclo básico completo: crear el repositorio, editar con ayuda del agente, revisar en local, generar PDF y publicar la web. A partir de ahí, el trabajo diario consiste en repetir el mismo patrón con cambios más pequeños: escribir, previsualizar, validar y publicar.
