from fastapi import FastAPI
from routers.note_routers import router as note_router
from database import Base, engine
from models.note_model_sql import Tag, Note

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(note_router)
