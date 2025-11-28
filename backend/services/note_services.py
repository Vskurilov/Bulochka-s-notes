import json, os
import time

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from models.note_models import NoteCreate, NoteUpdate

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "notes.json")

def load_notes():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_notes(notes):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=4)
        
def get_note_by_id(id: int):
    notes = load_notes()
    return next((n for n in notes if n["id"] == id), None)

def filter_notes_by_tags(notes, tags):
    if not tags:
        return notes
    return [
        n for n in notes
        if any(t in n.get("tags", []) for t in tags)
    ]
    

def update_note_service(id: int, patch: NoteUpdate):
    notes = load_notes()
    note = next((n for n in notes if n["id"] == id), None)

    if not note:
        raise HTTPException(404, "Note not found")

    if patch.title is not None:
        note["title"] = patch.title
    if patch.body is not None:
        note["body"] = patch.body
    if patch.tags is not None:
        note["tags"] = patch.tags

    save_notes(notes)
    return note

def create_note(note: NoteCreate ):
    if note.tags is None:
        note.tags = []
        
    new_note = {
        "id": int(round(time.time() * 1000)),
        "title": note.title,
        "body": note.body,
        "tags": note.tags
    }
    
    notes = load_notes()
    notes.append(new_note)
    save_notes(notes)
    
    return new_note

def delete_note_service(id: int):
    notes = load_notes()
    note = next((n for n in notes if n["id"] == id), None)

    if not note:
        raise HTTPException(404, "Note not found")

    notes.remove(note)
    save_notes(notes)
    