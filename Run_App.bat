@echo off
echo Starting Interaction Engine...
echo.

:: Change to the directory where the batch file is located
cd /d "%~dp0"

:: Check if the virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found at .venv\Scripts\activate.bat
    echo Please ensure the Python virtual environment is set up.
    pause
    exit /b 1
)

:: Activate virtual environment and run the app
call .venv\Scripts\activate.bat
streamlit run 1_Interaction_Simulator.py

pause
