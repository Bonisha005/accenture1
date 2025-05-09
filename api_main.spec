# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['api_main.py'],
    pathex=[r'C:\Users\Bonisha\Downloads\retail_agents'],
    binaries=[],
    datas=[('db', 'db'), ('scripts', 'scripts'), ('llm', 'llm'), ('tools', 'tools'), ('ml_models', 'ml_models'), ('agents', 'agents'), ('api', 'api')],
    hiddenimports=['sentence_transformers', 'transformers', 'torch', 'scipy'],
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
    name='api_main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
