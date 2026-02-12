# Contributing

## 🎉 Gracias por querer contribuir

Flask-AuthX es mi proyecto hobby, pero lo cuido como si fuera profesional.

Tener a alguien como tú aquí ya es un montón. Sea cual sea tu nivel, eres bienvenido.

## 🐞 Reportar bugs

Abre un issue con la plantilla ["Bug report"](https://github.com/kronnor919/flask-authx/issues/new?template=bug_report.md) y completa los campos.

¿No estás seguro de si es un bug?

Primero crea una Discussion en la categoría "Help". Lo hablamos ahí y si es bug, lo movemos a issues.

## 💡 Proponer features

Abre un issue con la plantilla ["Feature request"](https://github.com/kronnor919/flask-authx/issues/new?template=feature_request.md).

También puedes compartir tu idea en Discussions (categoría "Ideas") antes de publicarla. Así recibes feedback rápido y la mejoramos entre todos.

## 🛠 Configuración del entorno

```bash
git clone https://github.com/kronnor919/flask-authx
cd flask-authx
```

### Con UV (recomendado)

```bash
uv sync
```

Funciona en Linux, macOS y Windows.

### Con pip

1. Crear entorno virtual:

    ```bash
    python -m venv .venv
    ```

    (usa `python3` si es necesario)

2. Activar:

    - Linux / macOS: `source ./.venv/bin/activate`

    - Windows: `./.venv/Scripts/activate`

3. Instalar dependencias (junto a las de desarrollo):

    ```bash
    pip install .
    pip install . --group dev
    ```

## ✅ Linting

Formato y linting: Ruff (configuración por defecto)

Antes de cada commit, Ruff se ejecuta automáticamente.
Si algo no cumple las reglas, lo corrige solo.
Añades los cambios otra vez (`git add .`) y repites el commit. Así de fácil.

## 🧪 Tests

- Ejecutar tests: `pytest tests/`

- No hay una cobertura mínima de tests aún

- Todos los tests deben haber pasado para poder realizar un commit

## 📝 Conventional Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/) para los mensajes de commit.

Formato: `<tipo>(<ámbito>): descripción`

Tipos comunes:

- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Formato, puntos y comas, etc.
- `refactor`: Reestructuración de código
- `test`: Agregar o modificar tests

Ejemplo: `feat(auth): agregar validación de email`

## 📚 Documentación

### Reglas

1. **Traducción** - Si contribuyes a la documentación debes mantener sincronizadas la versión en inglés y la versión en español:

    - Versión en inglés: `nombre.ext` (ej: `README.md`, `CONTRIBUTING.md`)
    - Versión en español: `nombre.spanish.ext` (ej: `README.spanish.md`, `CONTRIBUTING.spanish.md`)

2. **Referencia bilingüe** - Antes de comenzar con el contenido relevante del archivo en inglés, deja claro que existe la versión en español. Esta especificación debe estar en ambos idiomas e incluir una referencia directa a la versión en español. Puede estar al inicio o después de una breve introducción. Los archivos en español no necesitan esta referencia.

    Formato esperado:

    ```markdown
    > [Tu aclaración en español (Referencia al archivo)] ([Tu aclaración en inglés])
    ```

    Ejemplo:

    ```markdown
    > Este documento también está disponible en [Español](CONTRIBUTING.spanish.md) (This document is also available in Spanish).
    ```

3. **Formato idéntico** - Ambos archivos deben usar la misma sintaxis (.md o .rst)

4. **Estructura consistente** - Misma jerarquía de títulos, listas y código

5. **Decoración con emojis** - Mantén los mismos emojis en las mismas posiciones

6. **Contenido** - Lo más idéntico posible en estructura, con texto adaptado al idioma

7. **Tono** - Puede ser amable y un poco coloquial, pero nunca faltando al respeto a nada ni a nadie

## 🔁 Flujo para Pull Requests

1. Fork del repositorio a tu cuenta.

2. Clonar localmente:

    ```bash
    git clone https://github.com/tu-usuario/tu-fork.git
    cd tu-fork
    git remote add upstream https://github.com/kronnor919/flask-authx
    ```

3. Crear rama:

    ```bash
    git checkout -b nombre-descriptivo
    ```

4. Hacer commits claros y atómicos:

    ```bash
    git commit -m "fix: error al validar email"
    ```

5. Mantener tu rama actualizada:

    ```bash
    git fetch upstream
    git rebase upstream/main
    ```

6. Subir cambios a tu fork:

    ```bash
    git push origin nombre-rama
    ```

7. Abrir Pull Request desde tu fork hacia este repositorio.

    - Título claro

    - Descripción que explique qué cambia y por qué

    - Referencia el issue si existe (`Closes #42`)

8. Revisión:

    - Puedo pedir cambios o hacer comentarios

    - Subes más commits a la misma rama

    - Se ven automáticamente en la PR

9. Merge:
    Política de merge: merge normal con `--no-ff`.
    Yo lo reviso, apruebo y fusiono.
    La rama se elimina manualmente.
    Mi disponibilidad es muy variable, pero te aseguro que cada PR lo voy a revisar y responder.

## ❓ ¿Necesitas ayuda?

El único foro de la comunidad es [Discussions](https://github.com/kronnor919/flask-authx/discussions) de GitHub.

Abre una Discussion en la categoría "Help".
