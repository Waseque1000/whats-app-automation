# -*- mode: python ; coding: utf-8 -*-
import sys
from pathlib import Path
import customtkinter

block_cipher = None

# CustomTkinter assets path
ctk_path = Path(customtkinter.__file__).parent

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        (str(ctk_path), 'customtkinter/'),
        ('.env.example', '.'),
    ],
    hiddenimports=[
        'customtkinter',
        'openpyxl',
        'xlrd',
        'phonenumbers',
        'PIL',
        'sqlite3',
        'pandas',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['playwright', 'pytest'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='WhatsAppStudentMessenger',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='WhatsAppStudentMessenger',
)

app = BUNDLE(
    coll,
    name='WhatsAppStudentMessenger.app',
    icon=None,
    bundle_identifier='com.whatsapp.studentmessenger',
)
