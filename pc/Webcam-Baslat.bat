@echo off
chcp 65001 >nul
title USB/WiFi Webcam
cd /d "%~dp0"
echo ============================================
echo   Telefon Webcam - Hibrit (USB + WiFi)
echo   Kapatmak icin bu pencerede Ctrl+C
echo ============================================
".venv\Scripts\python.exe" run.py %*
echo.
echo Yayin durdu. Kapatmak icin bir tusa bas...
pause >nul
