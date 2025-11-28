from typing import Optional, List
from pydantic import BaseModel


class Note(BaseModel):
    id: int
    title: str
    body: str
    tags: List[str]

class NoteCreate(BaseModel):
    title: str
    body: str
    tags: Optional[List[str]] = None

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    tags: Optional[List[str]] = None