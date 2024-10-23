from passlib.context import CryptContext


pwd_context = CryptContext(schemes='bcrypt', deprecated='auto')


def hashedPassword(password: str):
    return pwd_context.hash(password)


def verify(plainPassword, hashedPassword):
    return pwd_context.verify(plainPassword, hashedPassword)
