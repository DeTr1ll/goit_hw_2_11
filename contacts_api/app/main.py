from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/contacts/", response_model=schemas.ContactInDB)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db, contact)

@app.get("/contacts/", response_model=list[schemas.ContactInDB])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_contacts(db, skip=skip, limit=limit)

@app.get("/contacts/{contact_id}", response_model=schemas.ContactInDB)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.get_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.put("/contacts/{contact_id}", response_model=schemas.ContactInDB)
def update_contact(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(get_db)):
    return crud.update_contact(db, contact_id, contact)

@app.delete("/contacts/{contact_id}", response_model=schemas.ContactInDB)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    return crud.delete_contact(db, contact_id)

@app.get("/contacts/search/", response_model=list[schemas.ContactInDB])
def search_contacts(query: str, db: Session = Depends(get_db)):
    return crud.search_contacts(db, query)

@app.get("/contacts/birthdays/", response_model=list[schemas.ContactInDB])
def upcoming_birthdays(db: Session = Depends(get_db)):
    return crud.get_upcoming_birthdays(db)