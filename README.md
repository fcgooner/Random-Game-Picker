# Random-Game-Picker

Go to [HOW TO INSTALL](#how-to-install)

When you don't know what game you want to play this GUI program can help you to pick a random game from your GOG Galaxy library.

Basically, this program consists of three parts:
* .py script that generates .csv file from GOG Galaxy database file
* .py script that processing .csv file and describes main program logic and .kv design file for GUI
* .spec file to build executable file with PyInstaller

## Resources
[GOG-Galaxy-Export-Script](https://github.com/AB1908/GOG-Galaxy-Export-Script) — A script which generates a .csv file containing your GOG Galaxy Database. To be more specific I used and slightly edited a script from this [pull request](https://github.com/AB1908/GOG-Galaxy-Export-Script/pull/38)

[Random Galaxy Game launcher](https://gist.github.com/maxwellainatchi/794d22c2c24f98d5dc8e6abc7ccc8a92#file-random-galaxy-game-bat) — .bat script that opens a random game page in GOG Galaxy library. Basically, I used the last line of this script in my code

## HOW TO INSTALL
1. Download this repository and unpack it to any folder. 
2. Download and install [Python 3.1.9 (32bit)](https://www.python.org/downloads/release/python-391/). Don't forget to set a checkbox "Add Python 3.9 to PATH" during installation.
3. After Python is installed, press `Windows key`+`R` and type in `cmd` to open Windows command-line. Install kivy using the following command: `pip install kivy`
4. Install natsort module using the following command: `pip install natsort`
5. Install pyinstaller using the following command: `pip install pyinstaller`
6. Open a folder with your unpacked files from Step 1.
7. Hit `Alt`+`D` on your keyboard to highlight what’s in the address bar (or `CTRL`+`L`) and then copy highlighted path.
8. Open RandomGamePicker.spec file in any text editor and replace three placeholders with your copied path. Don't forget to change `\` to `\\` in your copied path. Save and close the file.
9. Hit `Alt`+`D` (or `CTRL`+`L`), type in `cmd` in address bar and hit `Enter`. This will open Windows command-line in current folder.
10. In opened window type in `dir` and press `Enter`. You will get a printout of all folders and files inside your current directory. Make sure that the printout has all required files (RandomGamePicker.py, RandomGamePicker.kv etc.)
11. Type in `pyinstaller RandomGamePicker.spec` and while PyInstaller finish to compile the program.
12. After Step 11 is done, there should be a `dist` folder. Inside it you'll see a `Random Game Picker` folder. This is your application folder. You can move it to any other location you like.
13. Run `Random Game Picker.exe` file inside `Random Game Picker` folder to launch the program.

To remove all installed modules during installation Steps, open Windows command-line and run these commands:
1. `pip freeze > requirements.txt`
2. `pip uninstall -r requirements.txt -y`

To uninstall Python use Control Panel.

## Additional info
1. .spec file was meant to be used with PyInstaller `--onedir` command-line argument. If you want to create a standalone executable using `--onefile`, you'll need to create a separate .spec file.
2. PyInstaller officially supports Python 3.7 and lower, though I built an executable with Python 3.9
3. You may want to recompile a [bootloader](https://stackoverflow.com/a/52054580/10873426) for PyInstaller.
