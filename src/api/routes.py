from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas
from .database import get_db

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/notes")
def get_notes(db: Session = Depends(get_db)):
    return db.query(models.Note).all()


@router.get("/notes/{note_id}")
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return note


@router.post("/notes", status_code=201)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):

    new_note = models.Note(
        title=note.title,
        content=note.content
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note


@router.put("/notes/{note_id}")
def update_note(note_id: int, data: schemas.NoteUpdate, db: Session = Depends(get_db)):

    note = db.query(models.Note).filter(models.Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note.title = data.title
    note.content = data.content

    db.commit()
    db.refresh(note)

    return note


@router.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):

    note = db.query(models.Note).filter(models.Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()

    return {"message": "Note deleted"}