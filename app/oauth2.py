import jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from sqlalchemy.orm import Session
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from .config import settings
from .custom_responses import ResponseFailed

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    toEncode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    toEncode.update({"exp": expire})

    return jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        userId = str(payload.get('user_id'))


        if userId is None:
            return credential_exception

        token_data = schemas.TokenData(id=userId)
        return token_data
    except Exception as e:
        print(f"error in verify_access_token: {e}")
        return credential_exception
    
    



def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    try:
        credential_exception = ResponseFailed(status_code=status.HTTP_401_UNAUTHORIZED, message="Could not validate credential")

        tokenData = verify_access_token(token, credential_exception)
        admin=db.query(models.Admin).filter(models.Admin.id == tokenData.id).first()

        return admin
    except Exception as error:
        print(f'error in get_current_user: {error}')
        return ResponseFailed(status_code=status.HTTP_401_UNAUTHORIZED, message="Could not validate credential")
    