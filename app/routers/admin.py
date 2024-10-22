from fastapi import status, Depends, APIRouter

from app import oauth2
from ..custom_responses import ResponseSuccess, ResponseFailed
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/admin",
    tags=['Admin']
)


@router.post("/")
async def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    try:
        existAdmin = db.query(models.Admin).filter(
            models.Admin.email == admin.email).first()

        if existAdmin:
            return ResponseFailed(status_code=status.HTTP_208_ALREADY_REPORTED, message=f"Admin with email {admin.email} already exists.")

        hashedPassword = utils.hash(admin.password)
        admin.password = hashedPassword
        new_admin = models.Admin(**admin.model_dump())
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        data = {
            "id": new_admin.id,
            "email": new_admin.email,
            "created_at": str(new_admin.created_at)
        }
        return ResponseSuccess(status_code=status.HTTP_201_CREATED, data=data)
    except Exception as error:
        print(f"error in create_admin: {error}")
        return ResponseFailed(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Something went wrong!"
        )


@router.get("/")
def get_profile(current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    try:
        adminFetch = db.query(models.Admin).filter(
            models.Admin.id == current_user.id).first()

        data = {
            "id": adminFetch.id,
            "email": adminFetch.email,
            "created_at": str(adminFetch.created_at)
        }
        return ResponseSuccess(
            status_code=status.HTTP_200_OK,
            data=data
        )
    except Exception as error:
        print(f"error in get_admin: {error}")
        return ResponseFailed(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Something went wrong!"
        )
