from fastapi import FastAPI, HTTPException, Path
from fastapi.responses import FileResponse
import mimetypes
import os

app = FastAPI()

IMAGE_DIR = "./imgs"


@app.get("/imgs/{image_name}")
async def get_frontend_imgs(image_name: str = Path(...)):
    image_path = os.path.join(IMAGE_DIR, image_name)

    if os.path.exists(image_path):
        media_type = mimetypes.guess_type(image_path)[0]
        return FileResponse(image_path, media_type=media_type)
    else:
        raise HTTPException(status_code=404, detail="Image not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)