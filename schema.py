from datetime import datetime
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
    phone_number: str
    password: str


# Response schema (exclude password)
class ShopOwnerResponse(ShopOwnerBase):
    id: int

    class Config:
        orm_mode = True

class FormBase(BaseModel):
    form_details: str
    score: Optional[int] = 0


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

class WinnerCreate(BaseModel):
    phone_number: str
    winner_details: Optional[str] = None
    type: Optional[str] = None
    awarded_at: Optional[datetime] = None


class WinnerResponse(BaseModel):
    id: int
    winner_details: Optional[str]
    awarded_at: datetime
    shop_owner: dict
    form: dict

    class Config:
        orm_mode = True