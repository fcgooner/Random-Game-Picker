import kivy
from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
import csv
import galaxy_library_export
import locale
import natsort
import os
import pathlib
import random
import shutil
import subprocess
import sys


#Get program data path to store GameDB.csv and params.ini
def_path = 'C:' + os.getenv('HOMEPATH') + '\AppData\Local\Random Game Picker'

#Check if def_path exists. Create if necessary
os.makedirs(def_path, exist_ok=True)

#Define params.ini pathfile
param_file_path = def_path + '/params.ini'

#Check if params.ini exists. Create if necessary
if not os.path.exists(param_file_path):
    f = open(param_file_path, "w")
    # Check user's region to set localization parameters
    if locale.getdefaultlocale()[0] == 'uk_UA':
        f.write("DEFAULT_LANGUAGE=UA\nHIDDEN_FLAG=False\nWINDOW_SIZE=REGULAR\nEXCLUDED_TAGS=\nINCLUDED_TAGS=")
    else:
        f.write("DEFAULT_LANGUAGE=EN\nHIDDEN_FLAG=False\nWINDOW_SIZE=REGULAR\nEXCLUDED_TAGS=\nINCLUDED_TAGS=")

# Read params.ini to set app language and default/user values 
with open(param_file_path) as f: 
    lines = f.readlines()

global_lang = lines[0].replace("DEFAULT_LANGUAGE=", '')[0:2]

# Set hidden_checkbox_active with new values from params.ini
if lines[1].replace("HIDDEN_FLAG=", '') == "True":
    hidden_checkbox_active = True
else:
    hidden_checkbox_active = False

# Set window size
if lines[2].replace("WINDOW_SIZE=",'').replace("\n",'') == "REGULAR":
    app_width, app_height = 850, 650
    current_window_size = "REGULAR"
else: 
    app_width, app_height = 650, 487
    current_window_size = "SMALL"
    
current_tags_excluded = lines[3].replace("EXCLUDED_TAGS=", '').replace("\n", '')
current_tags_included = lines[4].replace("INCLUDED_TAGS=", '').replace("\n", '')

# Format tags for further use
def format_tags(tags):
    if tags:
        user_tags = tags.strip('][').split(', ')
        for tag in range(0, len(user_tags)):
            user_tags[tag] = user_tags[tag].strip("'").upper()
    else:
        user_tags = []

    return user_tags

# Help popup
class HelpPopup(Popup):

    global global_lang
    global current_window_size
    
    app_help_size = current_window_size
    help_popup_lang = global_lang
    
    help_element_sizes = {
        "REGULAR": {
                    "popup_fontsize": 18},
        "SMALL": {
                    "popup_fontsize": 14}
    }
    
    help_popup_text_localization = {
        "UA":[
"""[color=c28400][u]МІТКИ (TAGS)[/u]:[/color]
Щоб виключити з пошуку ігри з певними мітками (tags),
зазначте їх через кому в полі [color=936899]ВИКЛЮЧИТИ ІГРИ З
НАСТУПНИМИ МІТКАМИ[/color] та натисніть [color=936899]Enter[/color], щоб застосувати зміни.\n
Щоб шукати ігри лише з певними мітками, зазначте їх через
кому в полі [color=936899]ШУКАТИ ІГРИ ЛИШЕ З НАСТУПНИМИ МІТКАМИ[/color]
та натисніть [color=936899]Enter[/color], щоб застосувати зміни.\n
[u]ПРИМІТКА[/u]: Виключені мітки мають вищий пріоритет.
Наприклад, якщо гра має мітку «МОЯ МІТКА», і ви зазначили її
в обох полях, така гра не буде обрана.\n
[color=c28400][u]ПРИХОВАНІ ІГРИ[/u]:[/color]
Початкові налаштування програми не беруть до уваги ігри, які
ви приховали з вашої бібліотеки. Якщо ви хочете, щоб програма
враховувала їх під час вибору гри, активуйте прапорець
[color=936899]ВКЛЮЧИТИ ПРИХОВАНІ ІГРИ[/color].\n
[color=c28400][u]РОЗМІР ВІКНА ПРОГРАМИ[/u]:[/color]
Якщо ви змінили розмір вікна, перезапустіть програму, щоб
зміни набули чинності.\n"""
],
        "EN":[
"""[color=c28400][u]TAGS[/u]:[/color]
To exclude games with specific tags from the search, type the tags
(separated by commas) into the [color=936899]EXCLUDE GAMES WITH TAGS[/color] field
and press [color=936899]Enter[/color] to apply changes.\n
To search games only with specific tags, type the tags (separated by
commas) into the [color=936899]SEARCH GAMES ONLY WITH THE NEXT TAGS[/color]
field and press [color=936899]Enter[/color] to apply changes.\n
[u]NOTE[/u]: Excluded tags have higher priority. For example, if a game
has attached tag "MY TAG" and you've set it in both fields, the game
won't be picked.\n
[color=c28400][u]HIDDEN GAMES[/u]:[/color]
By default, when picking a game, the program doesn't include games
that are hidden from your library. If you want to include hidden
games, activate the [color=936899]INCLUDE HIDDEN GAMES[/color] checkbox.\n
[color=c28400][u]WINDOW SIZE[/u]:[/color]
If you've changed window size, you need to restart the program to
apply changes.\n
"""
]
    }
    # Update popup windwow after language change
    def update_help_popup(self, language):
        self.ids.help_popup.text = self.help_popup_text_localization[language][0]

