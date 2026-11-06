# Procedencia de las copias

Estas copias se añadieron porque el enunciado pide partir de la plantilla `4GeeksAcademy/python-hello` y, a la vez, el ejercicio publica `app.py`, `test.py` y `learn.json`. No se reescribió el contenido de los archivos copiados.

## Plantilla citada por el enunciado

- Repositorio: https://github.com/4GeeksAcademy/python-hello
- Commit copiado: `142f2a913162efafce897da8bf241fe690f60395`
- Fecha de copia: 2026-11-06
- Licencia publicada en ese repositorio: ninguna (`license` es null en la API de GitHub y no hay archivo `LICENSE`)
- Carpeta: `third_party/4GeeksAcademy-python-hello/`
- Archivos, sin cambios: `main.py`, `server.py`, `learn.json`, `README.md`, `README.es.md`

Esa plantilla no trae `app.py` ni `test.py`. `server.py` importa Flask y no forma parte del programa de este ejercicio. El enunciado limita la entrada/salida y la terminal a la biblioteca estándar, así que la aplicación que se entrega es `app.py` en la raíz.

## Enunciado y pruebas del ejercicio

- Repositorio: https://github.com/breatheco-de/exercise-todo-list-cli-python
- Commit: `ee72a485a32270da30205db5020d5bc827c26104`
- `docs/enunciado/README.md` sha256 `294080fe497d8f0447932ca50ef4ca047297031f362084cea5e21d76a48acbeb`
- `docs/enunciado/README.es.md` sha256 `b8211ca8873ebed703be07a2b90632e518908b88f18f98897136e484cdcf8a11`
- `test.py` y `learn.json` en la raíz son copia byte a byte de ese commit
- El repositorio del ejercicio no publica archivo `LICENSE`

`test.py` se dejó intacto: es el contrato que debe cumplir `python3 test.py`.
