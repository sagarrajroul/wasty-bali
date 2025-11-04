from pydantic import BaseModel
from typing import Optional

# Base schema
class ShopOwnerBase(BaseModel):
    owner_name: str
    shop_name: str
    shop_id: str
    phone_number: str
    photo_url: Optional[str] = None


# Signup schema (includes password)
class ShopOwnerCreate(ShopOwnerBase):
    password: str


# Login schema
class ShopOwnerLogin(BaseModel):
    shop_id: str
    password: str


# Response schema (exclude password)
class ShopOwnerResponse(ShopOwnerBase):
    id: int

    class Config:
        orm_mode = True

class FormBase(BaseModel):
    type_of_shop: str
    dustbin_available: bool = False
    hand_sanitizer_available: bool = False
    use_plastic_bags: bool = True
    rating: Optional[int] = 0


class FormCreate(FormBase):
    shop_owner_id: int


class FormResponse(FormBase):
    id: int
    shop_owner_id: int

    class Config:
        orm_mode = True

class VolunteerSchema(BaseModel):
    name: str
    password: str
    status: bool = True

class VolunteerLogin(BaseModel):
    name: str
    password: str

class ShopQR(BaseModel):
    id: str
    shop_id: int
    qrcode_id: str


class UserScanRequest(BaseModel):
    shop_id: int
    qrcode_id: str


class VolunteerScanRequest(BaseModel):
    qrcode_id: str