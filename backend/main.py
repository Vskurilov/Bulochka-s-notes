from fastapi import FastAPI
from routers.note_routers import router as note_router

app = FastAPI()

app.include_router(note_router)
