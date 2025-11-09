from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import Date
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
import models
import schema
from db import get_db

router = APIRouter(prefix="/winner", tags=["Winner"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_winner(winner_data: schema.WinnerCreate, db: Session = Depends(get_db)):
    today = winner_data.awarded_at
    awarded = db.query(models.Winner).filter(models.Winner.awarded_at.cast(Date) == today.date(), models.Winner.type==winner_data.type).first()
    if awarded:
        raise HTTPException(status_code=400, detail="Winner for today already exists")
    
    shop_owner = db.query(models.ShopOwner).filter(models.ShopOwner.phone_number == winner_data.phone_number).first()
    if not shop_owner:
        raise HTTPException(status_code=404, detail="Shop owner not found")

    
    new_winner = models.Winner(
        shop_owner_id=shop_owner.id,
        winner_details=winner_data.winner_details,
        awarded_at=today, 
        type=winner_data.type
    )
    db.add(new_winner)
    db.commit()
    db.refresh(new_winner)

    return {"message": "Winner added successfully", "winner_id": new_winner.id}

@router.post("/today", status_code=status.HTTP_200_OK)
def get_winners(db: Session = Depends(get_db), date: Optional[datetime] = Query(None)):
    winner = db.query(models.Winner).filter(models.Winner.awarded_at.cast(Date) == date.date()).first()
    if not winner:
        raise HTTPException(status_code=404, detail="No winners found for today")
    winners = (
        db.query(models.Form)
        .join(models.ShopOwner)
        .options(joinedload(models.Form.shop_owner))
        .filter(models.ShopOwner.id == winner.shop_owner_id)
    )
    
    if not winners:
        raise HTTPException(status_code=404, detail="No winners found for this date")
    return winners.all()

@router.get("/winners/all", status_code=status.HTTP_200_OK)
def get_all_winners(db: Session = Depends(get_db)):
    all_winners = (
        db.query(models.Winner)
        .options(
            joinedload(models.Winner.shop_owner).joinedload(models.ShopOwner.forms)
        )
        .order_by(models.Winner.awarded_at.desc())
        .all()
    )

    if not all_winners:
        raise HTTPException(status_code=404, detail="No winners found")

    return all_winners