# About popup
class AboutPopup(Popup):

    global global_lang
    global current_window_size

    app_about_size = current_window_size
    about_popup_lang = global_lang

    about_element_sizes = {
        "REGULAR": {
                    "popup_fontsize": 18},
        "SMALL": {
                    "popup_fontsize": 14}
    }

    about_popup_text_localization = {
        "UA":[
"""[color=9e6dc8]RANDOM GAME PICKER[/color] обирає випадкову гру з вашої бібліотеки
GOG Galaxy, включно з іграми зі Steam, EGS та Origin, у разі
якщо у вас увімкнена синхронізація з цими платформами.
_____________________________________________________________________\n
- Проєкт на GitHub:
  [ref=https://github.com/fcgooner/Random-Game-Picker]\
  [u][color=4d41ef]https://github.com/fcgooner/Random-Game-Picker[/color][/u][/ref]\n\n
- Використані сторонні матеріали:\n
    1. Скрипт експорту бази даних GOG Galaxy:
    [ref=https://github.com/AB1908/GOG-Galaxy-Export-Script]\
    [u][color=4d41ef]https://github.com/AB1908/GOG-Galaxy-Export-Script[/color][/u][/ref]\n
    2. Команда відкриття сторінки гри в GOG Galaxy:
    [ref=https://gist.github.com/maxwellainatchi/794d22c2c24f98d5dc8e6abc7ccc8a92]\
    [u][color=4d41ef]https://gist.github.com/maxwellainatchi[/color][/u][/ref]"""],
        "EN":[
"""[color=9e6dc8]RANDOM GAME PICKER[/color] picks a random game from your GOG
Galaxy library including games from Steam, EGS, and Origin if you've
synced these platforms with your GOG Galaxy library.
_____________________________________________________________________\n
- Project on GitHub:
  [ref=https://github.com/fcgooner/Random-Game-Picker]\
  [u][color=4d41ef]https://github.com/fcgooner/Random-Game-Picker[/color][/u][/ref]\n\n
- Used sources:\n
    1. Script for parsing and exporting GOG Galaxy Database:
    [ref=https://github.com/AB1908/GOG-Galaxy-Export-Script]\
    [u][color=4d41ef]https://github.com/AB1908/GOG-Galaxy-Export-Script[/color][/u][/ref]\n
    2. Command to open game page in GOG Galaxy:
    [ref=https://gist.github.com/maxwellainatchi/794d22c2c24f98d5dc8e6abc7ccc8a92]\
    [u][color=4d41ef]https://gist.github.com/maxwellainatchi[/color][/u][/ref]"""]
    }
    # Update popup windwow after language change
    def update_about_popup(self, language):
        self.ids.about_popup.text = self.about_popup_text_localization[language][0]

