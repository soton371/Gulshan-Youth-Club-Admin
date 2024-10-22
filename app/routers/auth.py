from fastapi import status, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, utils, oauth2, schemas
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..custom_responses import ResponseSuccess, ResponseFailed


router = APIRouter(tags=['Authentication'])


@router.post("/login")
def login(user_credentials: schemas.AdminLogin, db: Session = Depends(get_db)):
    try:
        fetchAdmin = db.query(models.Admin).filter(
            models.Admin.email == user_credentials.email).first()
        if not fetchAdmin:
            raise ResponseFailed(
                status_code=status.HTTP_404_NOT_FOUND, message=f"User not found with {user_credentials.username}")

        verify = utils.verify(user_credentials.password, fetchAdmin.password)
        if not verify:
            raise ResponseFailed(
                status_code=status.HTTP_404_NOT_FOUND, message="Incorrect password")

        # create token & return token
        accessToken = oauth2.create_access_token(
            data={"user_id": fetchAdmin.id})
        data = {"access_token": accessToken, "token_type": "Bearer"}
        return ResponseSuccess(status_code=status.HTTP_200_OK, data=data)
    except Exception as error:
        print(f'error in login')
        return ResponseFailed(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Something went wrong")
