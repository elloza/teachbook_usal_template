# Servidor propio

La publicación en servidor propio permite desplegar el mismo libro en un dominio institucional, por ejemplo `libro.usal.es`, usando SFTP. Esta opción es útil cuando la web debe integrarse con infraestructura de la universidad o cuando se quiere controlar el dominio final.

## Qué necesita el servidor

El servidor debe permitir acceso SFTP con usuario y contraseña, y debe tener un directorio público donde copiar la web generada. En muchos alojamientos ese directorio se llama `public_html`, aunque puede variar según la configuración institucional.

El despliegue SFTP no configura el dominio por sí solo. Hay dos piezas distintas:

- **Servidor**: recibe los archivos HTML, CSS, JavaScript, imágenes y PDF.
- **Dominio**: apunta una dirección como `libro.usal.es` al servidor correcto.

La plantilla se encarga de construir y subir los archivos. La configuración DNS y del alojamiento depende del servicio web de la institución.

## Secretos necesarios

El workflow `.github/workflows/sftp-deploy.yml` usa secretos de GitHub Actions. Deben configurarse en **Settings → Secrets and variables → Actions**:

| Secreto | Uso |
|---|---|
| `SFTP_SERVER` | Nombre del servidor o dominio de conexión SFTP. |
| `SFTP_USERNAME` | Usuario SFTP. |
| `SFTP_PASSWORD` | Contraseña SFTP. |
| `SFTP_PORT` | Puerto SFTP. Es opcional; si no existe se usa `22`. |

```{warning}
No escribas estos valores en archivos `.yml`, Markdown, notebooks ni scripts. Deben vivir únicamente como secretos del repositorio.
```

## Ejecución del deploy

El despliegue a servidor propio es manual. Para lanzarlo:

1. abre la pestaña **Actions** en GitHub;
2. selecciona **sftp-deploy-book**;
3. pulsa **Run workflow**;
4. indica el directorio remoto, por defecto `public_html`;
5. confirma la ejecución.

El workflow compila el libro completo, genera los PDF y sube `book/_build/html` al directorio remoto indicado.

## Limpieza del directorio remoto

El despliegue SFTP sincroniza el servidor con limpieza: los archivos remotos que ya no existan en el build local se eliminan. Esto evita que queden páginas antiguas publicadas por error.

Antes de desplegar, el workflow valida que el directorio remoto no sea una ruta peligrosa como `/`, `.`, `..` o una ruta absoluta. Aun así, conviene revisar con cuidado el valor de `remote_dir`, porque ese directorio quedará igual que `book/_build/html`.

## Cuándo usar servidor propio

Usa servidor propio cuando:

- necesitas publicar bajo un dominio institucional;
- el libro debe integrarse con una web existente;
- la universidad proporciona alojamiento SFTP;
- quieres separar la publicación final del dominio de GitHub.
