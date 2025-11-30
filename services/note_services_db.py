from typing import List, Sequence, Optional
from sqlalchemy.orm import Session

from models.note_model_sql import Note as NoteORM, Tag
from models.note_models import NoteCreate, NoteUpdate, Note as NoteSchema


def orm_note_to_schema(note: NoteORM) -> NoteSchema:
    return NoteSchema(
        id=note.id,
        title=note.title,
        body=note.body,
        tags=[t.name for t in note.tags]
    )


def create_note_services(db: Session, title: str, body: str, tag_names: list[str]):
    note = NoteORM(title=title, body=body)
    # создаём ORM-объект NoteORM (пока только в памяти, ещё не сохранён в базе)
    
    tags = get_or_create_tags(db, tag_names or [])
    # получаем список ORM-объектов Tag:
    # существующие берём из базы, отсутствующие — создаём и добавляем в сессию
    
    note.tags = tags
    # привязываем теги к заметке (many-to-many связь через secondary-таблицу)
    
    db.add(note)
    # добавляем заметку в сессию (готовим к сохранению в базе)
    
    db.commit()
    # фиксируем все изменения в базе: создаётся note, при необходимости новые tag и связи
    
    db.refresh(note)
    # обновляем объект note из базы (подтягиваем сгенерированный id и актуальное состояние)
    
    return note


def get_or_create_tags(db: Session, tag_names: Sequence[str]) -> List[Tag]:
    # Возвращает список ORM-объектов Tag, при необходимости создавая новые
    
    tags: List[Tag] = []
    # создаём пустой список, куда будем складывать найденные/созданные теги
    
    for name in tag_names:
        name = name.strip()
        if not name:
            continue
        # убираем пробелы по краям и пропускаем пустые строки
        
        tag = db.query(Tag).filter(Tag.name == name).first()
        # ищем тег в базе по имени
        
        if not tag:
            tag = Tag(name=name)
            db.add(tag)
        # если такого тега нет — создаём ORM-объект Tag и добавляем его в сессию
        
        tags.append(tag)
        # добавляем тег (найденный или новый) в итоговый список
    
    return tags
    # возвращаем список тегов


def create_note_from_schema(db: Session, note_in: NoteCreate) -> NoteORM:
    # функция создаёт заметку из Pydantic-схемы и сохраняет её в базе
    note = NoteORM(title=note_in.title, body=note_in.body)
    # создаём ORM-объект NoteORM на основе данных из NoteCreate
    
    tags = get_or_create_tags(db, note_in.tags or [])
    # получаем список тегов (существующие из базы + новые при необходимости)
    
    note.tags = tags
    # устанавливаем связи между заметкой и тегами (many-to-many)
    
    db.add(note)
    # добавляем note в сессию базы данных
    
    db.commit()
    # фиксируем изменения в базе (note + новые теги + связи)
    
    db.refresh(note)
    # обновляем объект note из базы (получаем id и актуальное состояние)
    
    return note


def get_note_by_id_service(db: Session, note_id: int) -> Optional[NoteORM]:
    # получаем note по id
    # возвращаем первую найденную заметку, у которой NoteORM.id совпадает с note_id
    return db.query(NoteORM).filter(NoteORM.id == note_id).first()


def filter_notes_by_tags_service(
    db: Session,
    tags_names: Optional[List[str]] = None,
) -> List[NoteORM]:
    # функция возвращает список заметок, при необходимости отфильтрованный по тегам
    
    query = db.query(NoteORM)
    # создаём запрос к таблице заметок (пока без фильтров)
    
    if tags_names:
        query = (
            query
            .join(NoteORM.tags)                 # JOIN c таблицей тегов через связь tags
            .filter(Tag.name.in_(tags_names))  # оставляем заметки, у которых есть хотя бы один из указанных тегов
            .distinct()                      # убираем дубли заметок, если несколько тегов совпали
        )
        # если теги переданы — фильтруем запрос по именам тегов
    
    return query.all()
    # выполняем запрос и получаем список объектов NoteORM


def update_note_service(
    db: Session,
    note_id: int,
    patch: NoteUpdate
) -> Optional[NoteORM]:
    # функция обновления заметки в базе данных
    
    note: Optional[NoteORM] = (
        db.query(NoteORM)
        .filter(NoteORM.id == note_id)
        .first()
    )
    # ищем существующую заметку по её id
    
    if not note:
        return None
    # если заметка не найдена — возвращаем None
    
    if patch.title is not None:
        note.title = patch.title
    # если новое значение title передано — обновляем его
    
    if patch.body is not None:
        note.body = patch.body
    # если новое значение body передано — обновляем его
    
    if patch.tags is not None:
        tags = get_or_create_tags(db, patch.tags)
        note.tags = tags
    # если передан список тегов — получаем/создаём теги и переустанавливаем связи
    
    db.commit()
    # фиксируем изменения в базе (обновлённые поля и связи)
    
    db.refresh(note)
    # обновляем объект note из базы (получаем актуальное состояние)
    
    return note


def delete_note_service(db: Session, note_id: int) -> Optional[NoteORM]:
    # удаление заметки по id 
    
    note: Optional[NoteORM] = (
        db.query(NoteORM)
        .filter(NoteORM.id == note_id)
        .first()
    )
    # ищем заметку по её id
    
    if not note:
        return None
    # если не нашли — ничего не удаляем, возвращаем None
    
    db.delete(note)
    # помечаем заметку как удалённую в сессии
    
    db.commit()
    # фиксируем удаление в базе данных
    
    return note
    # возвращаем удалённую заметку (её объект всё ещё существует в памяти)
