from fastapi import APIRouter, Depends, HTTPException, status, Form, UploadFile
from sqlalchemy.orm import Session
import schema
import crud.auth_crud as auth_crud
from db import get_db
from utils.s3_utils import upload_to_s3

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=schema.ShopOwnerResponse, status_code=status.HTTP_201_CREATED)
@router.post("/signup", response_model=schema.ShopOwnerResponse)
async def signup(
    owner_name: str = Form(...),
    shop_name: str = Form(...),
    shop_id: str = Form(...),
    phone_number: str = Form(...),
    password: str = Form(...),
    photo: UploadFile = None,
    db: Session = Depends(get_db)
):
    photo_url = None
    if photo:
        photo_url = upload_to_s3(photo)

    owner_data = schema.ShopOwnerCreate(
        owner_name=owner_name,
        shop_name=shop_name,
        shop_id=shop_id,
        phone_number=phone_number,
        password=password,
        photo_url=photo_url
    )

    db_owner = auth_crud.create_shop_owner(db, owner_data)
    if not db_owner:
        raise HTTPException(status_code=400, detail="Shop ID already exists")
    return db_owner


@router.post("/login", response_model=schema.ShopOwnerResponse, status_code=status.HTTP_200_OK)
def login(credentials: schema.ShopOwnerLogin, db: Session = Depends(get_db)):
    owner = auth_crud.authenticate_shop_owner(db, credentials.shop_id, credentials.password)
    if not owner:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return owner
