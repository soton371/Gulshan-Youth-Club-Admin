from fastapi import status, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, utils, oauth2, schemas
from ..custom_responses import ResponseSuccess, ResponseFailed


router = APIRouter(tags=['Authentication'])


@router.post("/login")
def login(user_credentials: models.AdminLogin, db: Session = Depends(get_db)):
    try:
        fetchAdmin = db.query(schemas.Admin).filter(
            schemas.Admin.email == user_credentials.email).first()
        if not fetchAdmin:
            return ResponseFailed(
                status_code=status.HTTP_404_NOT_FOUND, message=f"User not found with {user_credentials.email}")
        print('2222')
        verify = utils.verify(user_credentials.password, fetchAdmin.password)
        if not verify:
            return ResponseFailed(
                status_code=status.HTTP_404_NOT_FOUND, message="Incorrect password")

        # create token & return token
        accessToken = oauth2.create_access_token(
            data={"user_id": fetchAdmin.id})
        data = {"access_token": accessToken, "token_type": "Bearer"}
        return ResponseSuccess(status_code=status.HTTP_200_OK, data=data)
    except Exception as error:
        print(f'error in login {error}')
        return ResponseFailed(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Something went wrong")



@router.post("/send-otp")
def send_otp(payload: models.SendOtpData, db: Session = Depends(get_db)):
    try:
        # send otp & store in db
        print('d')
    except Exception as error:
        print(f"error in send_otp: {error}")
        return ResponseFailed(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Something went wrong")
    
