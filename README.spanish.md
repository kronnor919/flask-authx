## 🔐 Flask-AuthX

Flask-AuthX proporciona un sistema completo de gestión de sesiones de usuarios, con autenticación, hashing de contraseñas, base de datos pre-configurada y crea automáticamente los endpoints listos para ser usados por un cliente. 🚀

Y no, no es un boilerplate. No estás obligado a usar exactamente el mismo sistema que yo te imponga en esta herramienta, puedes extender y modificar a tu gusto cada componente, yo solo te ofrezco una solución rápida si estás haciendo un MVP (literalmente solo requiere 6 líneas de código extender tu app Flask y te ahorras casi mil líneas). ⚡

## ⚠️ Advertencias

Este proyecto está actualemente en un estado inestable, ***NO*** se debe usar para otro objetivo que no sea testear funcionalidades, no uses esta extensión en una app que vayas a desplegar. 🚧

Esta mini-documentación puede estar desvinculada del estado real del proyecto (adelantada a las funcionalidades o retrasada). También pueden faltar funcionalidades o ciertos aspectos pueden no quedar claros. De cualquier modo, todas sus opiniones e ideas son bienvenidas. 📝

No soy un desarrollador experimentado, estoy aprendiendo, y este es mi principal proyecto actual, planeo escalarlo y crear una herramienta de verdad pero recuerden que esto es un proyecto de aprendizaje. 🌱

## ✨ Funcionalidades

- 🔐 Autenticación y gestión de usuarios.
- 🛡️ Seguridad de los datos.
- 👥 Autorización basada en roles.
- 🛠️ Cada detalle fundamental de la lógica es ajustable a tus propias necesidades.
- 🗄️ Sistema completo implementado por defecto compatible con cualquier motor de base de datos con SQLAlchemy.

## 🚀 Uso básico

```py
# ./app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_authx import AuthXBuilder

def create_app() -> Flask:
    app = Flask(__name__)

    app.config.from_mapping({
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "FIRST_USER_NAME": "kronnor",
        "FIRST_USER_PASSWORD": "73336463"
    })
    # Tambien podrias cargar la configuracion desde un archivo de entorno (.env)

    SQLAlchemy(app) # Requerido por flask-authx por defecto

    AuthXBuilder(app).build()

    return app
```

Si intentas correr el servidor mediante `flask run` verás que funciona sin problemas, pero ¿Qué ha hecho Flask-AuthX en este punto? 🤔

Si tumbas el servidor (`Ctrl + C`) y ejecutas `flask routes` verás que la salida será algo como:

```
Endpoint               Methods  Rule                    
---------------------  -------  ------------------------
auth.login             POST     /auth/login             
auth.logout            DELETE   /auth/logout            
static                 GET      /static/<path:filename> 
users.delete           DELETE   /users/<int:id>         
users.get_all          GET      /users                  
users.get_by_id        GET      /users/<int:id>         
users.get_by_username  GET      /users/<string:username>
users.post             POST     /users
```

Esto indica que nuestra extensión, efectivamente ha extendido tu aplicación Flask con nuevas funcionalidades. ✅

Incluso si volviéramos a activar el servidor y en el navegador colocamos la siguiente url: `http://localhost:5000/users`.

Te debería cargar una página del debuger de Werkzeug mostrándote los siguientes datos:

```json
{
    "success":true,
    "users":[
        {
            "id":1,
            "role":"admin",
            "username":"kronnor"
        }
    ]
}
```

Que es el usuario que hemos configurado rápidamente en el primer ejemplo de uso. 👤

Ahora que pasa si tu no quieres depender de Flask-SQLAlchemy en tu aplicación, pues no te obligamos a usarlo, sencillo. 🎯

## 🛠️ Personalizando funcionalidades

Con Flask-AuthX tienes el poder de configurar la base de datos que quieras, con el ORM que quieras, con el motor que quieras. 💪

Como te habrás dado cuenta en el primer ejemplo usamos una clase llamada `AuthXBuilder` para activar la extensión, pues esta clase contiene métodos que te ayudan a modificar la lógica con la que trabaja Flask-AuthX.

### 📊 Ejemplo (Acceso a datos)

Quieres hacer tu propia implementación de gestión de usuarios usando la libreria `sqlite3` de python (se que no tiene mucho sentido pero es por simplicidad). Pues debes usar un conjunto de interfaces que ofrece la extensión que ayudan a que tu sistema se acople perfectamente a lo que la extensión espera que haga.

