#For Game Outline
#on cmd type: python setup.py build

from cx_Freeze import setup, Executable
includefiles = ['Resources', #Add Images and Music here
                'configuration.info',
                'readme.md']
includes = []
packages = ["Scripts", #Local Scripts
    "pygame", "sys", "os", "time", "pickle", "random"]#Python Packages

target = Executable(script='gameloop.py',
                    base='WIN32GUI', #None if console only
                    compress=False,
                    copyDependentFiles=True,
                    appendScriptToExe=True,
                    appendScriptToLibrary=False,
                    icon=None) #Place your path to the game's icon

setup(
    name = 'Game Name',#
    version = '1.0.0',#
    description = 'Description.',#
    author = 'Seraph Wedd', #
    author_email = 'seraphwedd18@gmail.com', #
    options = {'build_exe': {'packages':packages, 'include_files':includefiles}},
    executables = [target]
    )
