@echo off
setlocal enabledelayedexpansion

:: Check if any arguments were passed
if "%~1"=="" (
    echo ❌ Please provide a commit message.
    echo Usage: gpush "Your commit message here"
    exit /b 1
)

:: Reconstruct full message
set "message=%~1"
shift
:loop
if not "%~1"=="" (
    set "message=!message! %~1"
    shift
    goto loop
)

git add .
git commit -m "!message!"
git push -u origin master
