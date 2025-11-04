from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from db import Base

class ShopOwner(Base):
    __tablename__ = "shop_owner"

    id = Column(Integer, primary_key=True, index=True)
    owner_name = Column(String(100), nullable=False)
    shop_name = Column(String(50), nullable=False)
    shop_id = Column(String(50), unique=True, nullable=False)
    phone_number = Column(String(15), nullable=False)
    password = Column(String, nullable=False)
    photo_url = Column(String, nullable=True)

class Form(Base):
    id = Column(Integer, primary_key=True, index=True)
    type_of_shop = Column(String(100), nullable=False)
    dustbin_available = Column(Boolean, default=False)
    hand_sanitizer_available = Column(Boolean, default=False)
    use_plastic_bags = Column(Boolean, default=True)
    shop_owner_id = Column(Integer, ForeignKey("shop_owner.id"))
    rating = Column(Integer, default=0)
    __tablename__ = "form"


class Volunteer(Base):
    __tablename__ = "volunteer"

    id = Column(Integer, primary_key=True, index=True)
    volunteer_code = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    status = Column(String(20), default="active")

class ShopQR(Base):
    __tablename__ = "shop_qr"

    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shop_owner.id"))
    qrcode_id = Column(String(20), unique=True, nullable=False)
