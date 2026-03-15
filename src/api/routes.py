from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from . import models, schemas
from .database import get_db

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/notes")
def list_notes(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    title: str | None = Query(None, description="Filter by title substring"),
    sort: str = Query("id", description="Field to sort by"),
    order: str = Query("asc", description="Sort order: asc or desc"),
    db: Session = Depends(get_db)
):
    """
    List notes with optional pagination, filtering by title, and sorting.
    """
    query = db.query(models.Note)

    if title:
        query = query.filter(models.Note.title.ilike(f"%{title}%"))

    sort_column = getattr(models.Note, sort, None)
    if not sort_column:
        raise HTTPException(status_code=400, detail=f"Invalid sort field: {sort}")
    if order.lower() == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))

    skip = (page - 1) * limit
    notes = query.offset(skip).limit(limit).all()

    return notes


@router.get("/notes/{note_id}")
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.post("/notes", status_code=201)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    new_note = models.Note(title=note.title, content=note.content)
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