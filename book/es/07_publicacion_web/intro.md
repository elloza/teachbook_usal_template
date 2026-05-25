# Publicación Web

La publicación web convierte el libro generado en un sitio estático que se puede consultar desde cualquier navegador. En esta plantilla hay dos rutas pensadas para necesidades distintas:

- **GitHub Pages**: es la opción recomendada para empezar. GitHub construye el libro, genera los PDF y publica la web automáticamente al subir cambios a la rama principal.
- **Servidor propio**: es la opción adecuada cuando el libro debe vivir en un dominio institucional, por ejemplo `libro.usal.es`, o en un alojamiento gestionado por la universidad.

Las dos rutas usan el mismo resultado técnico: la carpeta `book/_build/html`, generada por `scripts/build_book.py`. La diferencia está en dónde se copia esa carpeta y quién sirve los archivos al público.

```{important}
Nunca se deben escribir usuarios, contraseñas ni datos de acceso dentro del repositorio. Los despliegues a servidores propios deben usar secretos de GitHub Actions.
```

En las secciones siguientes se resumen los dos flujos soportados por la plantilla.
