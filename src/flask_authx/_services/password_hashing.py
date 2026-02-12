import bcrypt

from flask_authx._interfaces.security import IPasswordHashing


class BcryptPasswordHashing(IPasswordHashing):
    def hash(self, password: str) -> str:
        salt = bcrypt.gensalt(12)
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    def verify(self, password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
