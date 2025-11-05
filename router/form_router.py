from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import Date
from sqlalchemy.orm import Session
from crud import form_crud
import schema
from db import get_db
import models
from datetime import datetime

router = APIRouter(prefix="/form", tags=["Form"])

@router.post("/", response_model=schema.FormResponse)
def create_form(form: schema.FormCreate, db: Session = Depends(get_db)):
    db_form = form_crud.create_form(db, form)
    return db_form


@router.get("/", response_model=list[schema.FormResponse])
def read_forms(db: Session = Depends(get_db)):
    forms = form_crud.get_forms(db)
    return forms


@router.get("/{shope_id}", response_model=schema.FormResponse)
def read_form(shope_id: int, db: Session = Depends(get_db)):
    form = form_crud.get_form_by_id(db, shope_id)
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")
    return form

# @router.get("/list",status_code=status.HTTP_200_OK)
# def list_forms(
#     db: Session = Depends(get_db),
#     shop_id: Optional[str] = Query(None, description="Filter by Shop ID"),
#     shop_name: Optional[str] = Query(None, description="Filter by Shop Name"),
#     sort_by_score: Optional[str] = Query(None, regex="^(asc|desc)$", description="Sort by Score"),
#     date: Optional[datetime] = Query(None, description="Filter by specific date (YYYY-MM-DD)")
# ):
#     # Start query joining both tables
#     query = db.query(models.Form).join(models.ShopOwner)

#     # Filter by Shop ID
#     if shop_id:
#         query = query.filter(models.ShopOwner.shop_id == shop_id)

#     # Filter by Shop Name
#     if shop_name:
#         query = query.filter(models.ShopOwner.shop_name.ilike(f"%{shop_name}%"))

#     # Filter by single date (same day)
#     if date:
#         query = query.filter(models.Form.created_at.cast(Date) == date.date())

#     # Sorting
#     if sort_by_score == "asc":
#         query = query.order_by(models.Form.score.asc())
#     elif sort_by_score == "desc":
#         query = query.order_by(models.Form.score.desc())
#     else:
#         query = query.order_by(models.Form.created_at.desc())

#     forms = query.all()
#     return forms
