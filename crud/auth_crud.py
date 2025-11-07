from sqlalchemy.orm import Session
import models
import schema
from utils.utils import hash_password, verify_password

def create_shop_owner(db: Session, owner: schema.ShopOwnerCreate):
    # Check if shop_id already exists
    existing_owner = db.query(models.ShopOwner).filter(models.ShopOwner.phone_number == owner.phone_number).first()
    if existing_owner:
        return {"error": "Phone number already exists"}

    #hashed_pwd = hash_password(owner.password)
    db_owner = models.ShopOwner(
        owner_name=owner.owner_name,
        shop_name=owner.shop_name,
        shop_id=owner.shop_id,
        phone_number=owner.phone_number,
        password=owner.password,
        photo_url=owner.photo_url
    )
    db.add(db_owner)
    db.commit()
    db.refresh(db_owner)
    return db_owner


def authenticate_shop_owner(db: Session, phone_number: str, password: str):
    owner = db.query(models.ShopOwner).filter(models.ShopOwner.phone_number == phone_number).first()
    if not owner:
        return None
    if password != owner.password:
        return None
    return owner

def get_shop_owner_by_id(db: Session, owner_id: int):
    return db.query(models.ShopOwner).filter(models.ShopOwner.id == owner_id).first()
