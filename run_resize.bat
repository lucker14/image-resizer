@echo off
REM This batch file creates and uses a local virtual environment (.venv)
REM so the tool works consistently on Windows without polluting global Python.

SETLOCAL ENABLEDELAYEDEXPANSION
SET SCRIPT_DIR=%~dp0
SET VENV_DIR=%SCRIPT_DIR%.venv
SET SOURCE_DIR="/Volumes/NO NAME/Vybrané"
SET MAX_SIDE=800
SET FONT_SIZE=48
SET WATERMARK_TEXT=Nabídka pro redakci
SET WATERMARK_OPACITY=30
nREM Create venv if missing
IF NOT EXIST "%VENV_DIR%\Scripts\python.exe" (
    echo Creating virtual environment at %VENV_DIR%
    python -m venv "%VENV_DIR%"
)
nREM Use venv python to install dependencies and run the script
SET PYTHON=%VENV_DIR%\Scripts\python.exe
"%PYTHON%" -m pip install --upgrade pip
"%PYTHON%" -m pip install -r "%SCRIPT_DIR%requirements.txt"
n"%PYTHON%" "%SCRIPT_DIR%resize_watermark.py" --source-dir %SOURCE_DIR% --max-side %MAX_SIDE% --font-size %FONT_SIZE% --watermark-text "%WATERMARK_TEXT%" --watermark-opacity-percent %WATERMARK_OPACITY% %*
nENDLOCAL
