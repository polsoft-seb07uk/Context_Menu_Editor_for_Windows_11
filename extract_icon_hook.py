# -*- coding: utf-8 -*-
"""
Runtime hook PyInstaller (uruchamiany PRZED context_menu_editor.py).

Aplikacja wczytuje ikonę okna przez tkinter (self.iconbitmap("ico.ico")),
sprawdzając WZGLĘDNĄ ścieżkę do pliku "ico.ico" w bieżącym katalogu roboczym.

W trybie --onefile plik ico.ico jest owinięty do wnętrza .exe i przy starcie
rozpakowywany do tymczasowego katalogu sys._MEIPASS, a NIE do katalogu,
w którym leży sam plik .exe. Ten hook kopiuje ikonę z _MEIPASS obok pliku
.exe (tylko przy pierwszym uruchomieniu), dzięki czemu:
  - plik .exe pozostaje pojedynczym plikiem "all-in-one" do rozesłania,
  - a po pierwszym uruchomieniu ikona w oknie/"O programie" również działa.

Plik jest bezpieczny w wykonaniu - żaden wyjątek nie przerywa startu appki.
"""
import os
import sys
import shutil

try:
    if getattr(sys, "frozen", False):
        meipass = getattr(sys, "_MEIPASS", None)
        exe_dir = os.path.dirname(os.path.abspath(sys.executable))
        if meipass:
            src = os.path.join(meipass, "ico.ico")
            dst = os.path.join(exe_dir, "ico.ico")
            if os.path.exists(src) and not os.path.exists(dst):
                shutil.copy2(src, dst)
        # Upewnij się, że katalogiem roboczym jest katalog pliku .exe,
        # zgodnie z tym, czego oczekuje kod aplikacji (ścieżki względne).
        try:
            os.chdir(exe_dir)
        except Exception:
            pass
except Exception:
    pass
