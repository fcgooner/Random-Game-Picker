# Random-Game-Picker

Go to [HOW TO INSTALL](#how-to-install)

Update - Version 1.2 (22.01.2021)
- Tags support added
- Two pre-defined window resolutions added
- Slightly improved randomizer: the program will not pick the same game more than once during one cycle.

============================================================================================

Don't know what game to play next? Let Random Game Picker to decide that for you!
Random Game Picker picks a random game from your GOG Galaxy library.

Basically, this program consists of three parts:
* .py script that generates .csv file from GOG Galaxy database file
* .py script that processing .csv file and describes main program logic and .kv design file for GUI
* .spec file to build executable file with PyInstaller

## Resources
[GOG-Galaxy-Export-Script](https://github.com/AB1908/GOG-Galaxy-Export-Script) — A script which generates a .csv file containing your GOG Galaxy Database. To be more specific I used and slightly edited a script from this [pull request](https://github.com/AB1908/GOG-Galaxy-Export-Script/pull/38)

[Random Galaxy Game launcher](https://gist.github.com/maxwellainatchi/794d22c2c24f98d5dc8e6abc7ccc8a92#file-random-galaxy-game-bat) — .bat script that opens a random game page in GOG Galaxy library. Basically, I used the last line of this script in my code

## HOW TO INSTALL
1. Download and install [Python 3.1.9 (32bit)](https://www.python.org/downloads/release/python-391/). Don't forget to set a checkbox "Add Python 3.9 to PATH" during installation.
2. Download this repository and unpack it to any folder. 
3. Open the unpacked folder, hit `Alt`+`D` to highlight an address bar (or `CTRL`+`L`), type in `cmd` and hit `Enter`. Run the following command: `pip install -r requirements.txt`. Wait until everything is installed.
4. Run the following command: `pyinstaller RandomGamePicker.spec` and wait till PyInstaller finishes compiling the program.
5. After previous Step is done, there should be a `dist` folder. Inside it you'll see a `Random Game Picker` folder. This is your compiled program folder. If you want you can move it to any other location.

> **IMPORTANT!** If you've already installed previous version of Random Game Picker, before proceeding to Step 6 you need to delete old parameters file. In order to so, follow the next steps:
> 1. Press `WIN`+`R` to open the run dialog box.
> 2. Copy and paste the following string `%HOMEPATH%\AppData\Local`
> 3. In opened File Explorer window find "Random Game Picker" folder and delete it.
> - Alternatively you can run `delete_old_param_file.bat` from the program main folder. You will need to confirm a deletion.

6. Run the `Random Game Picker.exe` file inside `Random Game Picker` folder to launch the program.

### UNINSTALL PYTHON AND MODULES (OPTIONAL)
If you want to uninstall all modules installed during installation Steps, open Command Prompt in folder from Step 2 and run: `pip uninstall -r requirements.txt -y`

To uninstall Python use Control Panel.

## Additional info
1. .spec file was meant to be used with PyInstaller `--onedir` command-line argument. If you want to create a standalone executable using `--onefile` argument, you'll need to create a different .spec file.
2. PyInstaller officially supports Python 3.7 and lower, though I built an executable with Python 3.9
3. You may want to recompile a [bootloader](https://stackoverflow.com/a/52054580/10873426) for PyInstaller.
