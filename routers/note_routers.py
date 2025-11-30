from typing import List
from fastapi import APIRouter, HTTPException, Query, Response, Depends

from sqlalchemy.orm import Session

from database import get_db

from models.note_models import Note as NoteSchema, NoteCreate, NoteUpdate


from services.note_services_db import (
    create_note_services,
    delete_note_service,
    create_note_from_schema,
    filter_notes_by_tags_service,
    get_note_by_id_service,    
    orm_note_to_schema,
    update_note_service)

router = APIRouter()

@router.get("/")
def read_root():
    return {"answer": "Hello World" }


@router.post("/notes", response_model=NoteSchema, status_code=201)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    # note — объект Pydantic-модели NoteCreate с данными из тела запроса
    created = create_note_from_schema(db, note)
    # вызываем сервис создания заметки, передавая title, body и список тегов (если tags = None — используем пустой список)
    return orm_note_to_schema(created)
    
@router.get("/notes", response_model=List[NoteSchema])
def get_notes(
    tags: list[str] = Query(default_factory=list),
    db: Session = Depends(get_db)
    ):
    # если список пустой -> передаём None, сервис вернёт все заметки
    notes_orm = filter_notes_by_tags_service(db, tags or None)
    return [orm_note_to_schema(n) for n in notes_orm]      

@router.get("/notes/{id}", response_model=NoteSchema)
def get_note(id: int, db: Session = Depends(get_db)):
    # id — path-параметр, db — SQLAlchemy Session
    note = get_note_by_id_service(db, id)
    # получаем заметку из базы
    
    if not note:
        raise HTTPException(404, "Note not found")
    # если заметка не найдена — 404
    
    return orm_note_to_schema(note)
    # преобразуем ORM → Pydantic перед отдачей клиенту
    
@router.delete("/notes/{id}", status_code=204)
def delete_note(id: int, db: Session = Depends(get_db)):
    # id — это path-параметр, подставляемый в {id} из URL.
    # db — это зависимость, FastAPI вызывает get_db() и передаёт сюда объект Session.
    deleted_note = delete_note_service(db, id)
    # вызываем сервис удаления. Если заметки нет — вернётся None.
    if deleted_note is None:
        raise HTTPException(404, "Note not found")
    return Response(status_code=204)
    # если заметка не найдена — возвращаем 404, иначе отдаём пустой ответ с кодом 204

@router.put("/notes/{id}", response_model=NoteSchema, status_code=200)
def update_note(
    id: int,
    patch: NoteUpdate,
    db: Session = Depends(get_db),
):
    # id — path-параметр, patch — данные для обновления, db — сессия БД
    note = update_note_service(db, id, patch)
    # вызываем сервис обновления заметки

    if note is None:
        raise HTTPException(404, "Note not found")
    # если заметка не найдена — отдаём 404

    return orm_note_to_schema(note)
    # конвертируем ORM-объект в Pydantic-схему и возвращаем клиенту
