# System Information Collector - PowerShell Launcher
# Run this script to generate comprehensive hardware and software reports

$Host.UI.RawUI.WindowTitle = "System Information Collector"

Write-Host ""
Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host "                 SYSTEM INFORMATION COLLECTOR" -ForegroundColor Green
Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This tool will generate comprehensive hardware and software reports" -ForegroundColor Yellow
Write-Host "for your computer. This may take a few moments..." -ForegroundColor Yellow
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Check and install required packages
Write-Host "Checking required packages..." -ForegroundColor Cyan
Write-Host ""

$packages = @("psutil", "WMI")

foreach ($package in $packages) {
    python -c "import $package" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Installing $package..." -ForegroundColor Yellow
        pip install $package
        Write-Host ""
    } else {
        Write-Host "✓ $package is already installed" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Starting system scan..." -ForegroundColor Cyan
Write-Host ""

# Run the Python script
$scriptPath = Join-Path $PSScriptRoot "system_info_collector.py"
python $scriptPath

# Check if reports were generated successfully
if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Reports generated successfully!" -ForegroundColor Green
    Write-Host "Opening reports folder..." -ForegroundColor Cyan
    
    $reportsPath = Join-Path $PSScriptRoot "Reports"
    if (Test-Path $reportsPath) {
        Start-Process explorer.exe -ArgumentList $reportsPath
    }
}

Write-Host ""
Read-Host "Press Enter to exit"
