from kivy_deps import sdl2, glew
import os
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

user_path = os.getcwd()

a = Analysis(['RandomGamePicker.py'],
             pathex=[user_path],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='RandomGamePicker',
          debug=False,
          icon=[user_path + "\\images\\app.ico"],
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe, Tree(user_path),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Random Game Picker')
