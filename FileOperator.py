import os

class FileOperator:

    def __init__(self, userId, bot):
        
        self.userId=userId

        self.bot=bot

        self.path = "BotFiles/"

    def delete_sub(self, message, name):
        if(message.text=="Да"):
            os.remove(f"{self.path}{name}.txt")  
            self.bot.send_message(self.userId, "Заметка успешно удалена!")
        else:
            self.bot.send_message(self.userId, "Вот и славно!")
        
    def new_file(self, name):

        with open(f"{self.path}{name}.txt", "w", encoding="utf-8") as file:
            file.write("null")

    def new_notes(self, message):

        if(message.text=="..."):

            self.bot.send_message(self.userId, "Хозяин-барин")
        else:
            self.new_file(message.text)

            self.bot.send_message(self.userId, f"Облаcть {message.text} успешно зарегистрирована!")  

    def new_message(self, message, name):
        if(message.text=="..."):
            self.bot.send_message(self.userId, "Хозяин-барин")
        else:
            with open(f"{self.path}{name}.txt", "w", encoding="utf-8") as file:
                file.writelines(message.text.replace('\n', '/$/'))
                self.bot.send_message(self.userId, "Заметка успешно записана!")  

    def write_menu_flag(self, data):
        with open(f"{self.path}FlagCarrier.txt", "w", encoding="utf-8") as file:
            file.write(data)

    def read_menu_flag(self):
        with open(f"{self.path}FlagCarrier.txt", "r", encoding="utf-8") as file:
            return file.read()

    def read_sub_inf(self, name):
        try:
            with open(f"{self.path}{name}.txt", "r", encoding="utf-8") as file:
                lines = file.read()
                return lines.replace("/$/", "\n")
            
        except FileNotFoundError:
            self.new_file(name)

            print(f"Создан новый файл: {name}.txt")

            return "null"
