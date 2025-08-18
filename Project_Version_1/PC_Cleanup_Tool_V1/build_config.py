"""
PyInstaller Build Configuration for PC Cleanup Tool
Professional packaging system for standalone executable distribution
"""

import PyInstaller.__main__
import os
import sys
from pathlib import Path
import shutil

def create_spec_file():
    """Create PyInstaller spec file for advanced configuration"""
    
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['gui_app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('README.md', '.'),
        ('requirements.txt', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.scrolledtext',
        'psutil',
        'winreg',
        'subprocess',
        'threading',
        'queue',
        'json',
        'pathlib',
        'datetime',
        'logging',
        'shutil',
        'webbrowser'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'cv2',
        'tensorflow',
        'torch'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NicksPCCleanupTool',
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
    version='version_info.txt',
    icon='icon.ico'
)
'''
    
    with open('pc_cleanup_tool.spec', 'w') as f:
        f.write(spec_content)
    
    print("✅ Created PyInstaller spec file: pc_cleanup_tool.spec")

def create_version_info():
    """Create version information file for Windows executable"""
    
    version_info = '''
# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Nick P - IT Solutions'),
        StringStruct(u'FileDescription', u'Professional PC Cleanup & Optimization Tool'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'PCCleanupTool'),
        StringStruct(u'LegalCopyright', u'© 2025 Nick P. All rights reserved.'),
        StringStruct(u'OriginalFilename', u'NicksPCCleanupTool.exe'),
        StringStruct(u'ProductName', u'Nick\'s PC Optimization Suite'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
    
    with open('version_info.txt', 'w') as f:
        f.write(version_info)
    
    print("✅ Created version info file: version_info.txt")

def create_installer_script():
    """Create NSIS installer script for professional deployment"""
    
    nsis_script = '''
; PC Cleanup Tool Installer Script
; Professional installer for business deployment

!define APPNAME "Nick's PC Optimization Suite"
!define COMPANYNAME "Nick P - IT Solutions"
!define DESCRIPTION "Professional PC Cleanup & Optimization Tool"
!define VERSIONMAJOR 1
!define VERSIONMINOR 0
!define VERSIONBUILD 0
!define HELPURL "https://your-website.com/support"
!define UPDATEURL "https://your-website.com/updates"
!define ABOUTURL "https://your-website.com"
!define INSTALLSIZE 50000

RequestExecutionLevel admin
InstallDir "$PROGRAMFILES\\${COMPANYNAME}\\${APPNAME}"

Name "${APPNAME}"
Icon "icon.ico"
outFile "PCCleanupTool_Installer_v${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}.exe"

!include LogicLib.nsh

page components
page directory
page instfiles

!macro VerifyUserIsAdmin
UserInfo::GetAccountType
pop $0
${If} $0 != "admin"
    messageBox mb_iconstop "Administrator rights required!"
    setErrorLevel 740
    quit
${EndIf}
!macroend

function .onInit
    setShellVarContext all
    !insertmacro VerifyUserIsAdmin
functionEnd

section "PC Cleanup Tool (Required)"
    setOutPath $INSTDIR
    
    ; Main executable
    file "dist\\NicksPCCleanupTool.exe"
    file "README.md"
    file "LICENSE"
    
    ; Create uninstaller
    writeUninstaller "$INSTDIR\\uninstall.exe"
    
    ; Start Menu shortcuts
    createDirectory "$SMPROGRAMS\\${COMPANYNAME}"
    createShortCut "$SMPROGRAMS\\${COMPANYNAME}\\${APPNAME}.lnk" "$INSTDIR\\NicksPCCleanupTool.exe"
    createShortCut "$SMPROGRAMS\\${COMPANYNAME}\\Uninstall.lnk" "$INSTDIR\\uninstall.exe"
    
    ; Desktop shortcut
    createShortCut "$DESKTOP\\${APPNAME}.lnk" "$INSTDIR\\NicksPCCleanupTool.exe"
    
    ; Registry information for add/remove programs
    writeRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "DisplayName" "${APPNAME}"
    writeRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "UninstallString" "$INSTDIR\\uninstall.exe"
    writeRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "InstallLocation" "$INSTDIR"
    writeRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "DisplayIcon" "$INSTDIR\\NicksPCCleanupTool.exe"
    writeRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "Publisher" "${COMPANYNAME}"
    writeRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "HelpLink" "${HELPURL}"
    writeRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "URLUpdateInfo" "${UPDATEURL}"
    writeRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "URLInfoAbout" "${ABOUTURL}"
    writeRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "DisplayVersion" "${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}"
    writeRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "VersionMajor" ${VERSIONMAJOR}
    writeRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "VersionMinor" ${VERSIONMINOR}
    writeRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "NoModify" 1
    writeRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "NoRepair" 1
    writeRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "EstimatedSize" ${INSTALLSIZE}
sectionEnd

section "Uninstall"
    ; Remove files
    delete "$INSTDIR\\NicksPCCleanupTool.exe"
    delete "$INSTDIR\\README.md"
    delete "$INSTDIR\\LICENSE"
    delete "$INSTDIR\\uninstall.exe"
    
    ; Remove shortcuts
    delete "$SMPROGRAMS\\${COMPANYNAME}\\${APPNAME}.lnk"
    delete "$SMPROGRAMS\\${COMPANYNAME}\\Uninstall.lnk"
    delete "$DESKTOP\\${APPNAME}.lnk"
    rmDir "$SMPROGRAMS\\${COMPANYNAME}"
    
    ; Remove installation directory
    rmDir "$INSTDIR"
    
    ; Remove registry entries
    deleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}"
sectionEnd
'''
    
    with open('installer.nsi', 'w') as f:
        f.write(nsis_script)
    
    print("✅ Created NSIS installer script: installer.nsi")

def build_executable():
    """Build the standalone executable using PyInstaller"""
    
    print("🔨 Building standalone executable...")
    
    # Clean previous builds
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    # Build using spec file
    PyInstaller.__main__.run([
        'pc_cleanup_tool.spec',
        '--clean',
        '--noconfirm'
    ])
    
    print("✅ Executable built successfully!")
    print(f"📁 Location: {os.path.abspath('dist')}")

def create_portable_package():
    """Create portable package with all necessary files"""
    
    print("📦 Creating portable package...")
    
    portable_dir = Path('portable_package')
    if portable_dir.exists():
        shutil.rmtree(portable_dir)
    
    portable_dir.mkdir()
    
    # Copy executable
    if Path('dist/NicksPCCleanupTool.exe').exists():
        shutil.copy2('dist/NicksPCCleanupTool.exe', portable_dir)
    
    # Copy documentation
    for file in ['README.md', 'requirements.txt']:
        if Path(file).exists():
            shutil.copy2(file, portable_dir)
    
    # Create portable config
    portable_config = {
        "portable_mode": True,
        "log_directory": "./logs",
        "report_directory": "./reports",
        "branding": {
            "title": "Nick's PC Optimization Suite - Portable",
            "company": "Nick P - IT Solutions"
        }
    }
    
    with open(portable_dir / 'portable_config.json', 'w') as f:
        json.dump(portable_config, f, indent=2)
    
    # Create batch file for easy launching
    batch_content = '''@echo off
title Nick's PC Cleanup Tool - Portable
echo Starting PC Cleanup Tool...
NicksPCCleanupTool.exe
pause
'''
    
    with open(portable_dir / 'run_cleanup_tool.bat', 'w') as f:
        f.write(batch_content)
    
    print(f"✅ Portable package created: {portable_dir.absolute()}")

def main():
    """Main build process"""
    print("🚀 PC Cleanup Tool - Professional Build System")
    print("=" * 50)
    
    try:
        # Create build files
        create_spec_file()
        create_version_info()
        create_installer_script()
        
        # Build executable
        build_executable()
        
        # Create portable package
        create_portable_package()
        
        print("\n✅ Build process completed successfully!")
        print("\nNext steps:")
        print("1. Test the executable in dist/NicksPCCleanupTool.exe")
        print("2. Use NSIS to compile installer.nsi for professional installer")
        print("3. Deploy portable_package/ for portable distribution")
        print("4. Customize branding in the source files as needed")
        
    except Exception as e:
        print(f"❌ Build failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
