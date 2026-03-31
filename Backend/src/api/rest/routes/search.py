from fastapi import APIRouter, Query
from handlers.search.search_service import search_videos

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/")
def search(query: str = Query(...)):
    return search_videos(query)