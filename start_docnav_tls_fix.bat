@echo off
setlocal

REM Tries to fix DocNav "TLS initialization failed" by providing a CA bundle for OpenSSL.

set "DOCNAV_EXE=C:\Xilinx\DocNav\docnav.exe"

REM Prefer Git for Windows CA bundle if present
set "CA_GIT=C:\Program Files\Git\mingw64\etc\ssl\certs\ca-bundle.crt"
REM Fallback: certifi bundle (example: FreeCAD)
set "CA_CERTIFI=C:\Program Files\FreeCAD 1.0\bin\Lib\site-packages\certifi\cacert.pem"

if exist "%CA_GIT%" (
  set "SSL_CERT_FILE=%CA_GIT%"
) else if exist "%CA_CERTIFI%" (
  set "SSL_CERT_FILE=%CA_CERTIFI%"
) else (
  echo ERROR: No CA bundle found. Install Git for Windows or provide a cacert.pem.
  pause
  exit /b 1
)

REM Avoid broken global OpenSSL config paths (if any)
set "OPENSSL_CONF="
set "SSL_CERT_DIR="

REM Optional: ensure we don't inherit proxy env vars unintentionally
REM set "HTTPS_PROXY="
REM set "HTTP_PROXY="
REM set "NO_PROXY="

if not exist "%DOCNAV_EXE%" (
  echo ERROR: DocNav not found at: %DOCNAV_EXE%
  pause
  exit /b 1
)

start "DocNav" "%DOCNAV_EXE%"
endlocal
