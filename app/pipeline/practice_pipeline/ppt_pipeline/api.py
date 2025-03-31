from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from datetime import datetime
import logging
from pydantic import BaseModel
from utils import *

logging.basicConfig(
    level=logging.INFO,  # info level
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

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

SAVE_DIR = "./upload_pptxs"
MD_SAVE_DIR = "./mds"

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)
if not os.path.exists(MD_SAVE_DIR):
    os.makedirs(MD_SAVE_DIR)


class GenerateQuestion(BaseModel):
    scq_num: int
    mcq_num: int
    tof_num: int
    sa_num: int
    pptx_filename: str


@app.post("/practice/upload/ppt")
async def upload_file(file: UploadFile = File(...)):
    try:
        logging.info(f"开始处理上传文件: {file.filename}")

        if not file.filename.endswith(".pptx"):
            logging.warning(f"上传的文件不是 pptx 格式: {file.filename}")
            raise HTTPException(status_code=400, detail="Not a pptx file")

        contents = await file.read()
        logging.info(f"成功读取文件内容: {file.filename}")

        filename = file.filename.replace(".pptx", "") + datetime.now().strftime("%Y%m%d%H%M%S") + ".pptx"
        file_location = os.path.join(SAVE_DIR, filename)

        with open(file_location, "wb") as f:
            f.write(contents)
        logging.info(f"文件已保存到: {file_location}")

        return JSONResponse(content={"filename": filename}, status_code=200)
    except Exception as e:
        logging.error(f"处理文件上传时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/practice/ppt/generate")
def generate_questions(generate_question: GenerateQuestion):
    try:
        scq_num = generate_question.scq_num
        mcq_num = generate_question.mcq_num
        tof_num = generate_question.tof_num
        sa_num = generate_question.sa_num
        pptx_filename = generate_question.pptx_filename

        logging.info(f"开始生成练习题，PPTX 文件: {pptx_filename}")

        ppt_filepath = os.path.join(SAVE_DIR, pptx_filename)
        md_filepath = os.path.join(MD_SAVE_DIR, pptx_filename.replace(".pptx", ".md"))

        if not os.path.exists(ppt_filepath):
            logging.error(f"PPT 文件不存在: {ppt_filepath}")
            raise HTTPException(status_code=404, detail="PPT file not found")

        logging.info(f"开始转换 PPTX 文件为 Markdown: {ppt_filepath}")
        pptx_convert(ppt_filepath, md_filepath)
        logging.info(f"Markdown 文件已生成: {md_filepath}")

        logging.info(f"开始生成练习题，参数: SCQ={scq_num}, MCQ={mcq_num}, TOF={tof_num}, SA={sa_num}")
        question = generate_practice(md_filepath, scq_num, mcq_num, tof_num, sa_num)
        # question = question.replace("```json", "").replace("```", "")
        logging.info(f"练习题生成成功")

        return JSONResponse(content=question, status_code=200)
    except Exception as e:
        logging.error(f"生成练习题时发生错误: {str(e)}")
        raise HTTPException(status_code=501, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    logging.info("启动PPT-practice应用")
    uvicorn.run(app, host="0.0.0.0", port=8001)