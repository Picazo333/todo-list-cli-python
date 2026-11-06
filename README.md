# Lista de tareas en la terminal

Programa de línea de comandos para anotar tareas del día, verlas numeradas, borrar una por su posición y guardarlas en `todos.csv`. Al abrir otra vez la terminal, la opción 5 vuelve a cargar ese archivo.

El menú y los textos de las opciones 1 a 6 salen del starter del ejercicio. Las respuestas de ayuda, de lista vacía y de error se añadieron para que cada paso diga qué ha pasado y cuál es el siguiente.

## Cómo ejecutarlo

Hace falta Python 3. No hay dependencias externas: el programa usa `csv` y `os`.

```bash
python3 app.py
python3 test.py
python3 -m unittest tests.test_robustness -v
```

`python3 test.py` es la suite oficial del ejercicio. Comparte una sola lista en memoria y debe correr en su propio proceso. La otra suite usa un directorio temporal y también debe correr aparte.

## Menú

En cada vuelta el programa pide una opción.

| Opción | Qué hace | Ejemplo |
| --- | --- | --- |
| 1 | Añade una tarea al final | título `Make the bed` |
| 2 | Borra la tarea de esa posición | `2` borra la segunda |
| 3 | Muestra la lista, numerada desde 1 | |
| 4 | Guarda la lista en `todos.csv` | |
| 5 | Sustituye la lista en memoria por la del archivo | |
| 6 | Sale | |
| `help` o `?` | Muestra la guía con ejemplos | |

Las posiciones empiezan en 1. Después de borrar, las tareas siguientes cambian de número. Para cambiar un título hay que borrar esa tarea y crearla de nuevo.

Un título vacío no se guarda. Una posición que no está en la lista no borra nada. Si `todos.csv` no existe, no es texto o trae una fila con más de una columna, la lista en memoria se queda como estaba.

## Ejemplo registrado

Esta secuencia es la de una sesión real con `python3 app.py`. El menú se imprime entero antes de cada elección; aquí quedan la elección y la respuesta.

Lista vacía, opción 3:

```text
No tasks yet. Choose option 1 to add one. Example: Make the bed
```

Tres altas en la misma ejecución, opción 3:

```text
1. Make the bed
2. Make lunch
3. Clean kitchen
```

Opción 2 y posición 2:

```text
Task removed. Positions were updated:
1. Make the bed
2. Clean kitchen
```

Posición 9 con dos tareas en la lista:

```text
Invalid position: 9 is outside 1-2. Choose option 3 to see current positions.
```

Opción 4:

```text
Saving todo's...
Saved 2 tasks in todos.csv.
```

Otro proceso, con el mismo `todos.csv`, opción 5:

```text
Loaded 2 tasks from todos.csv.
1. Make the bed
2. Clean kitchen
```

Un título con coma se guarda entre comillas para que el lector CSV lo recupere entero. `Buy milk, bread` y `Revisar muelle — ñandú` sobreviven a cerrar el programa y volver a cargar.

## Formato de `todos.csv`

Una tarea por fila, UTF-8, generada con el módulo `csv`. Un título con coma o comillas queda entrecomillado. Una fila en blanco se ignora. El archivo es dato de ejecución y está en `.gitignore`.

## Estructura

| Ruta | Papel |
| --- | --- |
| `app.py` | Programa y funciones que evalúa el ejercicio |
| `test.py` | Pruebas oficiales, sin modificar |
| `tests/test_robustness.py` | Comas, Unicode, archivo ausente y archivo no válido |
| `learn.json` | Manifiesto del ejercicio, copia íntegra |
| `docs/enunciado/` | Enunciado EN/ES de ese mismo commit |
| `third_party/4GeeksAcademy-python-hello/` | Plantilla citada por el enunciado, copia íntegra |
| `.github/workflows/tests.yml` | Ejecuta las dos suites en Python 3.12 |

## Decisiones

- La lista vive en la variable global `todos` porque las pruebas oficiales comparten ese estado entre métodos.
- `delete_task` acepta el número como entero o como texto, que es lo que devuelve `input()`.
- `save_todos` / `load_todos` usan `csv` para que una coma dentro del título no parta la fila. El archivo de la prueba oficial (`jump`, `run`, `roll`, una línea por tarea) se carga igual.
- `server.py` de la plantilla `python-hello` no se ejecuta: importa Flask y este ejercicio pide entrada/salida y terminal solo con la biblioteca estándar.

## Procedencia

- Enunciado y `test.py`: [breatheco-de/exercise-todo-list-cli-python](https://github.com/breatheco-de/exercise-todo-list-cli-python) en `ee72a485a32270da30205db5020d5bc827c26104`.
- Plantilla que el enunciado manda clonar: [4GeeksAcademy/python-hello](https://github.com/4GeeksAcademy/python-hello) en `142f2a913162efafce897da8bf241fe690f60395`. Ese repositorio no publica licencia. El detalle está en `third_party/PROVENANCE.md`.

La plantilla no trae `app.py` ni `test.py`. Esas piezas vienen del ejercicio. La implementación de las cinco funciones está en `app.py`.