# Main class
class MyLayout(Widget):
    # import global variables
    global global_lang
    global hidden_checkbox_active
    global current_window_size
    global current_tags_excluded
    global current_tags_included
    
    # Set local variables
    localization = {
        "UA": {
               "default_cover": "images/cover_placeholder_ua.png",
               "pre_title_text": "НАЗВА ГРИ:",
               "pick_button_text": "ОБРАТИ ВИПАДКОВУ ГРУ",
               "view_button_text": "ПЕРЕГЛЯНУТИ ГРУ В GOG GALAXY",
               "help_button_text": "ДОПОМОГА",
               "about_button_text": "ПРО ПРОГРАМУ",
               "hidden_checkbox_text": "ВКЛЮЧИТИ ПРИХОВАНІ ІГРИ",
               "spinner_text": "UA",
               "spinner_window_text": "РОЗМІР ВІКНА",
               "input_exclude_title": "ВИКЛЮЧИТИ ІГРИ З НАСТУПНИМИ МІТКАМИ:",
               "input_include_title": "ШУКАТИ ІГРИ ЛИШЕ З НАСТУПНИМИ МІТКАМИ:",
               "regular_window": "СТАНДАРТ",
               "small_window": "МАЛИЙ"
              },
        "EN": {
               "default_cover": "images/cover_placeholder_en.png",
               "pre_title_text": "GAME TITLE:",
               "pick_button_text": "PICK A RANDOM GAME",
               "view_button_text": "VIEW GAME IN GOG GALAXY",
               "help_button_text": "HELP",
               "about_button_text": "ABOUT",
               "hidden_checkbox_text": "INCLUDE HIDDEN GAMES",
               "spinner_text": "EN",
               "spinner_window_text": "WINDOW SIZE",
               "input_exclude_title": "EXCLUDE GAMES WITH TAGS:",
               "input_include_title": "SEARCH GAMES ONLY WITH THE NEXT TAGS:",
               "regular_window": "REGULAR",
               "small_window": "SMALL"
              }
    }

    game_data = {
                 "title": 0,
                 "tags": 1,
                 "is_hidden": 2,
                 "icon": 3,
                 "cover": 4,
                 "gog_link": 5
    }
    
    # Define app formating based on window size
    element_sizes = {
        "REGULAR": {
                    "header_fontsize": 46,
                    "pretitle_fontsize": 20,
                    "title_fontsize": 30,
                    "checkbox_fontsize": 15,
                    "pick_button_fontsize": 26,
                    "view_button_fontsize": 20,
                    "help_fontsize": 14,
                    "about_fontsize": 14,
                    "spinner_fontsize": 15,
                    "hidden_text_size": (400, 20),
                    "pretitle_textsize" : (150, 20),
                    "title_textsize" : (464, 150),
                    "exc_inc_text_fontsize": 18,
                    "exc_inc_textsize": (500, 50),
                    "exc_inc_input_fontsize": 18,
                    "checkbox_pos": {"x": 0.43, "center_y": 0.33}
                   },
        "SMALL": {
                    "header_fontsize": 35,
                    "pretitle_fontsize": 15,
                    "title_fontsize": 25,
                    "checkbox_fontsize": 12,
                    "pick_button_fontsize": 23,
                    "view_button_fontsize": 17,
                    "help_fontsize": 12,
                    "about_fontsize": 12,
                    "spinner_fontsize": 11,
                    "hidden_text_size": (300, 15),
                    "pretitle_textsize" : (120, 15),
                    "title_textsize" : (357, 100),
                    "exc_inc_text_fontsize": 13,
                    "exc_inc_textsize": (381, 40),
                    "exc_inc_input_fontsize": 12,
                    "checkbox_pos": {"x": 0.434, "center_y": 0.33}
                 }
    }
    
    cover_present = False
    current_lang = global_lang
    app_size = current_window_size
    font_latothin = "fonts/Lato-Thin.ttf"
    font_latoreg = "fonts/Lato-Regular.ttf"
    include_hidden_games = hidden_checkbox_active
    pick_button_is_pressed = False
    picked_game_cover = localization[current_lang]["default_cover"]
    picked_game_title = ""
    picked_game_link = ""
    picked_games = []
    tags_excluded = current_tags_excluded
    tags_included = current_tags_included

    # Behaviour when PICK A RANDOM GAME button is pressed
    def pick_button_pressed(self):
        # import global variables
        global current_tags_excluded
        global current_tags_included
        global hidden_checkbox_active

        user_excl_tags = format_tags(current_tags_excluded)
        user_incl_tags = format_tags(current_tags_included)
        
        # Set GOG Galaxy games database filepath
        game_db = "C:" + os.getenv('HOMEPATH') + '\AppData\Local\Random Game Picker\GameDB.csv'
        
        with open(game_db, 'r', encoding='utf-8') as csv_file:
            csv_reader = list(csv.reader(csv_file))
        
        games_number = 0    
        for lines in list(csv_reader)[1:]:
            games_number += 1

        csv_loop = True
        while csv_loop:
            # Pick a random game
            chosen_row = random.choice(list(csv_reader)[1:])
            print("Picked game: ", chosen_row[self.game_data["title"]])
            print("Hidden status: ", chosen_row[self.game_data["is_hidden"]])
            
            # Check if game wasn't already picked
            if not chosen_row[self.game_data["title"]] in self.picked_games:
                self.picked_games.append(chosen_row[self.game_data["title"]])
                
                # Exclude game if it doesn't have an icon image
                if chosen_row[self.game_data["icon"]]:
                    game_tags = format_tags(chosen_row[self.game_data["tags"]])
                    print('Game tags: %s | Excluded tags: %s | Included tags: %s' % (game_tags, user_excl_tags, user_incl_tags))
                    
                    # Check if game has no excluded tags
                    if set(game_tags).isdisjoint(user_excl_tags):

                        # Check if INCLUDE HIDDEN GAMES checkbox is set
                        if hidden_checkbox_active:
                        
                            # Check if user defined include tags
                            if not user_incl_tags:
                                self.update_game_data(chosen_row)
                                csv_loop = False
                            else:
                                # Check if game has user-defined incude tags
                                if not set(game_tags).isdisjoint(user_incl_tags):
                                    self.update_game_data(chosen_row)
                                    csv_loop = False
                        else:
                            if chosen_row[self.game_data["is_hidden"]] == "False":
                                # Check if user defined include tags
                                if not user_incl_tags:
                                    self.update_game_data(chosen_row)
                                    csv_loop = False
                                else:
                                    # Check if game has user-defined incude tags
                                    if not set(game_tags).isdisjoint(user_incl_tags):
                                        self.update_game_data(chosen_row)
                                        csv_loop = False
            
            print("Games count: ", len(self.picked_games), "\n")
            # Check to exit the loop if there are no more games to pick
            if games_number == len(self.picked_games):
                print("There are no more games! Starting a new search loop\n")
                # Clear list of picked games to start a new loop
                self.picked_games = []
                csv_loop = False

    # Update the main window with picked game data
    def update_game_data(self, data):
        self.picked_game_title = data[self.game_data["title"]]
        self.picked_game_link = data[self.game_data["gog_link"]][2:].split("'")[0]
        if data[self.game_data["cover"]]:
            self.picked_game_cover = data[self.game_data["cover"]]
            self.cover_present = True
        else:
            self.picked_game_cover = self.localization[self.current_lang]["default_cover"]
            self.cover_present = False
            
        self.update_game_title(self.picked_game_title)
        self.update_game_cover(self.picked_game_cover)
        self.pick_button_is_pressed = True


    def update_game_title(self, game_title):
        self.ids.game_title.text = game_title


    def update_game_cover(self, game_cover):
        self.ids.cover_image.source = game_cover
        
    # Update localization 
    def update_program_localization(self):
        if not self.pick_button_is_pressed:
            self.ids.cover_image.source = self.localization[self.current_lang]["default_cover"]  
        elif self.pick_button_is_pressed:
            if not self.cover_present:
                self.ids.cover_image.source = self.localization[self.current_lang]["default_cover"]
                    
        self.ids.title_text.text = self.localization[self.current_lang]["pre_title_text"]
        
        self.ids.pick_button.text = self.localization[self.current_lang]["pick_button_text"]
        self.ids.open_button.text = self.localization[self.current_lang]["view_button_text"]
        
        self.ids.help_button.text = self.localization[self.current_lang]["help_button_text"]
        self.ids.about_button.text = self.localization[self.current_lang]["about_button_text"]
        
        self.ids.hidden_text.text = self.localization[self.current_lang]["hidden_checkbox_text"]
        self.ids.language_spinner.text = self.localization[self.current_lang]["spinner_text"]
        self.ids.windows_size_spinner.text = self.localization[self.current_lang]["spinner_window_text"]

        self.ids.exclude_input.text = self.localization[self.current_lang]["input_exclude_title"]
        self.ids.include_input.text = self.localization[self.current_lang]["input_include_title"]
        self.ids.windows_size_spinner.values = self.localization[self.current_lang]["regular_window"], self.localization[self.current_lang]["small_window"]

    # Behaviour when the VIEW GAME IN GOG GALAXY button is pressed    
    def view_button_pressed(self):
        if self.picked_game_link:
            subprocess.run("start goggalaxy://openGameView/" + self.picked_game_link, shell=True)


    def set_program_language(self, language):
        global global_lang
        if language == "EN":
            lang_Code = "EN"
        else:
            lang_Code = "UA"
            
        if self.current_lang != lang_Code:
            self.current_lang = lang_Code
            global_lang = lang_Code
            self.update_program_localization()
            
    
    def hidden_checkbox(self, instance, value):
        global hidden_checkbox_active
        hidden_checkbox_active = value
        self.include_hidden_games = value
        
        
    def change_window_size(self, window_size):
        global current_window_size
        with open(param_file_path) as f: 
            lines = f.readlines()

        if window_size == "МАЛИЙ" or window_size == "SMALL":
            lines[2] = "WINDOW_SIZE=SMALL\n"
            app_size = current_window_size = "SMALL"
        elif window_size == "СТАНДАРТ" or window_size == "REGULAR":
            lines[2] = "WINDOW_SIZE=REGULAR\n"
            app_size = current_window_size = "REGULAR"
        
        with open(param_file_path, "w") as f: 
            f.writelines(lines)
            
            
    def update_excluded_tags(self, tags):
        global current_tags_excluded
        self.tags_excluded = tags
        current_tags_excluded = self.tags_excluded

        
    def update_included_tags(self, tags):
        global current_tags_included
        self.tags_included = tags
        current_tags_included = self.tags_included

    
