from fastapi import APIRouter, HTTPException, Query, Response
from fastapi.responses import JSONResponse

from models.note_models import Note, NoteCreate, NoteUpdate
from services.note_services import (
    create_note,
    filter_notes_by_tags,
    load_notes,
    get_note_by_id,
    update_note_service,
    delete_note_service,
)

router = APIRouter()

@router.get("/")
def read_root():
    return {"answer": "Hello World" }


@router.post("/notes", response_model=Note, status_code=201)
def post_note(note: NoteCreate):
    return create_note(note)    
    
@router.get("/notes")
def get_notes(tags: list[str] = Query(default_factory=list)):
    notes = load_notes() 
    notes = filter_notes_by_tags(notes, tags)
    return notes

@router.get("/notes/{id}", response_model=Note)
def get_note(id: int):
    note = get_note_by_id(id)
    if not note:
        raise HTTPException(404, "Note not found")
    return note
    
@router.delete("/notes/{id}", status_code=204)
def delete_note(id: int):
    delete_note_service(id)
    return Response(status_code=204)

@router.put("/notes/{id}", response_model=Note, status_code=200)
def update_note(id: int, patch: NoteUpdate):
    return update_note_service(id, patch)   