# run.ps1 - Quick start script for the backend
# Uses the pre-installed virtualenv directly (avoids re-installing)

$VENV = "C:\Users\user\AppData\Local\pypoetry\Cache\virtualenvs\decision-intelligence-system-1NEqVvNu-py3.14"
$PYTHON = "$VENV\Scripts\python.exe"

# Disable LangChain/LangSmith background tracing (prevents startup hangs)
$env:LANGCHAIN_TRACING_V2 = "false"
$env:LANGCHAIN_CALLBACKS_BACKGROUND = "false"

Write-Host "🚀 Starting Decision Intelligence API..." -ForegroundColor Cyan
Write-Host "   API:     http://localhost:8000" -ForegroundColor Green
Write-Host "   Swagger: http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""

& $PYTHON -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
