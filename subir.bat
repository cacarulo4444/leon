@echo off
:: Reemplaza 'leon' por el nombre de la carpeta de tu proyecto si es distinto
cd /d "%~dp0"

:: Verificamos si existe la carpeta .git para no tirar error
if not exist .git (
    echo [ERROR] No encontre la carpeta .git. 
    echo Asegurate de que este archivo este en la raiz del proyecto.
    pause
    exit
)

git add .
set /p msg="Mensaje del commit: "
git commit -m "%msg%"
git push origin main
echo.
echo --- PROCESO TERMINADO ---
pause