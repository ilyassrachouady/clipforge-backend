from fastapi import FastAPI, Request
from pydantic import BaseModel
import subprocess
import uuid
import os

app = FastAPI()

class ClipRequest(BaseModel):
    url: str
    start: str  # e.g., "00:01:10"
    end: str    # e.g., "00:02:00"
    quality: str = "bestvideo[height<=2160]+bestaudio"

@app.post("/clip")
async def create_clip(data: ClipRequest):
    clip_id = str(uuid.uuid4())[:8]
    output_file = f"{clip_id}.mp4"

    command = [
        "yt-dlp",
        "-f", data.quality,
        "--external-downloader", "ffmpeg",
        "--external-downloader-args",
        f"ffmpeg_i:-ss {data.start} -to {data.end}",
        "-o", output_file,
        data.url
    ]

    try:
        subprocess.run(command, check=True)
        return {
            "status": "success",
            "file": f"/files/{output_file}"
        }
    except subprocess.CalledProcessError:
        return {"status": "error", "message": "Download failed"}

@app.get("/files/{file_name}")
async def get_file(file_name: str):
    file_path = os.path.join(".", file_name)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="video/mp4", filename=file_name)
    return {"error": "File not found"}
