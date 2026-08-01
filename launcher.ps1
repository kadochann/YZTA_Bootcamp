<#
.SYNOPSIS
    MediTriag Launcher — starts all services and shuts everything down cleanly on Ctrl+C.

.USAGE
    ./launcher.ps1
#>

$ErrorActionPreference = "Stop"
$ProgressPreference    = "SilentlyContinue"  # suppress progress bars from docker/etc.
$Host.UI.RawUI.WindowTitle = "MediTriag Launcher"
$ROOT = $PSScriptRoot

function Write-Header($msg) {
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "  $msg" -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Ok($msg)    { Write-Host "[OK] $msg"    -ForegroundColor Green  }
function Write-Err($msg)   { Write-Host "[ERROR] $msg" -ForegroundColor Red    }
function Write-Info($msg)  { Write-Host "  >> $msg"    -ForegroundColor Gray   }

# -------------------------------------------------------
# Guard: venv
# -------------------------------------------------------
if (-not (Test-Path "$ROOT\.venv\Scripts\python.exe")) {
    Write-Err "Virtual environment not found. Run: python -m venv .venv"
    exit 1
}
Write-Ok "Virtual environment found."

# -------------------------------------------------------
# Guard: dependencies
# -------------------------------------------------------
Write-Host "Checking required packages..."
$check = & "$ROOT\.venv\Scripts\python.exe" -c `
    "import streamlit, fastapi, uvicorn, langchain, chromadb, google.genai" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Err "Some dependencies are missing. Run: pip install -r requirements.txt"
    exit 1
}
Write-Ok "Dependencies verified."

# -------------------------------------------------------
# Docker / DB
# -------------------------------------------------------
Write-Host ""
Write-Host "Starting PostgreSQL via Docker Compose..."
& docker-compose -f "$ROOT\docker-compose.yml" up -d
if ($LASTEXITCODE -ne 0) {
    Write-Err "docker-compose failed. Is Docker running?"
    exit 1
}

Write-Host "Waiting for database to be ready..."
Start-Sleep -Seconds 5

Write-Host "Applying database migrations..."
& "$ROOT\.venv\Scripts\alembic.exe" --config "$ROOT\alembic.ini" upgrade head
Write-Ok "Migrations applied."

# -------------------------------------------------------
# Start backend (Uvicorn) as a background job
# -------------------------------------------------------
Write-Host ""
Write-Host "Starting FastAPI backend (port 8000)..."
$backendJob = Start-Job -Name "MediTriag-Backend" -ScriptBlock {
    param($root)
    Set-Location "$root\api"
    & "$root\.venv\Scripts\uvicorn.exe" api:app --reload --port 8000 2>&1
} -ArgumentList $ROOT

Start-Sleep -Seconds 3   # give uvicorn time to bind

# -------------------------------------------------------
# Start Streamlit as a background job
# -------------------------------------------------------
Write-Host "Starting Streamlit UI (port 8501)..."
$uiJob = Start-Job -Name "MediTriag-UI" -ScriptBlock {
    param($root)
    Set-Location $root
    & "$root\.venv\Scripts\streamlit.exe" run Ana_Sayfa.py 2>&1
} -ArgumentList $ROOT

# -------------------------------------------------------
# Status
# -------------------------------------------------------
Write-Header "MediTriag started successfully"
Write-Host "  Backend  : http://localhost:8000" -ForegroundColor Yellow
Write-Host "  Docs     : http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "  Frontend : http://localhost:8501" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Press Ctrl+C to stop all services." -ForegroundColor DarkGray
Write-Host ""

# -------------------------------------------------------
# Stream logs from both jobs to this terminal
# -------------------------------------------------------
try {
    while ($true) {
        # Receive-Job can surface stderr from child processes as ErrorRecords.
        # Use SilentlyContinue so uvicorn/streamlit INFO lines don't throw.
        $backendOut = Receive-Job -Job $backendJob -ErrorAction SilentlyContinue
        if ($backendOut) {
            $backendOut | ForEach-Object { Write-Host "[backend] $_" -ForegroundColor DarkGreen }
        }

        $uiOut = Receive-Job -Job $uiJob -ErrorAction SilentlyContinue
        if ($uiOut) {
            $uiOut | ForEach-Object { Write-Host "[ui]      $_" -ForegroundColor DarkBlue }
        }

        # Alert if a job died unexpectedly
        if ($backendJob.State -eq 'Failed') {
            Write-Err "Backend job crashed! Check output above. Exiting..."
            break
        }
        if ($uiJob.State -eq 'Failed') {
            Write-Err "UI job crashed! Check output above. Exiting..."
            break
        }

        Start-Sleep -Milliseconds 500
    }
}
finally {
    # -------------------------------------------------------
    # Cleanup — always runs on Ctrl+C or any exit
    # -------------------------------------------------------
    Write-Host ""
    Write-Host "Shutting down MediTriag..." -ForegroundColor Yellow

    Write-Info "Stopping backend..."
    Stop-Job  -Job $backendJob -ErrorAction SilentlyContinue
    Remove-Job -Job $backendJob -Force -ErrorAction SilentlyContinue

    Write-Info "Stopping Streamlit UI..."
    Stop-Job  -Job $uiJob -ErrorAction SilentlyContinue
    Remove-Job -Job $uiJob -Force -ErrorAction SilentlyContinue

    Write-Info "Stopping Docker containers..."
    & docker-compose -f "$ROOT\docker-compose.yml" stop

    Write-Host ""
    Write-Ok "All services stopped. Goodbye!"
    Write-Host ""
}
