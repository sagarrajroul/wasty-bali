from fastapi import APIRouter, Depends, status, HTTPException

from db import get_db
from schema import UserScanRequest
from sqlalchemy.orm import Session
import models

router = APIRouter(prefix="/scan", tags=["Scan"])
@router.post("/shop")
def user_scan(data: UserScanRequest,db: Session = Depends(get_db)):
    # Check if qrcode_id already exists (optional)
    db_qr = db.query(models.ShopQR).filter(models.ShopQR.qrcode_id == data.qrcode_id).first()
    if db_qr:
        raise HTTPException(status_code=400, detail="QR Code already exists")

    qr = models.ShopQR(
        shop_id=data.shop_id,
        qrcode_id=data.qrcode_id
    )
    db.add(qr)
    db.commit()
    db.refresh(qr)
    return {"message": "QR code saved successfully", "data": qr}


@router.get("/volunteer/{qrcode_id}", status_code=status.HTTP_200_OK)
def volunteer_scan(qrcode_id: str, db: Session = Depends(get_db)):
    shop = db.query(models.ShopQR).filter(models.ShopQR.qrcode_id == qrcode_id).first()
    if shop:
        return {"shop_id": shop.shop_id}
    raise HTTPException(status_code=404, detail="QR Code not found")