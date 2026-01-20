@echo off
REM ============================================================================
REM Vivado FPGA Expert - MCP Server Başlatma Scripti
REM ============================================================================

echo.
echo ================================================================================
echo    Vivado FPGA Expert - MCP Server
echo ================================================================================
echo.

cd /d "%~dp0"
cd ai_assistant

echo [1/3] Python ortami kontrol ediliyor...
python --version
if errorlevel 1 (
    echo HATA: Python bulunamadi!
    pause
    exit /b 1
)

echo.
echo [2/3] Gerekli paketler kontrol ediliyor...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Flask yukleniyor...
    pip install flask flask-cors
)

echo.
echo [3/3] MCP Server baslatiliyor...
echo.
echo Server adresi: http://localhost:5000
echo VS Code'da @vivado ile kullanabilirsiniz.
echo.
echo Server'i durdurmak icin Ctrl+C basin.
echo.
echo ================================================================================
echo.

python vivado_mcp_server.py

pause
