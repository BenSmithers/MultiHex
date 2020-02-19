# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['launch.py'],
             pathex=['C:\\Users\\ramcg\\PycharmProjects\\MultiHex\\MultiHex'],
             binaries=[],
             datas=[('generator\\config.json', 'MultiHex\\generator'), ('hexes', 'hexes'),
                    ('resources\\binary_tables', 'MultiHex\\resources\\binary_tables'),
                    ('resources\\text_files','MultiHex\\resources\\text_files'),
                    ('Artwork', 'MultiHex\\Artwork'),


             ],
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
          name='launch',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='launch')
