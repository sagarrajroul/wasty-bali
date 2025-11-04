from sqlalchemy.orm import Session
import models
import schema

# --- FORM CRUD ---
def create_form(db: Session, form: schema.FormCreate):
    db_form = models.Form(**form.dict())
    db.add(db_form)
    db.commit()
    db.refresh(db_form)
    return db_form


def get_forms(db: Session):
    return db.query(models.Form).all()


def get_form_by_id(db: Session, form_id: int):
    return db.query(models.Form).filter(models.Form.id == form_id).first()
