from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='app.log',
                    filemode='a')

logger = logging.getLogger()

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

#   跨域支持
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SAVE_DIR = "./upload_pptxs"

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)


@app.post("/practice/upload/ppt")
async def upload_file(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith(".pptx"):
            raise HTTPException(status_code=400, detail="Not a pptx file")

        contents = await file.read()

        file_location = os.path.join(SAVE_DIR, file.filename)
        with open(file_location, "wb") as f:
            f.write(contents)

        logger.info(f"File saved at {file_location}")

        return JSONResponse(content={"filename": file.filename}, status_code=200)
    except Exception as e:
        logger.error(f"Failed to upload file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)