@echo off
title MOBA AI

cd /d "D:\Moba-Project\Moba"

start "MOBA AI Server" cmd /k ""D:\Moba-Project\venv\Scripts\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000"

timeout /t 5 /nobreak >nul

start "" "http://127.0.0.1:8000"