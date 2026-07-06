#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Edytor Menu Kontekstowego - Windows 11
polsoft.ITS™ Group

Pokazuje dokładnie te pozycje, które widać po kliknięciu PPM (klasyczne
menu "Pokaż więcej opcji" / shell) - bez żadnych dodatkowych informacji.
Pozwala: włączyć / wyłączyć / usunąć pozycję menu.

Wymaga Windows. Do pełnej funkcjonalności (wpisy systemowe, HKLM)
zalecane uruchomienie jako administrator.
"""

__author__ = "Sebastian Januchowski"
__copyright__ = "Copyright 2026, polsoft.ITS™ Group"
__credits__ = ["Sebastian Januchowski"]
__license__ = "Proprietary"
__version__ = "1.1.5"
__maintainer__ = "Sebastian Januchowski"
__email__ = "polsoft.its@mail.com"
__status__ = "Production"
__url__ = "https://github.com/polsoft-seb07uk"

import sys

if sys.platform != "win32":
    print("Ta aplikacja działa tylko w systemie Windows.")
    sys.exit(1)

import os
import json
import ctypes
import winreg
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser

# ---------------------------------------------------------------------------
# Ścieżka konfiguracji (zgodnie z wytycznymi polsoft)
# ---------------------------------------------------------------------------
CONFIG_DIR = os.path.expandvars(r"%userprofile%\.polsoft\settings")
CONFIG_FILE = os.path.join(CONFIG_DIR, "WebViewer.json")
ICON_FILE = "ico.ico"

def load_settings():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"theme": "light", "language": DEFAULT_LANG}

def save_settings(settings):
    try:
        os.makedirs(CONFIG_DIR, exist_ok=True)
        current = {}
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                current = json.load(f)
        current.update(settings)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(current, f, indent=4, ensure_ascii=False)
    except Exception:
        pass

# ---------------------------------------------------------------------------
# Uprawnienia administratora
# ---------------------------------------------------------------------------

def is_admin():
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def relaunch_as_admin():
    params = " ".join(f'"{a}"' for a in sys.argv)
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
    except Exception:
        pass
    sys.exit(0)

# ---------------------------------------------------------------------------
# Rozwiązywanie tekstu MUI
# ---------------------------------------------------------------------------

def resolve_mui_string(value):
    if not value or not value.startswith("@"):
        return value
    try:
        raw = value.lstrip("@")
        path_part, _, res_id = raw.rpartition(",-")
        if not path_part or not res_id:
            return value
        path_part = os.path.expandvars(path_part)
        res_id = int(res_id)
        LOAD_LIBRARY_AS_DATAFILE = 0x00000002
        h = ctypes.windll.kernel32.LoadLibraryExW(path_part, None, LOAD_LIBRARY_AS_DATAFILE)
        if not h:
            return value
        buf = ctypes.create_unicode_buffer(1024)
        ctypes.windll.user32.LoadStringW(h, res_id, buf, 1024)
        ctypes.windll.kernel32.FreeLibrary(h)
        return buf.value if buf.value else value
    except Exception:
        return value

# ---------------------------------------------------------------------------
# Tłumaczenia / Translations
# ---------------------------------------------------------------------------

TRANSLATIONS = {
    "en": {
        "title": "Context Menu Editor - polsoft.ITS™ Group",
        "refresh": "Refresh",
        "enable": "Enable",
        "disable": "Disable",
        "delete": "Delete",
        "theme_light": "Theme: Light",
        "theme_dark": "Theme: Dark",
        "about": "About",
        "admin_missing": "No administrator privileges",
        "run_as_admin": "Run as administrator",
        "col_status": "Status",
        "col_name": "Name (as in menu)",
        "col_category": "Location",
        "status_enabled": "✔ On",
        "status_disabled": "✖ Off",
        "found_items": "Found {n} menu items.",
        "info_title": "Info",
        "select_at_least_one": "Select at least one item.",
        "no_permission_title": "No permission",
        "failed_to_change": "Failed to change: {names}\nRun the program as administrator.",
        "failed_to_delete": "Failed to delete: {names}\nRun the program as administrator.",
        "confirm_delete_title": "Confirm deletion",
        "confirm_delete_msg": "Permanently delete: {names}?",
        "about_title": "About",
        "about_app_name": "Context Menu Editor v1.1.5",
        "about_author": "Author: Sebastian Januchowski",
        "about_email": "E-mail: ",
        "about_github": "GitHub: ",
        "close": "Close",
        "cat_all_files": "Files (all)",
        "cat_all_files_ext": "Files (all) - extensions",
        "cat_folders": "Folders",
        "cat_folders_ext": "Folders - extensions",
        "cat_bg": "Folder background (empty space)",
        "cat_bg_ext": "Folder background - extensions",
        "cat_drives": "Drives",
        "cat_all_objects": "All objects",
        "cat_all_objects_ext": "All objects - extensions",
        "copy_name": "Copy name",
        "copied_status": "Copied: {name}",
    },
    "pl": {
        "title": "Edytor Menu Kontekstowego - polsoft.ITS™ Group",
        "refresh": "Odśwież",
        "enable": "Włącz",
        "disable": "Wyłącz",
        "delete": "Usuń",
        "theme_light": "Motyw: Jasny",
        "theme_dark": "Motyw: Ciemny",
        "about": "O programie",
        "admin_missing": "Brak uprawnień administratora",
        "run_as_admin": "Uruchom jako administrator",
        "col_status": "Stan",
        "col_name": "Nazwa (jak w menu)",
        "col_category": "Miejsce",
        "status_enabled": "✔ Wł.",
        "status_disabled": "✖ Wył.",
        "found_items": "Znaleziono {n} pozycji menu.",
        "info_title": "Info",
        "select_at_least_one": "Zaznacz co najmniej jedną pozycję.",
        "no_permission_title": "Brak uprawnień",
        "failed_to_change": "Nie udało się zmienić: {names}\nUruchom program jako administrator.",
        "failed_to_delete": "Nie udało się usunąć: {names}\nUruchom program jako administrator.",
        "confirm_delete_title": "Potwierdź usunięcie",
        "confirm_delete_msg": "Trwale usunąć: {names}?",
        "about_title": "O programie",
        "about_app_name": "Edytor Menu Kontekstowego v1.1.5",
        "about_author": "Autor: Sebastian Januchowski",
        "about_email": "E-mail: ",
        "about_github": "GitHub: ",
        "close": "Zamknij",
        "cat_all_files": "Pliki (wszystkie)",
        "cat_all_files_ext": "Pliki (wszystkie) - rozszerzenia",
        "cat_folders": "Foldery",
        "cat_folders_ext": "Foldery - rozszerzenia",
        "cat_bg": "Tło folderu (puste miejsce)",
        "cat_bg_ext": "Tło folderu - rozszerzenia",
        "cat_drives": "Dyski",
        "cat_all_objects": "Wszystkie obiekty",
        "cat_all_objects_ext": "Wszystkie obiekty - rozszerzenia",
        "copy_name": "Kopiuj nazwę",
        "copied_status": "Skopiowano: {name}",
    },
}

DEFAULT_LANG = "en"


def tr(lang, key, **kwargs):
    text = TRANSLATIONS.get(lang, TRANSLATIONS[DEFAULT_LANG]).get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text

# ---------------------------------------------------------------------------
# Miejsca w rejestrze (klucze kategorii tłumaczone przez TRANSLATIONS)
# ---------------------------------------------------------------------------

SHELL_ROOTS = [
    ("*\\shell", "cat_all_files"),
    ("*\\shellex\\ContextMenuHandlers", "cat_all_files_ext"),
    ("Directory\\shell", "cat_folders"),
    ("Directory\\shellex\\ContextMenuHandlers", "cat_folders_ext"),
    ("Directory\\Background\\shell", "cat_bg"),
    ("Directory\\Background\\shellex\\ContextMenuHandlers", "cat_bg_ext"),
    ("Drive\\shell", "cat_drives"),
    ("AllFilesystemObjects\\shell", "cat_all_objects"),
    ("AllFilesystemObjects\\shellex\\ContextMenuHandlers", "cat_all_objects_ext"),
]


def get_clsid_name(clsid):
    clsid = clsid.strip("{}")
    key_path = r"CLSID\{%s}" % clsid
    try:
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, key_path) as k:
            try:
                name, _ = winreg.QueryValueEx(k, None)
                if name:
                    return resolve_mui_string(name)
            except FileNotFoundError:
                pass
            try:
                with winreg.OpenKey(k, "InprocServer32") as k2:
                    dll, _ = winreg.QueryValueEx(k2, None)
                    return os.path.basename(dll)
            except (FileNotFoundError, OSError):
                pass
    except OSError:
        pass
    return "{%s}" % clsid


def is_verb_disabled(key):
    for name in ("LegacyDisable", "ProgrammaticAccessOnly"):
        try:
            winreg.QueryValueEx(key, name)
            return True
        except FileNotFoundError:
            continue
    return False


def scan_menu_items():
    items = []
    for path, category in SHELL_ROOTS:
        is_handler = "ContextMenuHandlers" in path
        try:
            root_key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, path)
        except OSError:
            continue

        i = 0
        while True:
            try:
                sub = winreg.EnumKey(root_key, i)
            except OSError:
                break
            i += 1
            full_path = f"{path}\\{sub}"
            try:
                with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, full_path) as k:
                    if is_handler:
                        try:
                            clsid, _ = winreg.QueryValueEx(k, None)
                        except FileNotFoundError:
                            clsid = ""
                        name = get_clsid_name(clsid) if clsid else sub
                        enabled = not sub.startswith("-")
                        items.append({
                            "display": name,
                            "category": category,
                            "reg_path": full_path,
                            "key_name": sub,
                            "type": "handler",
                            "enabled": enabled,
                        })
                    else:
                        display = None
                        try:
                            muiverb, _ = winreg.QueryValueEx(k, "MUIVerb")
                            display = resolve_mui_string(muiverb)
                        except FileNotFoundError:
                            pass
                        if not display:
                            try:
                                default_val, _ = winreg.QueryValueEx(k, None)
                                display = resolve_mui_string(default_val) if default_val else sub
                            except FileNotFoundError:
                                display = sub
                        enabled = not is_verb_disabled(k)
                        items.append({
                            "display": display,
                            "category": category,
                            "reg_path": full_path,
                            "key_name": sub,
                            "type": "verb",
                            "enabled": enabled,
                        })
            except OSError:
                continue
        winreg.CloseKey(root_key)
    return items

# ---------------------------------------------------------------------------
# Operacje rejestru
# ---------------------------------------------------------------------------

def set_enabled(item, enabled):
    try:
        if item["type"] == "verb":
            with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, item["reg_path"], 0, winreg.KEY_SET_VALUE) as k:
                if enabled:
                    try:
                        winreg.DeleteValue(k, "LegacyDisable")
                    except FileNotFoundError:
                        pass
                else:
                    winreg.SetValueEx(k, "LegacyDisable", 0, winreg.REG_SZ, "")
        else:
            parent, _, key_name = item["reg_path"].rpartition("\\")
            new_name = key_name[1:] if key_name.startswith("-") else "-" + key_name
            with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, parent, 0, winreg.KEY_ALL_ACCESS) as pk:
                val, vtype = winreg.QueryValueEx(pk, key_name)
                winreg.SetValueEx(pk, new_name, 0, vtype, val)
                winreg.DeleteValue(pk, key_name)
            item["reg_path"] = f"{parent}\\{new_name}"
            item["key_name"] = new_name
        return True
    except (PermissionError, OSError):
        return False


def _delete_key_recursive(parent_key, sub_name):
    with winreg.OpenKey(parent_key, sub_name, 0, winreg.KEY_ALL_ACCESS) as k:
        while True:
            try:
                child = winreg.EnumKey(k, 0)
            except OSError:
                break
            _delete_key_recursive(k, child)
    winreg.DeleteKey(parent_key, sub_name)


def delete_item(item):
    try:
        parent, _, key_name = item["reg_path"].rpartition("\\")
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, parent, 0, winreg.KEY_ALL_ACCESS) as pk:
            if item["type"] == "verb":
                _delete_key_recursive(pk, key_name)
            else:
                winreg.DeleteValue(pk, key_name)
        return True
    except (PermissionError, OSError):
        return False

# ---------------------------------------------------------------------------
# Klasa Główna GUI
# ---------------------------------------------------------------------------

class ContextMenuEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.settings = load_settings()
        self.lang = self.settings.get("language", DEFAULT_LANG)
        if self.lang not in TRANSLATIONS:
            self.lang = DEFAULT_LANG

        self.title(self.t("title"))
        self.geometry("840x580")
        self.minsize(620, 420)
        
        # Ładowanie ikony do paska tytułowego głównego okna
        if os.path.exists(ICON_FILE):
            try:
                self.iconbitmap(ICON_FILE)
            except Exception:
                pass
        
        self.current_theme = self.settings.get("theme", "light")
        
        self.style = ttk.Style(self)
        self.items = []
        self.buttons_list = []
        
        self._build_ui()
        self.apply_theme_colors()
        self.refresh()

    def t(self, key, **kwargs):
        return tr(self.lang, key, **kwargs)

    def _build_tree_context_menu(self):
        """Buduje (lub przebudowuje po zmianie języka) menu kontekstowe PPM listy."""
        self.tree_menu.delete(0, "end")
        self.tree_menu.add_command(label=self.t("refresh"), command=self.refresh)
        self.tree_menu.add_separator()
        self.tree_menu.add_command(label=self.t("enable"), command=self.enable_selected)
        self.tree_menu.add_command(label=self.t("disable"), command=self.disable_selected)
        self.tree_menu.add_separator()
        self.tree_menu.add_command(label=self.t("copy_name"), command=self.copy_selected_name)
        self.tree_menu.add_separator()
        self.tree_menu.add_command(label=self.t("delete"), command=self.delete_selected)

    def copy_selected_name(self):
        sel = self._selected_items()
        if not sel:
            messagebox.showinfo(self.t("info_title"), self.t("select_at_least_one"))
            return
        text = "\n".join(i["display"] for i in sel)
        self.clipboard_clear()
        self.clipboard_append(text)
        self.status_bar.config(text=self.t("copied_status", name=sel[0]["display"] if len(sel) == 1 else f"{len(sel)} items"))

    def toggle_language(self):
        self.lang = "pl" if self.lang == "en" else "en"
        save_settings({"language": self.lang})
        self.retranslate_ui()

    def retranslate_ui(self):
        self.title(self.t("title"))

        self.btn_ref.config(text=self.t("refresh"))
        self.btn_en.config(text=self.t("enable"))
        self.btn_dis.config(text=self.t("disable"))
        self.btn_del.config(text=self.t("delete"))
        self.btn_theme.config(text=self.t("theme_dark" if self.current_theme == "dark" else "theme_light"))
        self.btn_abt.config(text=self.t("about"))

        if not is_admin():
            self.admin_label.config(text=self.t("admin_missing"))
            self.btn_adm.config(text=self.t("run_as_admin"))

        self.tree.heading("status", text=self.t("col_status"))
        self.tree.heading("name", text=self.t("col_name"))
        self.tree.heading("category", text=self.t("col_category"))

        self.lang_btn.config(text=self._lang_btn_text())

        self._build_tree_context_menu()

        self.refresh()

    def _lang_btn_text(self):
        return "🌐 EN" if self.lang == "en" else "🌐 PL"

    def _style_action_button(self, btn):
        """Usuwa systemowe obramowania i przypisuje zdarzenia podświetlenia z czarnym tekstem"""
        btn.config(
            font=("Segoe UI", 9),
            relief="flat",
            bd=0,
            highlightthickness=0,
            padx=12,
            pady=3
        )
        btn.bind("<Enter>", lambda e: btn.config(bg="#e5e5e5", fg="#000000"))
        btn.bind("<Leave>", lambda e: self._restore_button_color(btn))
        self.buttons_list.append(btn)

    def _restore_lang_btn_color(self):
        if self.current_theme == "dark":
            self.lang_btn.config(bg="#3a3a3a", fg="#ffffff")
        else:
            self.lang_btn.config(bg="#ffffff", fg="#000000")

    def _restore_button_color(self, btn):
        if self.current_theme == "dark":
            btn.config(bg="#3a3a3a", fg="#ffffff")
        else:
            btn.config(bg="#ffffff", fg="#000000")

    def _build_ui(self):
        self.top_panel = ttk.Frame(self, padding=8)
        self.top_panel.pack(fill="x")

        self.btn_ref = tk.Button(self.top_panel, text=self.t("refresh"), command=self.refresh)
        self.btn_ref.pack(side="left")
        self._style_action_button(self.btn_ref)

        self.btn_en = tk.Button(self.top_panel, text=self.t("enable"), command=self.enable_selected)
        self.btn_en.pack(side="left", padx=4)
        self._style_action_button(self.btn_en)

        self.btn_dis = tk.Button(self.top_panel, text=self.t("disable"), command=self.disable_selected)
        self.btn_dis.pack(side="left")
        self._style_action_button(self.btn_dis)

        self.btn_del = tk.Button(self.top_panel, text=self.t("delete"), command=self.delete_selected)
        self.btn_del.pack(side="left", padx=4)
        self._style_action_button(self.btn_del)
        
        self.btn_theme = tk.Button(self.top_panel, text=self.t("theme_light"), command=self.toggle_theme)
        self.btn_theme.pack(side="left")
        self._style_action_button(self.btn_theme)
        
        self.btn_abt = tk.Button(self.top_panel, text=self.t("about"), command=self.show_about)
        self.btn_abt.pack(side="left", padx=4)
        self._style_action_button(self.btn_abt)

        self.admin_label = ttk.Label(self.top_panel, text="")
        if not is_admin():
            self.admin_label.config(text=self.t("admin_missing"), foreground="#b00")
            self.admin_label.pack(side="right", padx=(0, 6))
            
            self.btn_adm = tk.Button(self.top_panel, text=self.t("run_as_admin"), command=relaunch_as_admin)
            self.btn_adm.pack(side="right")
            self._style_action_button(self.btn_adm)

        # Kontener na listę + paski przewijania (pionowy i poziomy)
        self.tree_frame = ttk.Frame(self)
        self.tree_frame.pack(fill="both", expand=True, padx=8, pady=8)
        self.tree_frame.rowconfigure(0, weight=1)
        self.tree_frame.columnconfigure(0, weight=1)

        cols = ("status", "name", "category")
        self.tree = ttk.Treeview(self.tree_frame, columns=cols, show="headings", selectmode="extended")
        self.tree.heading("status", text=self.t("col_status"))
        self.tree.heading("name", text=self.t("col_name"))
        self.tree.heading("category", text=self.t("col_category"))
        self.tree.column("status", width=80, anchor="center")
        self.tree.column("name", width=440)
        self.tree.column("category", width=240)

        # Widoczny pionowy pasek przewijania
        self.tree_vsb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        # Widoczny poziomy pasek przewijania (przydatny przy długich nazwach/ścieżkach)
        self.tree_hsb = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.tree_vsb.set, xscrollcommand=self.tree_hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree_vsb.grid(row=0, column=1, sticky="ns")
        self.tree_hsb.grid(row=1, column=0, sticky="ew")

        self.tree.bind("<Double-1>", lambda e: self.toggle_selected())

        # Przewijanie kółkiem myszy (Windows: <MouseWheel>; Linux: <Button-4>/<Button-5>)
        def _on_mousewheel(event):
            self.tree.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _on_mousewheel_linux(event):
            self.tree.yview_scroll(-1 if event.num == 4 else 1, "units")

        self.tree.bind("<MouseWheel>", _on_mousewheel)
        self.tree.bind("<Button-4>", _on_mousewheel_linux)
        self.tree.bind("<Button-5>", _on_mousewheel_linux)
        # Shift + kółko myszy = przewijanie poziome
        self.tree.bind("<Shift-MouseWheel>", lambda e: self.tree.xview_scroll(int(-1 * (e.delta / 120)), "units"))

        # Pełna obsługa przewijania klawiaturą: Home/End/PageUp/PageDown/strzałki
        self.tree.bind("<Home>", lambda e: (self.tree.yview_moveto(0), "break"))
        self.tree.bind("<End>", lambda e: (self.tree.yview_moveto(1), "break"))
        self.tree.bind("<Prior>", lambda e: self.tree.yview_scroll(-1, "pages"))  # Page Up
        self.tree.bind("<Next>", lambda e: self.tree.yview_scroll(1, "pages"))    # Page Down

        # ---------------------------------------------------------------
        # Menu kontekstowe (prawy przycisk myszy) na liście
        # ---------------------------------------------------------------
        self.tree_menu = tk.Menu(self.tree, tearoff=0)
        self._build_tree_context_menu()

        def _show_tree_menu(event):
            row_id = self.tree.identify_row(event.y)
            if row_id:
                # Jeśli kliknięty wiersz nie jest zaznaczony, zaznacz tylko jego
                if row_id not in self.tree.selection():
                    self.tree.selection_set(row_id)
                self.tree.focus(row_id)
            has_sel = bool(self.tree.selection())
            state = "normal" if has_sel else "disabled"
            # Indeksy: 0=Refresh, 1=sep, 2=Enable, 3=Disable, 4=sep, 5=Copy name, 6=sep, 7=Delete
            for idx in (2, 3, 5, 7):
                self.tree_menu.entryconfig(idx, state=state)
            try:
                self.tree_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.tree_menu.grab_release()

        self.tree.bind("<Button-3>", _show_tree_menu)     # PPM - Windows/Linux
        self.tree.bind("<Control-Button-1>", _show_tree_menu)  # macOS-style fallback

        self.status_frame = ttk.Frame(self)
        self.status_frame.pack(fill="x", side="bottom")

        self.status_bar = ttk.Label(self.status_frame, text="", anchor="w", padding=4)
        self.status_bar.pack(side="left", fill="x", expand=True, padx=(8, 0))

        self.lang_btn = tk.Button(
            self.status_frame,
            text=self._lang_btn_text(),
            command=self.toggle_language,
            font=("Segoe UI", 9),
            relief="flat",
            bd=0,
            highlightthickness=0,
            padx=8,
            pady=2,
            cursor="hand2",
        )
        self.lang_btn.pack(side="right", padx=8, pady=2)
        self.lang_btn.bind("<Enter>", lambda e: self.lang_btn.config(bg="#e5e5e5", fg="#000000"))
        self.lang_btn.bind("<Leave>", lambda e: self._restore_lang_btn_color())

    def apply_theme_colors(self):
        """Konfiguracja stylów pod wybrany motyw"""
        if self.current_theme == "dark":
            bg_color = "#202020"
            fg_color = "#ffffff"
            panel_bg = "#2d2d2d"
            tree_bg = "#1e1e1e"
            tree_fg = "#e0e0e0"
            select_bg = "#0078d4"
            select_fg = "#ffffff"
            
            for btn in self.buttons_list:
                btn.config(
                    bg="#3a3a3a",
                    fg="#ffffff",
                    activebackground="#e5e5e5",
                    activeforeground="#000000"
                )
            self.btn_theme.config(text=self.t("theme_dark"))
        else:
            bg_color = "#f3f3f3"
            fg_color = "#000000"
            panel_bg = "#e6e6e6"
            tree_bg = "#ffffff"
            tree_fg = "#000000"
            select_bg = "#a6d2ff"
            select_fg = "#000000"
            
            for btn in self.buttons_list:
                btn.config(
                    bg="#ffffff",
                    fg="#000000",
                    activebackground="#e5e5e5",
                    activeforeground="#000000"
                )
            self.btn_theme.config(text=self.t("theme_light"))

        self.config(bg=bg_color)
        self.style.theme_use("vista" if sys.platform == "win32" and self.current_theme == "light" else "default")
        
        self.style.configure(".", background=bg_color, foreground=fg_color)
        self.style.configure("TFrame", background=bg_color)
        self.style.configure("TLabel", background=bg_color, foreground=fg_color)
        
        self.style.configure("Treeview", 
                             background=tree_bg, 
                             fieldbackground=tree_bg, 
                             foreground=tree_fg,
                             rowheight=24)
        self.style.map("Treeview", 
                       background=[("selected", select_bg)], 
                       foreground=[("selected", select_fg)])

        # Stylowanie paska przewijania zgodnie z aktywnym motywem
        self.style.configure("Vertical.TScrollbar",
                             background=panel_bg,
                             troughcolor=tree_bg,
                             bordercolor=tree_bg,
                             arrowcolor=fg_color,
                             relief="flat")
        self.style.configure("Horizontal.TScrollbar",
                             background=panel_bg,
                             troughcolor=tree_bg,
                             bordercolor=tree_bg,
                             arrowcolor=fg_color,
                             relief="flat")
        
        self.style.configure("Treeview.Heading", 
                             background=panel_bg, 
                             foreground=fg_color, 
                             relief="flat")
        
        self.style.configure("StatusFrame.TFrame", background=panel_bg)
        self.status_frame.config(style="StatusFrame.TFrame")
        self.status_bar.config(background=panel_bg, foreground=fg_color)
        self._restore_lang_btn_color()
        if not is_admin() and self.current_theme == "dark":
            self.admin_label.config(foreground="#ff6b6b", background=bg_color)

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme_colors()
        save_settings({"theme": self.current_theme})

    def show_about(self):
        about_win = tk.Toplevel(self)
        about_win.title(self.t("about_title"))
        about_win.geometry("400x260")
        about_win.resizable(False, False)
        about_win.transient(self)
        about_win.grab_set()

        # Przypisanie ikony również do paska tytułowego okna "O programie"
        if os.path.exists(ICON_FILE):
            try:
                about_win.iconbitmap(ICON_FILE)
            except Exception:
                pass

        is_dark = (self.current_theme == "dark")
        win_bg = "#202020" if is_dark else "#f3f3f3"
        text_fg = "#ffffff" if is_dark else "#000000"
        link_fg = "#6ba4ff" if is_dark else "blue"
        
        about_win.config(bg=win_bg)

        about_win.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (about_win.winfo_width() // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (about_win.winfo_height() // 2)
        about_win.geometry(f"+{x}+{y}")

        frame = tk.Frame(about_win, padx=15, pady=15, bg=win_bg)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text=self.t("about_app_name"), font=("Segoe UI", 12, "bold"), bg=win_bg, fg=text_fg).pack(pady=(0, 5))
        tk.Label(frame, text="polsoft.ITS™ Group", font=("Segoe UI", 10, "italic"), bg=win_bg, fg=text_fg).pack(pady=(0, 15))
        
        tk.Label(frame, text=self.t("about_author"), bg=win_bg, fg=text_fg).pack(anchor="w", pady=2)
        
        mail_frame = tk.Frame(frame, bg=win_bg)
        mail_frame.pack(anchor="w", pady=2)
        tk.Label(mail_frame, text=self.t("about_email"), bg=win_bg, fg=text_fg).pack(side="left")
        link_mail = tk.Label(mail_frame, text="polsoft.its@mail.com", fg=link_fg, bg=win_bg, cursor="hand2")
        link_mail.pack(side="left")
        link_mail.bind("<Button-1>", lambda e: webbrowser.open("mailto:polsoft.its@mail.com"))

        gh_frame = tk.Frame(frame, bg=win_bg)
        gh_frame.pack(anchor="w", pady=2)
        tk.Label(gh_frame, text=self.t("about_github"), bg=win_bg, fg=text_fg).pack(side="left")
        link_gh = tk.Label(gh_frame, text="github.com/polsoft-seb07uk", fg=link_fg, bg=win_bg, cursor="hand2")
        link_gh.pack(side="left")
        link_gh.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/polsoft-seb07uk"))

        btn_close = tk.Button(frame, text=self.t("close"), command=about_win.destroy)
        btn_close.pack(pady=(25, 0))
        self._style_action_button(btn_close)
        self._restore_button_color(btn_close)

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        self.items = scan_menu_items()
        self.items.sort(key=lambda x: (self.t(x["category"]), x["display"].lower()))
        for idx, item in enumerate(self.items):
            status = self.t("status_enabled") if item["enabled"] else self.t("status_disabled")
            self.tree.insert("", "end", iid=str(idx), values=(status, item["display"], self.t(item["category"])))
        self.status_bar.config(text=self.t("found_items", n=len(self.items)))

    def _selected_items(self):
        return [self.items[int(iid)] for iid in self.tree.selection()]

    def toggle_selected(self):
        sel = self._selected_items()
        if not sel:
            return
        self._apply_enabled(sel, not sel[0]["enabled"])

    def enable_selected(self):
        self._apply_enabled(self._selected_items(), True)

    def disable_selected(self):
        self._apply_enabled(self._selected_items(), False)

    def _apply_enabled(self, sel, enabled):
        if not sel:
            messagebox.showinfo(self.t("info_title"), self.t("select_at_least_one"))
            return
        failed = [i["display"] for i in sel if not set_enabled(i, enabled)]
        for i in sel:
            if i["display"] not in failed:
                i["enabled"] = enabled
        if failed:
            messagebox.showwarning(
                self.t("no_permission_title"),
                self.t("failed_to_change", names=", ".join(failed))
            )
        self.refresh()

    def delete_selected(self):
        sel = self._selected_items()
        if not sel:
            messagebox.showinfo(self.t("info_title"), self.t("select_at_least_one"))
            return
        names = ", ".join(i["display"] for i in sel)
        if not messagebox.askyesno(self.t("confirm_delete_title"), self.t("confirm_delete_msg", names=names)):
            return
        failed = [i["display"] for i in sel if not delete_item(i)]
        if failed:
            messagebox.showwarning(
                self.t("no_permission_title"),
                self.t("failed_to_delete", names=", ".join(failed))
            )
        self.refresh()


if __name__ == "__main__":
    app = ContextMenuEditor()
    app.mainloop()