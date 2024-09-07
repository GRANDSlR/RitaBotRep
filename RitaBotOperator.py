import telebot, time, threading
from SheduleOperator import *
from FileOperator import *
from KeyboardOperator import *
import traceback
from Secret import token 
from Secret import id_ 

bot = telebot.TeleBot(token)

noteDirPath="BotFiles/"

KeyboardOperatorObject = KeyboardOperator(noteDirPath)

FileOperatorObject = FileOperator(id_, bot, noteDirPath)

SheduleOperatorObject = SheduleOperator(id_, bot, FileOperatorObject)


@bot.message_handler(content_types=['text'])
def get_text(message):
  if(message.text=="Заметки"):

    bot.send_message(id_, 'Выберите действие с заметками:', reply_markup=KeyboardOperatorObject.inline_markup_menu)

  if(message.text=="Старт"):

    bot.send_message(id_, 'Привет!', reply_markup=KeyboardOperatorObject.markup)

  if(message.text=="Расписание на сегодня"):

    SheduleOperatorObject.schedule_handler(0)

  if(message.text=="Расписание на завтра"):
    
    SheduleOperatorObject.schedule_handler(1)


@bot.callback_query_handler(func=lambda call: True)# ответ на меню заметок
def check_callback_data(call):
  if (call.data=="Написать заметку"):
    FileOperatorObject.write_menu_flag('1')
    bot.send_message(id_, "Выберите облаcть:", reply_markup=KeyboardOperatorObject.inlineKeyboard_init())
  
  elif (call.data=="Прочитать заметку"):
    FileOperatorObject.write_menu_flag('2')
    bot.send_message(id_, "Выберите облаcть:", reply_markup=KeyboardOperatorObject.inlineKeyboard_init())

  elif(call.data=="Добавить заметку"):
    bot.send_message(id_, "Назовите новую облаcть заметок:")
    bot.register_next_step_handler(call.message, FileOperatorObject.new_notes())
  
  elif(call.data=="Удалить заметку"):
    FileOperatorObject.write_menu_flag('3')
    bot.send_message(id_, "Выберите облаcть:", reply_markup=KeyboardOperatorObject.inlineKeyboard_init())

  else:
    if(FileOperatorObject.read_menu_flag()=='1'):
      bot.send_message(id_, "Содержимое заметки:\n")
      bot.send_message(id_, FileOperatorObject.read_sub_inf(call.data))
      bot.send_message(id_, f"Напишите заметку на {call.data}:")
      bot.register_next_step_handler(call.message, lambda msg: FileOperatorObject.new_message(msg, call.data))
    
    elif(FileOperatorObject.read_menu_flag()=='2'):
      bot.send_message(id_, FileOperatorObject.read_sub_inf(call.data))
    
    elif(FileOperatorObject.read_menu_flag()=='3'):
      bot.send_message(id_, f"Вы уверены, что хотите удалить {call.data}?")
      bot.register_next_step_handler(call.message, lambda msg: FileOperatorObject.delete_sub(msg, call.data))



if __name__ == "__main__":

  threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()

  try:

    print(f'Мониторинг за чатом {id_} работает')

    while True:

      SheduleOperatorObject.schedule_checker()

      time.sleep(30)

  except Exception as e:
    bot.send_message(id_, traceback.print_exc())
    print(traceback.print_exc())