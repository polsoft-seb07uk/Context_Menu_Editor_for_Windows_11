# -*- coding: utf-8 -*-
"""
Runtime hook PyInstaller (uruchamiany PRZED context_menu_editor.py).

Aplikacja wczytuje ikonę okna przez tkinter (self.iconbitmap("ico.ico")),
sprawdzając WZGLĘDNĄ ścieżkę do pliku "ico.ico" w bieżącym katalogu roboczym.

Plik ico.ico jest OSADZONY WEWNĄTRZ pojedynczego pliku .exe (parametr
icon='ico.ico' w spec osadza go jako zasób Win32 dla samego EXE, a wpis
w datas=[('ico.ico', '.')] osadza jego kopię wewnątrz archiwum onefile).
Bootloader PyInstallera onefile rozpakowuje ją wyłącznie do WEWNĘTRZNEGO,
tymczasowego katalogu roboczego (sys._MEIPASS) - NIGDY do folderu, w którym
leży sam plik .exe.

Ten hook jedynie przełącza katalog roboczy procesu na sys._MEIPASS, dzięki
czemu względna ścieżka "ico.ico" w kodzie aplikacji od razu ją znajduje.
Nie jest tworzony, kopiowany ani zostawiany ŻADEN plik obok ContextMenuEditor.exe
- dystrybuowany jest wyłącznie jeden, samodzielny plik .exe (all-in-one).

Plik jest bezpieczny w wykonaniu - żaden wyjątek nie przerywa startu appki.
"""
import os
import sys

try:
    if getattr(sys, "frozen", False):
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass and os.path.exists(os.path.join(meipass, "ico.ico")):
            os.chdir(meipass)
except Exception:
    pass
