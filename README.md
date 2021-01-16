# Random-Game-Picker
When you don't know what game you want to play this GUI program can help you to pick a random game from your GOG Galaxy library.

Basically, this program consists of three parts:
* .py script that generates .csv file from GOG Galaxy database file
* .py script that processing .csv file and describes main program logic and .kv design file for GUI
* .spec file to build executable file with PyInstaller

## Resources
[GOG-Galaxy-Export-Script](https://github.com/AB1908/GOG-Galaxy-Export-Script) — A script which generates a .csv file containing your GOG Galaxy Database. To be more specific I used and slightly edited a script from this [pull request](https://github.com/AB1908/GOG-Galaxy-Export-Script/pull/38)

[Random Galaxy Game launcher](https://gist.github.com/maxwellainatchi/794d22c2c24f98d5dc8e6abc7ccc8a92#file-random-galaxy-game-bat) — .bat script that opens a random game page in GOG Galaxy library. Basically, I used the last line of this script in my code

## Additional info
If you want to use this program, make sure you have kivy, natsort, and csv modules installed. Also, some additional libraries may be required.
The main file you need to run is RandomGamePicker.py

If you want to build an executable, you'll need PyInstaller.
To build .exe with PyInstaller use the following command:
```
pyinstaller RandomGamePicker.spec
```
> NOTE 1. .spec file was meant to be used with PyInstaller `--onedir` command-line argument. If you want to create a standalone executable, you need to create a separate .spec file.

> NOTE 2. PyInstaller officially supports Python 3.7 and lower, though I build executable with Python 3.9

> NOTE 3. You may want to recompile [bootloader](https://stackoverflow.com/a/52054580/10873426) for PyInstaller.
