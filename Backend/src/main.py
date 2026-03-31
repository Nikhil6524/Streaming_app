from fastapi import FastAPI
from api.rest.routes.auth import router as auth_router

from data.clients.postgres_client import engine
from data.models.postgres.user_model import Base
from api.rest.routes.user import router as user_router
from fastapi.middleware.cors import CORSMiddleware
from api.rest.routes.upload import router as upload_router
from api.rest.routes.video import router as video_router
from api.rest.routes.chunk_upload import router as chunk_router
from api.rest.routes.search import router as search_router


app = FastAPI()


app.include_router(search_router)
app.include_router(video_router)
app.include_router(upload_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(chunk_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Server running"}

# TEMP: create tables
Base.metadata.create_all(bind=engine)