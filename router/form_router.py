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

