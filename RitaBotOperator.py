import telebot, requests, time, threading, asyncio
from datetime import date, timedelta
from telebot import types
from bs4 import BeautifulSoup as BS
import os
from TimeOperator import *


# token = '5760104271:AAGeQlglQvkTiAHEUlCpTrn2NuAl-sAA2X0' # realt bot
# token='6125433165:AAGf3tSiymltFchIuuH0T6F2FdvVV-czzAI' # rita
token='6990977891:AAGFhYZT3dEV4ej1lvD0AKBnuwbWod2UBCA' # test bot
bot = telebot.TeleBot(token)
# @a7sd98Bot


url_KBP='https://kbp.by/rasp/timetable/view_beta_kbp/?page=stable&cat=group&id=53'

headers = {
  "User-Agent":
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

id_=1819018345

path = "BotFiles/"

# path = "BotFiles\\"

sub_disc_list = []

responce = requests.get(url_KBP, headers=headers)
soup=BS(responce.text, "lxml")


markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1=types.KeyboardButton("Старт")
item2=types.KeyboardButton("Заметки")
item3=types.KeyboardButton("Расписание на сегодня")
item4=types.KeyboardButton("Расписание на завтра")
markup.add(item1, item2).add(item3, item4)

inline_markup_menu = types.InlineKeyboardMarkup(row_width=2)
menu1=types.InlineKeyboardButton("Написать заметку", callback_data="Написать заметку")
menu2=types.InlineKeyboardButton("Прочитать заметку", callback_data="Прочитать заметку")
menu3=types.InlineKeyboardButton("Добавить заметку", callback_data="Добавить заметку")
menu4=types.InlineKeyboardButton("Удалить заметку", callback_data="Удалить заметку")
inline_markup_menu.add(menu1, menu2, menu3, menu4)


def up_state(id_, day, f):
  tomorrow = (date.today() + timedelta(days=f)).strftime("%d-%m")

  zameny=soup.find("tr", class_="zamena").find_all("th")
  
  bot.send_message(id_, f"Раписание на {tomorrow}")
  if ("Замен нет" in zameny[day].get_text()):
    bot.send_message(id_, "Замен нет")
  elif (zameny[day].find("label")!=None):
    bot.send_message(id_, "Замены есть")  
  else:
    bot.send_message(id_,"Расписание не обновлено")

def up_state_check(day):

  responce = requests.get(url_KBP, headers=headers)
  soup=BS(responce.text, "lxml")

  zameny=soup.find("tr", class_="zamena").find_all("th")

  if ("Замен нет" in zameny[day].get_text()):
    return "true"
  elif (zameny[day].find("label")!=None):
    return "true"
  else:
    return "false"


def print_schedule(id_, day):

  if(len(get_schedule(day))!=0):
    
    bot.send_message(id_, "\n".join(get_schedule(day)))

  if(len(find_notes(day))!=0):

    bot.send_message(id_, "Заметки:\n"+"".join(find_notes(day)))

def get_schedule(day):

  schedule_list = []
  lesson=soup.find_all("tr")

  for i in range(2, 17):

    subject=lesson[i].find_all("td")

    if (subject[day].find("div", class_="empty-pair")==None or subject[day].find("div", class_=f"pair lw_{day} added")!=None):
      num=subject[0].text
      if(subject[day].find("div", class_=f"pair lw_{day} added")==None):
        sub=subject[day].find("div", class_="subject").find("a").text
        cab=subject[day].find("div", class_="place").find("a").text
        schedule_list.append(f'{num}-{sub} [{cab}]')

      else:
        sub=subject[day].find("div", class_=f"pair lw_{day} added").find("div", class_="subject").find("a").text
        cab=subject[day].find("div", class_=f"pair lw_{day} added").find("div", class_="place").find("a").text
        schedule_list.append(f'{num}-{sub} [{cab}] *') 
        
  return schedule_list

def find_notes(day):

  write_sub_list = []
  lesson=soup.find_all("tr")

  for i in range(2, 17):

    subject=lesson[i].find_all("td")

    if (subject[day].find("div", class_="empty-pair")==None or subject[day].find("div", class_=f"pair lw_{day} added")!=None):

      sub=get_sub_at_day(subject, day)

      if(read_sub_inf(sub)!="null"):
        write_sub_list.append(sub +":\n"+ read_sub_inf(sub)+"\n")  

  write_sub_list = list(set(write_sub_list))
  
  return write_sub_list

def get_sub_at_day(subject, day):

  if(subject[day].find("div", class_=f"pair lw_{day} added")==None):

    return subject[day].find("div", class_="subject").find("a").text
  
  else:
    return subject[day].find("div", class_=f"pair lw_{day} added").find("div", class_="subject").find("a").text


@bot.message_handler(content_types=['text'])
def get_text(message):
  if(message.text=="Заметки"):

    bot.send_message(id_, 'Выберите действие с заметками:', reply_markup=inline_markup_menu)

  if(message.text=="Старт"):

    bot.send_message(id_, 'Привет!', reply_markup=markup)

  if(message.text=="Расписание на сегодня"):

    responce = requests.get(url_KBP, headers=headers)
    soup=BS(responce.text, "lxml")
    week=time.strftime("%A")
    up_state(id_, (int)(time.strftime('%w')), 0)
    print_schedule(id_, (int)(time.strftime('%w')))

  if(message.text=="Расписание на завтра"):
    
    responce = requests.get(url_KBP, headers=headers)
    soup=BS(responce.text, "lxml")
    week=time.strftime("%A")
    up_state(id_, (int)(time.strftime('%w'))+1, 1)
    print_schedule(id_, (int)(time.strftime('%w'))+1)

@bot.callback_query_handler(func=lambda call: True)# ответ на меню заметок
def check_callback_data(call):
  if (call.data=="Написать заметку"):
    write_menu_flag('1')
    bot.send_message(id_, "Выберите облаcть:", reply_markup=inlineKeyboard_init())
  
  elif (call.data=="Прочитать заметку"):
    write_menu_flag('2')
    bot.send_message(id_, "Выберите облаcть:", reply_markup=inlineKeyboard_init())

  elif(call.data=="Добавить заметку"):
    bot.send_message(id_, "Назовите новую облаcть заметок:")
    bot.register_next_step_handler(call.message, new_notes)
  
  elif(call.data=="Удалить заметку"):
    write_menu_flag('3')
    bot.send_message(id_, "Выберите облаcть:", reply_markup=inlineKeyboard_init())

  else:
    if(read_menu_flag()=='1'):
      bot.send_message(id_, "Содержимое заметки:\n")
      bot.send_message(id_, read_sub_inf(call.data))
      bot.send_message(id_, f"Напишите заметку на {call.data}:")
      bot.register_next_step_handler(call.message, lambda msg: new_message(msg, call.data))
    
    elif(read_menu_flag()=='2'):
      bot.send_message(id_, read_sub_inf(call.data))
    
    elif(read_menu_flag()=='3'):
      bot.send_message(id_, f"Вы уверены, что хотите удалить {call.data}?")
      bot.register_next_step_handler(call.message, lambda msg: delete_sub(msg, call.data))


def delete_sub(message, name):
  if(message.text=="Да"):
    os.remove(f"{path}{name}.txt")  
    bot.send_message(id_, "Заметка успешно удалена!")
  else:
    bot.send_message(id_, "Вот и славно!")
    
def new_file(name):

  with open(f"{path}{name}.txt", "w", encoding="utf-8") as file:
      file.write("null")

def new_notes(message):

  if(message.text=="..."):

    bot.send_message(id_, "Хозяин-барин")
  else:
    new_file(message.text)

    bot.send_message(id_, f"Облаcть {message.text} успешно зарегистрирована!")  

def new_message(message, name):
  if(message.text=="..."):
    bot.send_message(id_, "Хозяин-барин")
  else:
    with open(f"{path}{name}.txt", "w", encoding="utf-8") as file:
      file.writelines(message.text.replace('\n', '/$/'))
      bot.send_message(id_, "Заметка успешно записана!")  

def write_menu_flag(data):
  with open(f"{path}FlagCarrier.txt", "w", encoding="utf-8") as file:
    file.write(data)

def read_menu_flag():
  with open(f"{path}FlagCarrier.txt", "r", encoding="utf-8") as file:
    return file.read()

def read_sub_inf(name):
  try:
    with open(f"{path}{name}.txt", "r", encoding="utf-8") as file:
      lines = file.read()
      return lines.replace("/$/", "\n")
    
  except FileNotFoundError:
    new_file(name)

    print(f"Создан новый файл: {name}.txt")

    return "null"

def inlineKeyboard_init():
  txt_files = [f for f in os.listdir(path) if f.endswith('.txt')]
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


if __name__ == "__main__":
  try:
    threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
    
    print(f'Мониторинг за чатом {id_} работает')

    while True:

        if(TimeOperator.time_gateway()):

          if(up_state_check((int)(time.strftime('%w'))+1)=="true"):

            up_state(id_, (int)(time.strftime('%w'))+1, 1)
            print_schedule(id_, (int)(time.strftime('%w'))+1)
            
            time.sleep(TimeOperator.get_remaining_time(True if TimeOperator.time_gateway() else False))
        else:
          time.sleep(30)

  except Exception as e:
    print(e.with_traceback)
    time.sleep(30)  