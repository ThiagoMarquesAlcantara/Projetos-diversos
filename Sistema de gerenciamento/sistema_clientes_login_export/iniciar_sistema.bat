@echo off
echo ========================================
echo   INICIANDO SISTEMA DE CLIENTES (Python 3.12)
echo ========================================

:: Verifica se Python 3.12 está instalado
py -3.12 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Python 3.12 nao encontrado.
    echo Instale em: https://www.python.org/downloads/release/python-3120/
    pause
    exit /b
)

:: Cria ambiente virtual, se nao existir
if not exist venv (
    echo Criando ambiente virtual...
    py -3.12 -m venv venv
)

:: Ativa ambiente virtual
call venv\Scripts\activate

:: Instala dependencias
echo Instalando dependencias...
pip install --upgrade pip
pip install flask flask_sqlalchemy reportlab

:: Inicia o sistema
echo Iniciando servidor Flask...
python app.py

pause
