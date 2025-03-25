@echo off
echo 正在启动conda环境...

call "C:\ProgramData\Anaconda3\Scripts\activate.bat"

call conda activate pytorch-gpu

echo 正在启动项目后端...

start python "../app/static/api.py"
timeout /t 5 >nul

cd "../app/pipeline/ppt_pipeline/PPTist-master"
start npm run dev
timeout /t 5 >nul

pause