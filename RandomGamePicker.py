import kivy
from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.popup import Popup
import os
import subprocess
import csv
import random
import natsort
import sys
import galaxy_library_export
import shutil
import pathlib
import locale

def_path = os.getenv('HOMEPATH') + '\AppData\Local\Random Game Picker'
os.makedirs(def_path, exist_ok=True)
param_file_path = def_path + '\\params.ini'
#old_param = os.getcwd() + '\\params.ini'

if not os.path.exists(param_file_path):
    #shutil.copy(old_param, def_path)
    f = open(param_file_path, "w")
    if locale.getdefaultlocale()[0] == 'uk_UA':
        f.write("DEFAULT_LANGUAGE=UA\nHIDDEN_FLAG=False")
    else:
        f.write("DEFAULT_LANGUAGE=EN\nHIDDEN_FLAG=False")


with open(param_file_path) as f: 
    lines = f.readlines() #read
                
app_lang_global = lines[0].replace("DEFAULT_LANGUAGE=", '')[0:2]
if lines[1].replace("HIDDEN_FLAG=", '') == "True":
    hidden_flag = True
else:
    hidden_flag = False


class HelpPopup(Popup):

    global app_lang_global
    default_picker = app_lang_global
    
    help_text = {
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
    
    def updatePopup(self, picker):
        self.ids.help_title.text = self.help_text[picker][0]


class AboutPopup(Popup):

    global app_lang_global
    default_picker = app_lang_global
    
    about_text = {
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
    about_pop_title = {
        # index 4 is for PICK A GAME button font size
        "UA": "ПРО ПРОГРАМУ",
        "EN": "ABOUT"}
    
    def updateAbout(self, picker):
        self.ids.about_title.text = self.about_text[picker][0]
        self.ids.about_title.title = self.about_pop_title[picker]


class MyLayout(Widget):
    global app_lang_global
    global hidden_flag
    current_lang = app_lang_global
    show_hidden = hidden_flag
    
    latothin = "fonts/Lato-Thin.ttf"
    latoreg = "fonts/Lato-Regular.ttf"
    pick_button_pressed = False
    
    localization_dict = {
        # index 4 is for PICK A GAME button font size
        "UA": ["images/cover_placeholder_ua.png", "НАЗВА ГРИ: ", "ОБРАТИ ВИПАДКОВУ ГРУ", "ПЕРЕГЛЯНУТИ ГРУ В GOG GALAXY", 23, 17, "ДОПОМОГА", "ПРО ПРОГРАМУ", "ВКЛЮЧИТИ ПРИХОВАНІ ІГРИ"],
        "EN": ["images/cover_placeholder_en.png", "GAME TITLE: ", "PICK A RANDOM GAME", "VIEW GAME IN GOG GALAXY", 26, 21, "HELP", "ABOUT", "INCLUDE HIDDEN GAMES"]
    }
    loc_button_size = {
        # index 4 is for PICK A GAME button font size
        "UA": [32, 96, 118],
        "EN": [32, 46, 58]
    }
    loc_button_pos = {
        # index 4 is for PICK A GAME button font size
        
        "UA": [{"right": 0.204, "top": 0.09}, {"right": 0.423, "top": 0.09}],
        "EN": [{"right": 0.12, "top": 0.09}, {"right": 0.24, "top": 0.09}]
    }
    
    picked_game_cover = localization_dict[current_lang][0]
    picked_game_title = ""
    picked_game_link = ""
    cover_present = False
    # galaxy_link = "goggalaxy://openGameView/"
    
#python galaxy_library_export.py -d , --py-lists --image-square --image-vertical --platforms
    
    def pickPress(self):

        global hidden_flag
        game_db = os.getenv('HOMEPATH') + '\AppData\Local\Random Game Picker\GameDB.csv'
        with open(game_db, 'r') as csv_file:
            csv_reader = list(csv.reader(csv_file))
        
        csv_loop = True
        while csv_loop:
            #lengthofcsv = len(csv_reader)
            #position = random.randrange(1, lengthofcsv)
            chosen_row = random.choice(list(csv_reader)[1:])
            #print("picked games is: " + chosen_row[0])
            if chosen_row[2]:
                if hidden_flag:
                    csv_loop = self.updateGame(chosen_row)
                else:
                    if chosen_row[1] == "False":
                        csv_loop = self.updateGame(chosen_row)


    def updateGame(self, chosen_row):
        self.picked_game_title = chosen_row[0].replace("в„ў", "")
        self.picked_game_link = chosen_row[4][2:].split("'")[0]
        if chosen_row[3]:
            self.picked_game_cover = chosen_row[3]
            self.cover_present = True
        else:
            self.picked_game_cover = self.localization_dict[self.current_lang][0]
            self.cover_present = False
            
        self.updateTitle(self.picked_game_title)
        self.updateCover(self.picked_game_cover)
        self.pick_button_pressed = True
        
        return False
        
        
    def updateTitle(self, game_title):
        self.ids.game_title.text = game_title


    def updateCover(self, game_cover):
        self.ids.cover_image.source = game_cover
        
        
    def updateLang(self):
    
        if not self.pick_button_pressed:
            self.ids.cover_image.source = self.localization_dict[self.current_lang][0]  
        elif self.pick_button_pressed:
            if not self.cover_present:
                self.ids.cover_image.source = self.localization_dict[self.current_lang][0]
                    
        self.ids.title_text.text = self.localization_dict[self.current_lang][1]
        
        self.ids.pick_button.text = self.localization_dict[self.current_lang][2]
        self.ids.open_button.text = self.localization_dict[self.current_lang][3]
        
        self.ids.pick_button.font_size = self.localization_dict[self.current_lang][4]
        self.ids.open_button.font_size = self.localization_dict[self.current_lang][5]
        
        self.ids.help_button.text = self.localization_dict[self.current_lang][6]
        self.ids.about_button.text = self.localization_dict[self.current_lang][7]
        
        self.ids.help_button.pos_hint = self.loc_button_pos[self.current_lang][0]
        self.ids.about_button.pos_hint = self.loc_button_pos[self.current_lang][1]

        self.ids.help_button.height = self.loc_button_size[self.current_lang][0]
        self.ids.help_button.width = self.loc_button_size[self.current_lang][1]
        
        self.ids.about_button.height = self.loc_button_size[self.current_lang][0]
        self.ids.about_button.width = self.loc_button_size[self.current_lang][2]
        
        self.ids.hidden_text.text = self.localization_dict[self.current_lang][8]

        
    def openPress(self):
        self.openGog(self.picked_game_link)
            
            
    def openGog(self, game_link):
        if game_link:
            subprocess.run("start goggalaxy://openGameView/" + game_link, shell=True)


    def langChange(self, lang_Code):
        global app_lang_global
        if self.current_lang != lang_Code:
            self.current_lang = lang_Code
            app_lang_global = lang_Code
            self.updateLang()
            
    
    def hidden_checkbox(self, instance, value):
        global hidden_flag
        hidden_flag = value
        self.show_hidden = value
            
    
class RandomGamePicker(App):

    #set app window size
    def build(self):
        self.title = "Random Game Picker"
        Window.size = (600, 450)
        self.icon = 'images/app.ico'
        return MyLayout()
        
    #create games database    
    def on_start(self):
        #subprocess.run("python galaxy_library_export.py -d , --py-lists --image-square --image-vertical --platforms --hidden", shell=True)
        sys.argv = ['galaxy_library_export.py', '-d=,', '--py-lists', '--image-square', '--image-vertical', '--platforms', '--hidden' ]
        galaxy_library_export.main()
        
    #Remember default language
    def on_stop(self):
        global app_lang_global
        global hidden_flag
        global param_file_path
        
        # Read current default language
        with open(param_file_path) as f: 
            lines = f.readlines() #read 

        def_lang = lines[0].replace("DEFAULT_LANGUAGE=", '')[0:2]
        if lines[1].replace("HIDDEN_FLAG=", '') == "True":
            def_hidden = True
        else:
            def_hidden = False       
        
        # Change default language if it differs from current app language 
        if def_lang != app_lang_global:
            lines[0] = "DEFAULT_LANGUAGE=" + app_lang_global + "\n"
            with open(param_file_path, "w") as f: 
                f.writelines(lines) #write back 

        # Change default state of checkbox if it differs from current state 
        if def_hidden != hidden_flag:
            lines[1] = "HIDDEN_FLAG=" + str(hidden_flag)
            with open(param_file_path, "w") as f: 
                f.writelines(lines) #write back 
        
        


if __name__ == '__main__':
    RandomGamePicker().run()