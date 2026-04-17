@echo off
:: Atalho para executar o RM CLI sem precisar digitar "python rm_cli.py"
:: Coloque a pasta deste arquivo no seu PATH do Windows

:: Tenta com 'python' primeiro, depois com 'py'
where python >nul 2>&1
if %ERRORLEVEL% equ 0 (
    python "%~dp0rm_cli.py" %*
) else (
    where py >nul 2>&1
    if %ERRORLEVEL% equ 0 (
        py "%~dp0rm_cli.py" %*
    ) else (
        echo Python nao encontrado. Instale em https://www.python.org/downloads/
        exit /b 1
    )
)
