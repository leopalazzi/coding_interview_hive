from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(
    name = "Account Generator",
    version = "1",
    description = "Account Generator",
    executables = [Executable("accountGenerator.py")],
)