```py
import sqlite3
from flask import Flask
from flask_authx import (
    AuthXBuilder,
    IUsersRepository,
    IDatabaseSetup,
    ISessionsRepository
)

DATABASE_PATH = "./db.sqlite"

def get_database():
    return sqlite3.connect(DATABASE_PATH)

# Nos obliga a implementar un metodo init que será llamado cuando la aplicación tenga que crear la base de datos y ejecutar queries iniciales
class SQLiteDatabaseSetup(IDatabaseSetup):
    def init(self) -> None:
        # Aqui podriamos ejecutar queries para crear el esquema
        # si no esta configurado, insertar un primer usuario si
        # es necesario, y todo lo que necesites hacer

class SQLiteUsersRepository(IUsersRepository):
    def all(self):
        # Realizas tu logica para obtener todos los usuarios que hay
        # en la base de datos, puede que sea complicado implementar
        # paginacion si no recibe parametros pero se esta
        # trabajando en eso.
    
    ...

    # Implementas todos los demas metodos que requiere esta interfaz

class SQLiteSessionsRepository(ISessionsRepository):
    def all(self):
        # Mas de lo mismo...
    
    ...

def create_app() -> Flask:
    app = Flask(__name__)

    app.config.from_mapping({
        "FIRST_USER_NAME": "admin",
        "FIRST_USER_PASSWORD": "73336463"
    })

    # Ya no dependemos de SQLAlchemy

    (
        AuthXBuilder(app)
        .set_database_setup(SQLiteDatabaseSetup())
        .set_users_repository(SQLiteUsersRepository())
        .set_sessions_repository(SQLiteSessionsRepository())
        .build()
    )

    return app
```

El problema de modificar los componentes de base de datos es que cambiar 1 de estos 3 requiere cambiar los 3, aún así la extensión se encarga de que tú no tengas que tocar nada relacionado a los endpoints para que estos cambios se apliquen y las reglas de validación relacionadas a los usuariosse cumplan. 🔄

Pero... ¿Qué reglas? Tú no has definido ninguna de las reglas de validación en este punto, lo hice la extensión, y quizá tú no estés de acuerdo con las reglas que definí, pues déjame decirte que también son perfectamente modificables siguiendo la misma filosofía de heredar de clases y sobreescribir métodos. 📋

### 🧪 Ejemplo (Entidades / reglas de validación)

```py
import string
from flask import Flask
from flask_authx import AuthXBuilder, User, Result, ValidationError

class CustomUser(User):
    # Por defecto verifica que el username tenga al menos
    # 3 caracteres cualquiera, pero quiza tu quieres que 
    # tambien deba contener al menos 1 digito
    @staticmethod
    def validate_username(username: str) -> Result[None, ValidationError]:
        if len(username) == 0:
            return Result.fail(ValidationError("El nombre de usuario debe contener al menos 1 caracter."))
        
        if not any([True for c in username if c in string.digits else False]):
            return Result.fail(ValidationError("El nombre de usuario debe contener al menos 1 digito."))
        
        return Result.ok(None)
    
    # Hay otro metodo: validate_password pero no estas obligado a
    # sobreescribirlos todos

def create_app() -> Flask:
    app = Flask(__name__)

    app.config.from_mapping({
        "FIRST_USER_NAME": "admin",
        "FIRST_USER_PASSWORD": "73336463"
    })

    (
        AuthXBuilder(app)
        .set_user_class(CustomUser)
        .build()
    )

    return app
```

Con esta configuración la extensión se encargará de que cada regla (métodos `validate_*`) se apliquen antes de realizar cualquier operación sobre una entidad en la base de datos. ✅

### 🔑 Ejemplo (Seguridad de contraseñas)

Para controlar el hasheo de las contraseñas existe la interfaz `IPasswordHashing` y un método del builder que nos permite hacer lo que querramos con esta lógica.

```py
from flask_authx import IPasswordHashing

class BlehPasswordHashing(IPasswordHashing):
    HASH_SUFFIX = "bleh-hash"

    def hash(self, password: str) -> str:
        return password + self.HASH_SUFFIX # Puedes usar una libreria como bcrypt
    
    def verify(self, password: str, hashed: str) -> bool:
        return password == hashed[:len(self.HASH_SUFFIX)]
    
    # Este codigo es claramente INSEGURO para hashing.
    # Solo es para mantener simplicidad.

def create_app():
    # ... Codigo de siempre

    (
        AuthXBuilder(app)
        .set_password_hashing(BlehPasswordHashing())
        .build()
    )

    return app
```

## 📄 Licencia

MIT: Libre distribución mientras que no sea comercial. Ver [LICENSE 📜](./LICENSE)
