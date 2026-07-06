@echo off
echo ================================================
echo Office Call Notification System - HTTPS Starter
echo ================================================

echo.
echo 1. Generating self-signed certificate (PowerShell)...
powershell -ExecutionPolicy Bypass -File create_cert.ps1

echo.
echo 2. Starting FastAPI Backend with HTTPS...
python main.py

pause