from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import subprocess
import uuid
import os

app = FastAPI()

class ClipRequest(BaseModel):
    url: str
    start: str  # format: HH:MM:SS
    end: str    # format: HH:MM:SS

@app.post("/clip")
async def clip_video(data: ClipRequest):
    clip_id = str(uuid.uuid4())[:8]
    output_file = f"{clip_id}.mp4"
    duration = calculate_duration(data.start, data.end)

    cmd = [
        "yt-dlp",
        "-f", "bestvideo[height<=1080]+bestaudio",
        data.url,
        "--external-downloader", "ffmpeg",
        "--external-downloader-args", f"ffmpeg_i:-ss {data.start} -t {duration}",
        "-o", output_file
    ]

    try:
        subprocess.run(cmd, check=True)
        return {"file": f"/download/{output_file}"}
    except subprocess.CalledProcessError as e:
        return JSONResponse(content={"error": "Download failed", "details": str(e)}, status_code=500)

@app.get("/download/{filename}")
async def get_clip(filename: str):
    file_path = os.path.join(".", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="video/mp4", filename=filename)
    return JSONResponse(content={"error": "File not found"}, status_code=404)

def calculate_duration(start: str, end: str) -> str:
    from datetime import datetime
    fmt = '%H:%M:%S'
    duration = datetime.strptime(end, fmt) - datetime.strptime(start, fmt)
    return str(duration)
