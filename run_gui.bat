@echo off
cd /d "%~dp0"
py -3 mogul_app.py 2>nul || python mogul_app.py
if errorlevel 1 pause
