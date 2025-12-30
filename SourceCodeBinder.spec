# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('function', 'function'), ('gui', 'gui'), ('C:\\Users\\EJI1WX\\OneDrive - Bosch Group\\PythonProject\\SourceCodeBinder\\resources\\SourceCodeBinder.ico', '.')]
binaries = []
hiddenimports = ['customtkinter', 'markdown2', 'pdfkit']
tmp_ret = collect_all('customtkinter')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['SourceCodeBinder.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='SourceCodeBinder',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\EJI1WX\\OneDrive - Bosch Group\\PythonProject\\SourceCodeBinder\\resources\\SourceCodeBinder.ico'],
)
