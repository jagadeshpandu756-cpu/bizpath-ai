@echo off
cd /d "C:\Users\jagad\OneDrive\Desktop\bizpath-ai\backend"
call venv\Scripts\activate.bat
start cmd /k "cd /d C:\Users\jagad\OneDrive\Desktop\bizpath-ai\backend && venv\Scripts\activate && uvicorn main:app --reload --port 8000"
timeout /t 4 /nobreak
start "" "http://127.0.0.1:8000"