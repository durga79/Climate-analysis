@echo off
SETLOCAL EnableExtensions EnableDelayedExpansion

REM ============================================================================
REM CLIMATE ANALYTICS PIPELINE - WINDOWS LAUNCHER
REM ============================================================================

ECHO ============================================================================
ECHO CLIMATE ANALYTICS & ECONOMIC DEVELOPMENT PROJECT
ECHO ============================================================================
ECHO.

REM Check if Python is installed
python --version >NUL 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO ERROR: Python is not found in your PATH.
    ECHO Please install Python 3.10+ and add it to your PATH.
    PAUSE
    EXIT /B 1
)

REM Set PYTHONPATH to current directory to allow imports
SET PYTHONPATH=%CD%

ECHO [1/5] Checking environment...
IF NOT EXIST "src\data_acquisition\fetch_all_datasets.py" (
    ECHO ERROR: specific files not found. Please run this from the project root.
    PAUSE
    EXIT /B 1
)

ECHO.
ECHO [2/5] Running Data Acquisition...
python src/data_acquisition/fetch_all_datasets.py
IF %ERRORLEVEL% NEQ 0 (
    ECHO ERROR: Data Acquisition failed.
    PAUSE
    EXIT /B 1
)

ECHO.
ECHO [3/5] Running ETL Pipeline (Extract-Transform-Load)...
python src/etl/pipeline.py
IF %ERRORLEVEL% NEQ 0 (
    ECHO ERROR: ETL Pipeline failed.
    PAUSE
    EXIT /B 1
)

ECHO.
ECHO [4/5] Running Statistical & ML Analysis...
python src/analysis/run_analysis.py
IF %ERRORLEVEL% NEQ 0 (
    ECHO ERROR: Analysis failed.
    PAUSE
    EXIT /B 1
)

ECHO.
ECHO [5/5] Launching Dashboard...
ECHO The dashboard will open in your default browser at http://127.0.0.1:8050
ECHO Press Ctrl+C in this window to stop the server.
ECHO.
python dashboard/app.py

ENDLOCAL

