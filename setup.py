#-*-coding: utf-8-*-

import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages":["os"], "excludes":["tkinter"]}

base = None

if sys.platform == "win32": base = "Win32GUI"

setup(name = "try.py", version = '0.1', description = "some",
      options = {"buil_exe":build_exe_options}, executables = [Executable("setup.py", base = base
    )])