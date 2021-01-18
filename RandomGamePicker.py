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
    # Check user's region to write localization parameters
    if locale.getdefaultlocale()[0] == 'uk_UA':
        f.write("DEFAULT_LANGUAGE=UA\nHIDDEN_FLAG=False")
    else:
        f.write("DEFAULT_LANGUAGE=EN\nHIDDEN_FLAG=False")

# Read params.ini to set app language and user preferences 
with open(param_file_path) as f: 
    lines = f.readlines()

global_lang = lines[0].replace("DEFAULT_LANGUAGE=", '')[0:2]

# Set hidden_checkbox_active with new values from params.ini
if lines[1].replace("HIDDEN_FLAG=", '') == "True":
    hidden_checkbox_active = True
else:
    hidden_checkbox_active = False

# Help popup
class HelpPopup(Popup):

    global global_lang
    help_popup_lang = global_lang
    
    help_popup_text_localization = {
        "UA":[
"""- [color=9e6dc8]Random Game Picker[/color] обирає випадкову гру з вашої
  бібліотеки GOG Galaxy, включно з іграми зі Steam, EGS та
  Origin, у разі якщо у вас увімкнена синхронізація з цими
  платформами.\n
- Щоб обрати випадкову гру натисніть кнопку
  [color=936899]ОБРАТИ ВИПАДКОВУ ГРУ[/color].\n
- Щоб переглянути обрану гру в GOG Galaxy натисніть
  кнопку [color=936899]ПЕРЕГЛЯНУТИ ГРУ В GOG GALAXY[/color].\n
- Початкові налаштування програми не беруть до уваги
  ігри, які ви приховали з вашої бібліотеки. Якщо ви
  хочете, щоб програма враховувала їх під час вибору
  гри, активуйте прапорець [color=936899]ВКЛЮЧИТИ ПРИХОВАНІ ІГРИ[/color].\n
- Якщо програма не працює пересвідчіться, що у вас
  присутній файл galaxy-2.0.db за наступним шляхом:
  C:\ProgramData\GOG.com\Galaxy\storage"""
],
        "EN":[
"""- [color=9e6dc8]Random Game Picker[/color] picks a random game from your GOG
  Galaxy library including games from Steam, EGS, and Origin if
  you've synced these platforms with your GOG Galaxy library.\n
- To pick a random game press the [color=936899]PICK A RANDOM GAME[/color]
  button.\n
- To view a selected game in GOG Galaxy press the
  [color=936899]VIEW GAME IN GOG GALAXY[/color] button.\n
- By default, when picking a game, the program doesn't include
  games that are hidden from your library. If you want to
  include hidden games, activate the [color=936899]INCLUDE HIDDEN GAMES[/color]
  checkbox.\n
- If the program is not working, make sure that you have a
  galaxy-2.0.db file inside the following path:
  C:\ProgramData\GOG.com\Galaxy\storage"""]
    }
    # Update popup windwow after language change
    def update_help_popup(self, language):
        self.ids.help_popup.text = self.help_popup_text_localization[language][0]

# About popup
class AboutPopup(Popup):

    global global_lang
    about_popup_lang = global_lang
    
    about_popup_text_localization = {
        "UA":[
"""- Розробник: [color=51c8e0]RGM[/color] || Створено в 2021 р.\n\n
- Використані сторонні ресурси:\n
  1. Скрипт експорту бази даних GOG Galaxy:
     [ref=https://github.com/AB1908/GOG-Galaxy-Export-Script][color=4d41ef]https://github.com/AB1908/GOG-Galaxy-Export-Script[/color][/ref]\n
  2. Команда відкриття сторінки гри в GOG Galaxy:
     [ref=https://gist.github.com/maxwellainatchi/794d22c2c24f98d5dc8e6abc7ccc8a92][color=4d41ef]https://gist.github.com/maxwellainatchi[/color][/ref]"""],
        "EN":[
"""- Created by: [color=51c8e0]fc_gooner[/color] in 2021\n\n
- Used sources:\n
  1. Script for parsing and exporting GOG Galaxy Database:
     [ref=https://github.com/AB1908/GOG-Galaxy-Export-Script][color=4d41ef]https://github.com/AB1908/GOG-Galaxy-Export-Script[/color][/ref]\n
  2. Command to open game page in GOG Galaxy:
     [ref=https://gist.github.com/maxwellainatchi/794d22c2c24f98d5dc8e6abc7ccc8a92][color=4d41ef]https://gist.github.com/maxwellainatchi[/color][/ref]"""]
    }
    # Update popup windwow after language change
    def update_about_popup(self, language):
        self.ids.about_popup.text = self.about_popup_text_localization[language][0]

