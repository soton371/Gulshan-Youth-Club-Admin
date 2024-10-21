from fastapi import status, Depends, APIRouter
from fastapi.responses import JSONResponse

from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/admin",
    tags=['Admin']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.AdminOut)
async def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    try:
        existAdmin = db.query(models.Admin).filter(models.Admin.email == admin.email).first()

        if existAdmin:
            return JSONResponse(
                status_code=status.HTTP_208_ALREADY_REPORTED,
                content={"success": False, "message": f"Admin with email {admin.email} already exists."}
            )

        hashedPassword = utils.hash(admin.password)
        admin.password = hashedPassword
        new_admin = models.Admin(**admin.model_dump())
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        
        return new_admin
    except Exception as error:
        return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"success": False, "message": "Something went wrong!"}
            )

@router.get("/{id}")
def get_admin(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Admin).filter(models.Admin.id == id).first()
    
    if not user:
        return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"success": False, "message": f"User with id {id} does not exist"}
            )
    # return ResponseSuccess(data=user.id)
    return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"success": True, "data": user.email}
            )
