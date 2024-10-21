from fastapi import status, HTTPException, Depends, APIRouter
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
            raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED, detail=f"Already exists {admin.email}")

        hashedPassword = utils.hash(admin.password)
        admin.password = hashedPassword
        new_admin = models.Admin(**admin.model_dump())
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        
        return new_admin
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.get("/{id}", response_model=schemas.AdminOut)
def get_admin(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Admin).filter(models.Admin.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exist")
    
    return user
