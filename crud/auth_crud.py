from sqlalchemy.orm import Session
import models
import schema
from utils.utils import hash_password, verify_password

def create_shop_owner(db: Session, owner: schema.ShopOwnerCreate):
    # Check if shop_id already exists
    existing_owner = db.query(models.ShopOwner).filter(models.ShopOwner.shop_id == owner.shop_id).first()
    if existing_owner:
        return None  # handle duplicate in route

    hashed_pwd = hash_password(owner.password)
    db_owner = models.ShopOwner(
        owner_name=owner.owner_name,
        shop_name=owner.shop_name,
        shop_id=owner.shop_id,
        phone_number=owner.phone_number,
        password=hashed_pwd,
        photo_url=owner.photo_url
    )
    db.add(db_owner)
    db.commit()
    db.refresh(db_owner)
    return db_owner


def authenticate_shop_owner(db: Session, shop_id: str, password: str):
    owner = db.query(models.ShopOwner).filter(models.ShopOwner.shop_id == shop_id).first()
    if not owner:
        return None
    if not verify_password(password, owner.password):
        return None
    return owner
