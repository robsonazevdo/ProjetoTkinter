import sys
from cx_Freeze import setup, Executable
import tkinter

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
        Executable("app.py", base=base)
]

buildOptions = dict(
        packages = [],
        includes = [],
        include_files = [],
        excludes = []
)




setup(
    name = "Historico Atendimento",
    version = "1.0",
    description = "Gravar o atendimento efetuado",
    options = dict(build_exe = buildOptions),
    executables = executables
 )
