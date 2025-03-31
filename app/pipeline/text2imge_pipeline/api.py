from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import os
from text2image import main, parser_Message

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

IMAGE_DIR = "./generated_images"
os.makedirs(IMAGE_DIR, exist_ok=True)

APPID = 'a597c611'
APISecret = 'N2NiMDYxZWRlODRhNTcxYTcyMGM2ZTRi'
APIKEY = '9df07f763ae0823e414dd9e44e1b69b7'


class Describe(BaseModel):
    text: str


@app.post("/image/generate")
async def generate_image(desc: Describe):
    text = desc.text

    image_name = f"{uuid.uuid4()}.jpg"
    image_path = os.path.join(IMAGE_DIR, image_name)

    res = main(text, appid=APPID, apikey=APIKEY, apisecret=APISecret)
    parser_Message(res, image_path)

    image_url = f"http://localhost:8002/generated_images/{image_name}"
    return JSONResponse(content={"image_url": image_url})

from fastapi.staticfiles import StaticFiles
app.mount("/generated_images", StaticFiles(directory=IMAGE_DIR), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8002)