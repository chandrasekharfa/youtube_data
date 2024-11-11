from fastapi import FastAPI
from youtube_info import get_youtube_video_info

app = FastAPI()

@app.get("/youtube-info/")
async def youtube_info(url: str):
    return await get_youtube_video_info(url)
