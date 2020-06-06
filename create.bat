@echo off

set fn=%1
if "%2"=="" (
    set flag=""
) else (
    set flag=%2
)
cd /d %~dp0

if "%1"=="" (
    echo "Error! To use the create function type: create <repo_name> <l, private>"
) else (
    python create.py %fn% %flag%
)
if %errorlevel%==0 (
    exit
) else (
    cd C:\Users\thale
)