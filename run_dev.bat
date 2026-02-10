@echo off
REM Inicia el servidor de desarrollo usando el venv local
if not exist venv\Scripts\python.exe (
  echo Virtualenv not found. Run: python -m venv venv
  exit /b 1
)
venv\Scripts\python.exe run.py
