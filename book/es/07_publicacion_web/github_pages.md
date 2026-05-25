# GitHub Pages

GitHub Pages es el despliegue por defecto de esta plantilla. Es el flujo más sencillo porque no requiere servidor propio: GitHub Actions construye el libro y GitHub Pages sirve la web resultante.

## Qué hace el workflow

El archivo `.github/workflows/deploy.yml` se ejecuta al hacer `push` a `main` y también se puede lanzar manualmente desde la pestaña **Actions**. En cada ejecución:

1. prepara Python 3.12;
2. instala el entorno del proyecto con `scripts/setup_env.py`;
3. revisa codificación UTF-8 y assets estáticos;
4. instala la cadena LaTeX ligera;
5. genera los PDF de todos los idiomas;
6. compila la web HTML multi-idioma;
7. publica `book/_build/html` en GitHub Pages.

Este orden es importante: primero se generan los PDF y después se compila la web, para que los enlaces de descarga apunten siempre a archivos actualizados.

## Activación inicial

En un repositorio nuevo creado desde la plantilla, la configuración recomendada es:

1. abrir **Settings** en GitHub;
2. entrar en **Pages**;
3. elegir **Source: GitHub Actions**;
4. guardar la configuración;
5. subir el primer cambio a `main`.

Tras el primer `push`, GitHub ejecutará el workflow `deploy-book`. Si termina correctamente, la URL pública aparece en la propia página de GitHub Pages y en el resumen de la acción.

## Repositorios públicos y privados

El workflow está preparado para leer el contenido del repositorio con permisos mínimos. En repositorios privados, la publicación depende de la configuración de GitHub Pages disponible en la cuenta u organización. Si GitHub Pages no está disponible para ese repositorio, el libro se podrá compilar igualmente, pero no se publicará por esta vía.

## Cuándo usar GitHub Pages

Usa GitHub Pages cuando:

- quieres publicar rápido sin pedir un servidor;
- el libro puede vivir bajo una URL de GitHub;
- quieres que cada cambio en `main` actualice la web automáticamente;
- estás usando la plantilla por primera vez y necesitas el camino con menos configuración.
