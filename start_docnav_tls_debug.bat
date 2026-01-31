@echo off
setlocal

REM Force a known CA bundle (Git for Windows)
set "SSL_CERT_FILE=C:\Program Files\Git\mingw64\etc\ssl\certs\ca-bundle.crt"
set "SSL_CERT_DIR="
set "OPENSSL_CONF="

REM Qt debug (may or may not emit output depending on build)
set "QT_DEBUG_PLUGINS=1"
set "QT_LOGGING_RULES=qt.network.ssl.warning=true;qt.network.ssl.info=true;qt.network.warning=true"

set "LOG=%TEMP%\docnav_tls_debug.log"
echo ===== DocNav TLS debug ===== > "%LOG%"
echo DATE=%DATE% TIME=%TIME% >> "%LOG%"
echo SSL_CERT_FILE=%SSL_CERT_FILE% >> "%LOG%"
echo. >> "%LOG%"

REM /WAIT keeps the console attached until exit
start "DocNav" /wait "C:\Xilinx\DocNav\docnav.exe" >> "%LOG%" 2>&1

echo. >> "%LOG%"
echo ===== DocNav exited (code %ERRORLEVEL%) ===== >> "%LOG%"
echo Log written to: %LOG%
endlocal
