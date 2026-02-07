# 🔐 Flask-AuthX

Flask-AuthX provides a complete user session management system, with authentication, password hashing, a pre-configured database, and automatically creates ready-to-use endpoints for any client. 🚀

And no, it's not a boilerplate. You're not forced to use exactly the same system I impose in this tool—you can extend and modify every component as you like. I'm just offering a quick solution if you're building an MVP (literally takes only 6 lines of code to extend your Flask app, saving you almost a thousand lines). ⚡

Una versión en español de este archivo está disponible en: [README.spanish.md](./README.spanish.md) (A spanish version of this file is available)

## ⚠️ Warnings

This project is currently in an unstable state. ***DO NOT*** use it for anything other than testing features. Do not use this extension in an app you plan to deploy. 🚧

This mini-documentation may be out of sync with the actual state of the project (ahead of features or behind). Some features may also be missing or certain aspects may not be clear. In any case, all your opinions and ideas are welcome. 📝

This is my main project right now. I plan to scale it and turn it into a real tool, but remember this is a learning project. 🌱

## ✨ Features

- 🔐 User authentication and management.
- 🛡️ Data security.
- 👥 Role-based authorization.
- 🛠️ Every key logic detail can be adjusted to your own needs.
- 🗄️ A complete default system compatible with any database engine via SQLAlchemy.

## 🚀 Basic Usage

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
    # You could also load configuration from an environment file (.env)

    SQLAlchemy(app) # Required by flask-authx by default

    AuthXBuilder(app).build()

    return app
```

If you try to run the server executing `flask run`, you’ll see it works without issues—but what has Flask-AuthX done at this point? 🤔

If you stop the server (`Ctrl + C`) and run `flask routes`, you’ll see something like:

```text
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

This means our extension has indeed extended your Flask app with new functionality. ✅

Even if you restart the server and go to the following URL in your browser: http://localhost:5000/users, you should see a Werkzeug debugger page showing:

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

That's the user we quickly configured in the first usage example. 👤

But what if you don't want to rely on Flask-SQLAlchemy in your app? Well, we don't force you to use it—simple. 🎯

## 🛠️ Customizing Your Extension

With Flask-AuthX, you have the power to configure any database you want, with any ORM you want, with any engine you want. 💪

As you may have noticed in the first example, we used a class called AuthXBuilder to activate the extension. This class contains methods that help you change how Flask-AuthX works.

## 📊 Example (Data Access)

You want to create your own user management implementation using Python’s built-in `sqlite3` library (I know it doesn’t make much sense, but it’s for simplicity). You’ll need to use a set of interfaces provided by the extension to ensure your system integrates perfectly with what the extension expects.

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

# Requires us to implement an init method that will be called when the app needs to create the database and run initial queries
class SQLiteDatabaseSetup(IDatabaseSetup):
    def init(self) -> None:
        # Here you could execute queries to create the schema
        # if not already set up, insert a first user if
        # necessary, and anything else you need to do

class SQLiteUsersRepository(IUsersRepository):
    def all(self):
        # Add your logic to get all users in the database.
        # Pagination might be tricky without parameters, but
        # we’re working on it.
    
    ...

    # Implement all other methods required by this interface

class SQLiteSessionsRepository(ISessionsRepository):
    def all(self):
        # More of the same...
    
    ...

def create_app() -> Flask:
    app = Flask(__name__)

    app.config.from_mapping({
        "FIRST_USER_NAME": "admin",
        "FIRST_USER_PASSWORD": "73336463"
    })

    # No longer dependent on SQLAlchemy

    (
        AuthXBuilder(app)
        .set_database_setup(SQLiteDatabaseSetup())
        .set_users_repository(SQLiteUsersRepository())
        .set_sessions_repository(SQLiteSessionsRepository())
        .build()
    )

    return app
```

The problem with modifying database components is that changing one of these three usually requires changing all three. Still, the extension ensures you don't have to touch anything related to the endpoints for these changes to apply, and all user-related validation rules will still be enforced. 🔄

But… what rules? You haven't defined any validation rules at this point—I did, the extension did. And maybe you don't agree with the rules I defined. Well, let me tell you they're also fully customizable following the same philosophy of inheriting from classes and overriding methods. 📋

## 🧪 Example (Entities / Validation Rules)

```py
import string
from flask import Flask
from flask_authx import AuthXBuilder, User, Result, ValidationError

class CustomUser(User):
    # By default, it checks that the username has at least
    # 3 characters, but maybe you also want it to contain
    # at least 1 digit
    @staticmethod
    def validate_username(username: str) -> Result[None, ValidationError]:
        if len(username) == 0:
            return Result.fail(ValidationError("Username must contain at least 1 character."))
        
        if not any([True for c in username if c in string.digits else False]):
            return Result.fail(ValidationError("Username must contain at least 1 digit."))
        
        return Result.ok(None)
    
    # There’s another method: validate_password, but you’re not
    # required to override them all

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

With these changes, the extension will ensure each rule (the `validate_*` methods) is applied before performing any operation on an entity in the database. ✅

## 🔑 Example (Password Security)

To control password hashing, there’s the `IPasswordHashing` interface and a builder method that lets you do whatever you want with this logic.

```py
from flask_authx import IPasswordHashing

class BlehPasswordHashing(IPasswordHashing):
    HASH_SUFFIX = "bleh-hash"

    def hash(self, password: str) -> str:
        return password + self.HASH_SUFFIX # You can use a library like bcrypt
    
    def verify(self, password: str, hashed: str) -> bool:
        return password == hashed[:-len(self.HASH_SUFFIX)]
    
    # This code is clearly INSECURE for hashing.
    # It’s just for simplicity.

def create_app():
    # ... The usual code

    (
        AuthXBuilder(app)
        .set_password_hashing(BlehPasswordHashing())
        .build()
    )

    return app
```

## 📄 License

MIT: Free use and distribution. See [LICENSE 📜](./LICENSE)
