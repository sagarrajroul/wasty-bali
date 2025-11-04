from fastapi import APIRouter, HTTPException, status, Depends
from db import get_db
from models import Volunteer
from schema import VolunteerLogin
from sqlalchemy.orm import Session


router = APIRouter(prefix="/volunteer", tags=["Volunteer"])


@router.post("/login")
def check_volunteer(credentials: VolunteerLogin, db: Session = Depends(get_db)):
    volunteer = db.query(Volunteer).filter(Volunteer.name == credentials.name).first()

    if not volunteer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Volunteer not found")

    # Compare plain password or hashed
    if volunteer.password != credentials.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")

    return {"message": "Login successful", "volunteer": volunteer}