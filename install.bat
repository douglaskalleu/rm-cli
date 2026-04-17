@echo off
:: ============================================================
:: Instalador do RMC CLI
:: Baixe e execute este arquivo para instalar o RMC CLI
:: ============================================================

echo.
echo  ========================================
echo   RMC CLI - Instalador
echo  ========================================
echo.

:: Definir pasta de instalação
set "INSTALL_DIR=%USERPROFILE%\rmc-cli"

:: Verificar se Python está instalado
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    where py >nul 2>&1
    if %ERRORLEVEL% neq 0 (
        echo [ERRO] Python nao encontrado!
        echo        Instale em: https://www.python.org/downloads/
        echo        Marque "Add Python to PATH" durante a instalacao.
        pause
        exit /b 1
    )
)

echo [1/4] Criando pasta de instalacao: %INSTALL_DIR%
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo [2/4] Baixando arquivos do GitHub...
:: Baixar arquivos principais
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/douglaskalleu/rm-cli/master/rm_cli.py' -OutFile '%INSTALL_DIR%\rm_cli.py'"
if %ERRORLEVEL% neq 0 (
    echo [ERRO] Falha ao baixar rm_cli.py
    pause
    exit /b 1
)

powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/douglaskalleu/rm-cli/master/rmc.bat' -OutFile '%INSTALL_DIR%\rmc.bat'"
if %ERRORLEVEL% neq 0 (
    echo [ERRO] Falha ao baixar rmc.bat
    pause
    exit /b 1
)

echo [3/4] Adicionando ao PATH do usuario...
:: Verificar se já está no PATH
echo %PATH% | findstr /I /C:"%INSTALL_DIR%" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    powershell -Command "[Environment]::SetEnvironmentVariable('Path', [Environment]::GetEnvironmentVariable('Path', 'User') + ';%INSTALL_DIR%', 'User')"
    echo        Adicionado: %INSTALL_DIR%
) else (
    echo        Ja esta no PATH.
)

echo [4/4] Verificando instalacao...
:: Atualizar PATH na sessão atual
set "PATH=%PATH%;%INSTALL_DIR%"

:: Testar
python "%INSTALL_DIR%\rm_cli.py" --help >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo.
    echo  ========================================
    echo   Instalacao concluida com sucesso!
    echo  ========================================
    echo.
    echo  Feche e reabra o terminal, depois:
    echo.
    echo    rmc config --base-path "C:\SuaPasta"
    echo    rmc list
    echo    rmc start host
    echo.
) else (
    echo.
    echo [AVISO] Instalacao concluida, mas nao foi possivel verificar.
    echo         Feche e reabra o terminal e tente: rmc --help
)

pause
