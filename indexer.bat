@echo off
REM Windows launcher for the CS172 search index builder (Part B).
REM
REM Usage:
REM     indexer.bat [--crawl-dir DIR] [--metadata CSV] [--index-dir DIR]
REM
REM Defaults:
REM     --crawl-dir  crawled_pages
REM     --metadata   crawled_pages/metadata.csv
REM     --index-dir  index/lucene_index
REM
REM Example:
REM     indexer.bat
REM     indexer.bat --crawl-dir crawled_pages --index-dir index/lucene_index

setlocal

where python >nul 2>nul
if errorlevel 1 (
    set PYTHON=py
) else (
    set PYTHON=python
)

%PYTHON% "%~dp0indexer\build_index.py" %*
exit /b %ERRORLEVEL%