class RandomGamePicker(App):
    global app_height
    global app_width
    # Set the program main window parameters
    def build(self):
        Window.size = (app_width, app_height)
        self.icon = 'images/app.ico'
        self.title = "Random Game Picker"
        return MyLayout()
        
    # Create games database    
    def on_start(self):
        # Create cvs file for user library
        sys.argv = ['galaxy_library_export.py', '-d=,', '--py-lists', '--image-square', '--image-vertical', '--platforms', '--hidden', '--tags']
        galaxy_library_export.main()
        
    # Behaviour while the program is closing
    def on_stop(self):
        global global_lang
        global hidden_checkbox_active
        global param_file_path
        global current_tags_excluded
        global current_tags_included
        
        # Read current language
        with open(param_file_path) as f: 
            lines = f.readlines()
        
        # Write new values to param.ini
        lines[0] = "DEFAULT_LANGUAGE=" + global_lang + "\n"
                
        if lines[1].replace("HIDDEN_FLAG=", '') == "True":
            def_hidden = True
        else:
            def_hidden = False

        lines[1] = "HIDDEN_FLAG=" + str(hidden_checkbox_active) + "\n"
        lines[3] = "EXCLUDED_TAGS=" + current_tags_excluded + "\n"
        lines[4] = "INCLUDED_TAGS=" + current_tags_included + "\n"

        with open(param_file_path, "w") as f: 
            f.writelines(lines)


if __name__ == '__main__':
    RandomGamePicker().run()