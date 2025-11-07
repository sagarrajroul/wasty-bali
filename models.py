from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, func
from sqlalchemy.orm import relationship

from db import Base

class ShopOwner(Base):
    __tablename__ = "shop_owner"

    id = Column(Integer, primary_key=True, index=True)
    owner_name = Column(String(100), nullable=False)
    shop_name = Column(String(50), nullable=False)
    shop_id = Column(String(50), nullable=True)
    phone_number = Column(String(15), nullable=False)
    password = Column(String, nullable=False)
    photo_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    forms = relationship("Form", back_populates="shop_owner")

class Form(Base):
    id = Column(Integer, primary_key=True, index=True)
    shop_owner_id = Column(Integer, ForeignKey("shop_owner.id"))
    form_details = Column(String(500), nullable=False)
    score = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    shop_owner = relationship("ShopOwner", back_populates="forms")
    __tablename__ = "form"


class Volunteer(Base):
    __tablename__ = "volunteer"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    status = Column(Boolean, default=True)

class ShopQR(Base):
    __tablename__ = "shop_qr"

    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shop_owner.id"))
    qrcode_id = Column(String(20), unique=True, nullable=False)
