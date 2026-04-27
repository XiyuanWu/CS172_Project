@echo off
REM Windows launcher for the CS172 web crawler (Part A).
REM
REM Usage:
REM     crawler.bat ^<seed-file^> ^<num-pages^> ^<hops-away^> ^<output-dir^>
REM
REM Example:
REM     crawler.bat seed.txt 10000 6 crawled_pages
REM
REM You can also pass extra flags through to main.py, e.g.:
REM     crawler.bat seed.txt 10000 6 crawled_pages --allowed-domain ucr.edu -v

setlocal

if "%~4"=="" (
    echo Usage: %~nx0 ^<seed-file^> ^<num-pages^> ^<hops-away^> ^<output-dir^> [extra args]
    exit /b 1
)

set SEED=%~1
set NPAGES=%~2
set HOPS=%~3
set OUTDIR=%~4
shift & shift & shift & shift

where python >nul 2>nul
if errorlevel 1 (
    set PYTHON=py
) else (
    set PYTHON=python
)

%PYTHON% "%~dp0main.py" --seed-file "%SEED%" --max-pages %NPAGES% --max-hops %HOPS% --output-dir "%OUTDIR%" %*
exit /b %ERRORLEVEL%
