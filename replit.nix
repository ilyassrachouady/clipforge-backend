{ pkgs }: {
  deps = [
    pkgs.python310
    pkgs.ffmpeg
    pkgs.yt-dlp
    pkgs.python310Packages.uvicorn
    pkgs.python310Packages.fastapi
    pkgs.python310Packages.pydantic
  ];
}
