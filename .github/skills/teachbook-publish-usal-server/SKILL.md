---
name: teachbook-publish-usal-server
description: >
  Publica el TeachBook desde un ordenador local al servidor USAL por SFTP usando
  un .env privado y una conexion eduVPN. No sirve para GitHub Pages ni para
  modificar workflows de GitHub Actions.
  Trigger phrases: "publicar en servidor USAL", "publicar por SFTP", "eduVPN",
  "deploy local", "subir al servidor USAL", "servidor propio USAL",
  "deploy_sftp_from_env", "SFTP local".
---

# Skill: Publicar en Servidor USAL por SFTP

## Cuándo usar esta skill

- Cuando el docente quiere publicar el TeachBook en un servidor USAL propio desde su ordenador.
- Cuando la publicación requiere estar conectado a eduVPN y usar credenciales SFTP privadas.
- Cuando se quiere probar el plan o hacer un dry-run sin subir archivos.

No usar esta skill para GitHub Pages: en ese caso se usa `teachbook-git-publish`.

## Reglas de seguridad

- No hacer `commit`, `push` ni modificar workflows.
- No ejecutar despliegue real salvo petición explícita del usuario.
- No imprimir ni pegar el contenido completo de `.env`.
- No mostrar `SFTP_PASSWORD`, tokens, claves VPN, `PrivateKey` ni `PresharedKey`.
- Usar siempre el Python de `.venv`; no crear entornos alternativos.
- El ordenador debe estar conectado a eduVPN antes de comprobar o publicar.

## Preparar credenciales locales

1. Copiar `.env.example` como `.env`.
2. Rellenar en `.env`:
   - `SFTP_SERVER`
   - `SFTP_PORT`
   - `SFTP_USERNAME`
   - `SFTP_PASSWORD`
   - `SFTP_REMOTE_DIR`
3. Confirmar que `.env` sigue ignorado por Git.

`SFTP_REMOTE_DIR` debe ser una ruta relativa segura ya existente en el servidor, por ejemplo `public_html`.

## Comandos

Usar PowerShell en Windows:

```powershell
.venv\Scripts\python.exe scripts\local\deploy_sftp_from_env.py --plan-only
.venv\Scripts\python.exe scripts\local\deploy_sftp_from_env.py --dry-run
.venv\Scripts\python.exe scripts\local\deploy_sftp_from_env.py --apply
```

Usar terminal en macOS, Linux o WSL:

```bash
.venv/bin/python scripts/local/deploy_sftp_from_env.py --plan-only
.venv/bin/python scripts/local/deploy_sftp_from_env.py --dry-run
.venv/bin/python scripts/local/deploy_sftp_from_env.py --apply
```

`--plan-only` valida el `.env` y muestra un plan seguro sin conectar al servidor, construir ni subir. El modo por defecto es dry-run: comprueba eduVPN/SFTP, valida el directorio remoto, prepara el build y no sube archivos. `--apply` es el único modo que publica.

Para usar un `.env` en otra ubicación:

```bash
.venv/bin/python scripts/local/deploy_sftp_from_env.py --env-file /ruta/privada/teachbook.env --dry-run
```

## Qué hace el script

1. Verifica que se ejecuta con el Python de `.venv` y Python 3.12.
2. Lee el `.env` privado sin imprimir secretos.
3. Comprueba el puerto SFTP; si falla, normalmente falta eduVPN o hay un dato incorrecto.
4. Abre una sesión SFTP y exige que `SFTP_REMOTE_DIR` exista.
5. Ejecuta validaciones UTF-8 y assets.
6. Genera PDFs con el flujo local del proyecto, salvo que se use `--skip-pdf`.
7. Compila HTML en `book/_build/html/`.
8. Si se usa `--apply`, despliega con `lftp mirror -R --delete --parallel=4` cuando `lftp` está disponible.

Si `lftp` no está disponible, el script usa un fallback Python con `paramiko`. Si falta `paramiko`, instalarlo solo dentro de `.venv`:

```bash
.venv/bin/python -m pip install paramiko
```

## Comprobación antes de publicar

Antes de `--apply`, ejecutar siempre:

```bash
.venv/bin/python scripts/local/deploy_sftp_from_env.py --dry-run
```

Si el dry-run termina bien, el despliegue real es el mismo comando cambiando `--dry-run` por `--apply`.
