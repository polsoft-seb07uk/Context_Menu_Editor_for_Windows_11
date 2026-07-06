@echo off
:: ============================================================================
:: Skrypt uruchomieniowy dla: Edytor Menu Kontekstowego Windows 11
::
:: METADANE PROJEKTU:
:: Autor:       Sebastian Januchowski
:: Firma/Grupa: polsoft.ITS™ Group
:: Repozytorium: https://github.com/polsoft-seb07uk
:: Kontakt:     polsoft.its@mail.com
:: Wersja:      1.0.0 (2026)
:: ============================================================================
chcp 65001 >nul
title Uruchamianie: Edytor Menu Kontekstowego

:: Sprawdzenie uprawnień administratora (wymagane do pełnej modyfikacji HKLM/HKCR)
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :init
) else (
    goto :uac_bypass
)

:uac_bypass
echo [INFO] Brak uprawnień administratora. Podnoszenie uprawnień...
powershell -Command "Start-Process -FilePath '%0' -Verb RunAs"
exit /b

:init
cls
echo ============================================================================
echo  Edytor Menu Kontekstowego - polsoft.ITS™ Group
echo  Autor: Sebastian Januchowski
echo ============================================================================
echo.

:: Przejście do katalogu roboczego, w którym znajduje się plik bat
cd /d "%~dp0"

:: Sprawdzenie czy Python jest zainstalowany w systemie
where python >nul 2>&1
if %errorLevel% neq 0 (
    echo [BŁĄD] Python nie jest zainstalowany lub nie został dodany do zmiennej PATH.
    echo Pobierz Pythona z oficjalnej strony lub Microsoft Store.
    echo.
    pause
    exit /b
)

:: Uruchomienie aplikacji w tle (pythonw ukrywa czarne okno konsoli CMD)
echo [OK] Uruchamianie aplikacji ContextMenuEditor...
start "" pythonw "context_menu_editor.py"

exit /b