# Main class
class MyLayout(Widget):
    # import global variables
    global global_lang
    global hidden_checkbox_active
    # Set local variables
    localization = {
        # index 4 is for PICK A GAME button font size
        "UA": ["images/cover_placeholder_ua.png",
               "НАЗВА ГРИ:",
               "ОБРАТИ ВИПАДКОВУ ГРУ",
               "ПЕРЕГЛЯНУТИ ГРУ В GOG GALAXY",
               23,
               17,
               "ДОПОМОГА",
               "ПРО ПРОГРАМУ",
               "ВКЛЮЧИТИ ПРИХОВАНІ ІГРИ"],
        "EN": ["images/cover_placeholder_en.png",
               "GAME TITLE:",
               "PICK A RANDOM GAME",
               "VIEW GAME IN GOG GALAXY",
               26,
               21,
               "HELP",
               "ABOUT",
               "INCLUDE HIDDEN GAMES"]
    }
    
    loc_button_pos = {
        "UA": [
               {"right": 0.204, "top": 0.09},
               {"right": 0.423, "top": 0.09}
              ],
        "EN": [
               {"right": 0.12, "top": 0.09},
               {"right": 0.24, "top": 0.09}
              ]
    }
    
    loc_button_size = {
        "UA": [32, 96, 118],
        "EN": [32, 46, 58]
    }
    
    cover_present = False
    current_lang = global_lang
    font_latothin = "fonts/Lato-Thin.ttf"
    font_latoreg = "fonts/Lato-Regular.ttf"
    include_hidden_games = hidden_checkbox_active
    pick_button_is_pressed = False
    picked_game_cover = localization[current_lang][0]
    picked_game_title = ""
    picked_game_link = ""

    # Behaviour when PICK A RANDOM GAME button is pressed
    def pick_button_pressed(self):
        # import global variables
        global hidden_checkbox_active
        # Save GOG Galaxy games database filepath
        game_db = "C:" + os.getenv('HOMEPATH') + '\AppData\Local\Random Game Picker\GameDB.csv'
        
        with open(game_db, 'r', encoding='utf-8') as csv_file:
            csv_reader = list(csv.reader(csv_file))
        
        csv_loop = True
        while csv_loop:
            chosen_row = random.choice(list(csv_reader)[1:])
            # Exclude game if it doesn't have an icon image
            if chosen_row[2]:
                # Check if INCLUDE HIDDEN GAMES checkbox is set
                if hidden_checkbox_active:
                    csv_loop = self.update_game_data(chosen_row)
                else:
                    if chosen_row[1] == "False":
                        csv_loop = self.update_game_data(chosen_row)

    # Update the program main window with picked game data
    def update_game_data(self, game_data):
        self.picked_game_title = game_data[0]
        self.picked_game_link = game_data[4][2:].split("'")[0]
        if game_data[3]:
            self.picked_game_cover = game_data[3]
            self.cover_present = True
        else:
            self.picked_game_cover = self.localization[self.current_lang][0]
            self.cover_present = False
            
        self.update_game_title(self.picked_game_title)
        self.update_game_cover(self.picked_game_cover)
        self.pick_button_is_pressed = True


    def update_game_title(self, game_title):
        self.ids.game_title.text = game_title


    def update_game_cover(self, game_cover):
        self.ids.cover_image.source = game_cover
        
    # Update the program language    
    def update_program_localization(self):
        if not self.pick_button_is_pressed:
            self.ids.cover_image.source = self.localization[self.current_lang][0]  
        elif self.pick_button_is_pressed:
            if not self.cover_present:
                self.ids.cover_image.source = self.localization[self.current_lang][0]
                    
        self.ids.title_text.text = self.localization[self.current_lang][1]
        
        self.ids.pick_button.text = self.localization[self.current_lang][2]
        self.ids.open_button.text = self.localization[self.current_lang][3]
        
        self.ids.pick_button.font_size = self.localization[self.current_lang][4]
        self.ids.open_button.font_size = self.localization[self.current_lang][5]
        
        self.ids.help_button.text = self.localization[self.current_lang][6]
        self.ids.about_button.text = self.localization[self.current_lang][7]
        
        self.ids.help_button.pos_hint = self.loc_button_pos[self.current_lang][0]
        self.ids.about_button.pos_hint = self.loc_button_pos[self.current_lang][1]

        self.ids.help_button.height = self.loc_button_size[self.current_lang][0]
        self.ids.help_button.width = self.loc_button_size[self.current_lang][1]
        
        self.ids.about_button.height = self.loc_button_size[self.current_lang][0]
        self.ids.about_button.width = self.loc_button_size[self.current_lang][2]
        
        self.ids.hidden_text.text = self.localization[self.current_lang][8]

    # Behaviour when the VIEW GAME IN GOG GALAXY button is pressed    
    def view_button_pressed(self):
        if self.picked_game_link:
            subprocess.run("start goggalaxy://openGameView/" + self.picked_game_link, shell=True)


    def set_program_language(self, lang_Code):
        global global_lang
        if self.current_lang != lang_Code:
            self.current_lang = lang_Code
            global_lang = lang_Code
            self.update_program_localization()
            
    
    def hidden_checkbox(self, instance, value):
        global hidden_checkbox_active
        hidden_checkbox_active = value
        self.include_hidden_games = value
            
    
class RandomGamePicker(App):

    # Set the program main window parameters
    def build(self):
        self.title = "Random Game Picker"
        Window.size = (600, 450)
        self.icon = 'images/app.ico'
        return MyLayout()
        
    # Create games database    
    def on_start(self):
        sys.argv = ['galaxy_library_export.py', '-d=,', '--py-lists', '--image-square', '--image-vertical', '--platforms', '--hidden']
        galaxy_library_export.main()
        
    # Behaviour after the program is closed
    def on_stop(self):
        global global_lang
        global hidden_checkbox_active
        global param_file_path
        
        # Read current language
        with open(param_file_path) as f: 
            lines = f.readlines()
        
        if lines[1].replace("HIDDEN_FLAG=", '') == "True":
            def_hidden = True
        else:
            def_hidden = False

        # Change default state of checkbox if it differs from current state 
        if def_hidden != hidden_checkbox_active:
            lines[1] = "HIDDEN_FLAG=" + str(hidden_checkbox_active)
            with open(param_file_path, "w") as f: 
                f.writelines(lines) #write back 
        
        def_lang = lines[0].replace("DEFAULT_LANGUAGE=", '')[0:2]
        # Change default language if it differs from current program language 
        if def_lang != global_lang:
            lines[0] = "DEFAULT_LANGUAGE=" + global_lang + "\n"
            with open(param_file_path, "w") as f: 
                f.writelines(lines)


if __name__ == '__main__':
    RandomGamePicker().run()