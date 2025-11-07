
from fastapi import APIRouter, Depends, Query, status
from typing import Optional
from sqlalchemy import Date
from sqlalchemy.orm import Session, joinedload
import models
from datetime import datetime
import schema
from db import get_db


router = APIRouter(prefix="/admin", tags=["Authentication"])

@router.get("/owners", response_model=list[schema.ShopOwnerResponse])
def get_all_owners(db: Session = Depends(get_db)):
    return db.query(models.ShopOwner).all()


@router.post("/form/list", status_code=status.HTTP_200_OK)
def list_forms(
    db: Session = Depends(get_db),
    owner_name: Optional[str] = Query(None),
    phone_number: Optional[str] = Query(None),
    shop_name: Optional[str] = Query(None),
    sort_by_score: Optional[str] = Query(None, regex="^(asc|desc)$"),
    date: Optional[datetime] = Query(None)
):
    query = (
        db.query(models.Form)
        .join(models.ShopOwner)
        .options(joinedload(models.Form.shop_owner))  # 👈 include related ShopOwner
    )

    if phone_number:
        query = query.filter(models.ShopOwner.phone_number.ilike(f"%{phone_number}%"))
    if owner_name:
        query = query.filter(models.ShopOwner.owner_name.ilike(f"%{owner_name}%"))
    if shop_name:
        query = query.filter(models.ShopOwner.shop_name.ilike(f"%{shop_name}%"))
    if date:
        query = query.filter(models.Form.created_at.cast(Date) == date.date())

    if sort_by_score == "asc":
        query = query.order_by(models.Form.score.asc())
    elif sort_by_score == "desc":
        query = query.order_by(models.Form.score.desc())
    else:
        query = query.order_by(models.Form.created_at.desc())

    forms = query.all()

    return {
        "total": len(forms),
        "forms": forms
        # "forms": [
        #     {
        #         "form_id": f.id,
        #         "score": f.score,
        #         "created_at": f.created_at,
        #         "form_details": f.form_details,
        #         "shop_owner": {
        #             "shop_id": f.shop_owner.shop_id,
        #             "shop_name": f.shop_owner.shop_name,
        #             "owner_name": f.shop_owner.owner_name
        #         }
        #     }
        #     for f in forms
        # ]
    }
