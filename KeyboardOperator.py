import os
from telebot import types

class KeyboardOperator:

    def __init__(self, noteDirPath):
        
        self.markup=None

        self.inline_markup_menu=None

        self.path = noteDirPath

        self.markup_init()

    def markup_init(self):
        
        self.markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        item1=types.KeyboardButton("Старт")
        item2=types.KeyboardButton("Заметки")
        item3=types.KeyboardButton("Расписание на сегодня")
        item4=types.KeyboardButton("Расписание на завтра")

        self.markup.add(item1, item2).add(item3, item4)

        self.inline_markup_menu = types.InlineKeyboardMarkup(row_width=2)

        menu1=types.InlineKeyboardButton("Написать заметку", callback_data="Написать заметку")
        menu2=types.InlineKeyboardButton("Прочитать заметку", callback_data="Прочитать заметку")
        menu3=types.InlineKeyboardButton("Добавить заметку", callback_data="Добавить заметку")
        menu4=types.InlineKeyboardButton("Удалить заметку", callback_data="Удалить заметку")

        self.inline_markup_menu.add(menu1, menu2, menu3, menu4)

    def inlineKeyboard_init(self):
        txt_files = [f for f in os.listdir(self.path) if f.endswith('.txt')]
        files=[]
        for file in txt_files:
            files.append(file.split(".")[0])
        inline_markup = types.InlineKeyboardMarkup(row_width=2)
        for line in range(1, len(files), 2):
            if(files[line]=="FlagCarrier"):
                line+=1
            menu1=types.InlineKeyboardButton(f"{files[line]}", callback_data=f"{files[line]}")
            if(line+1!=len(files)):
                menu2=types.InlineKeyboardButton(f"{files[line+1]}", callback_data=f"{files[line+1]}")
                inline_markup.add(menu1, menu2)
            else:
                inline_markup.add(menu1)

        return inline_markup