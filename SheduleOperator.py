from TimeOperator import *
from FileOperator import *
from datetime import date, timedelta
from bs4 import BeautifulSoup as BS
import requests

class SheduleOperator:

    def __init__(self, userId, bot, day, FileOperatorObject):

        self.url_KBP='https://kbp.by/rasp/timetable/view_beta_kbp/?page=stable&cat=group&id=53'

        self.headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }

        self.userId=userId

        self.bot=bot

        self.day=day

        self.sheduleDayFlag = 0

        self.FileOperatorObject=FileOperatorObject


    def schedule_checker(self):

        if(self.up_state_check()=="true"):

            self.schedule_handler(1)

            if (TimeOperator.sleep_until_evening() == False):
                return

            while True:
                if (TimeOperator.time_gateway()):

                    self.schedule_handler(1)

                    TimeOperator.sleep_until_next_day()
                    break

            time.sleep(30) 

    def schedule_handler(self, sheduleDayFlag):

        self.sheduleDayFlag=sheduleDayFlag

        self.up_state()
        self.print_schedule()

    def up_state(self):

        responce = requests.get(self.url_KBP, headers=self.headers)
        soup=BS(responce.text, "lxml")

        tomorrow = (date.today() + timedelta(days=self.sheduleDayFlag)).strftime("%d-%m")
        zameny = soup.find("tr", class_="zamena").find_all("th")

        self.bot.send_message(self.userId, f"Раписание на {tomorrow}")

        if ("Замен нет" in zameny[self.day + self.sheduleDayFlag].get_text()):
            self.bot.send_message(self.userId, "Замен нет")
        elif (zameny[self.day + self.sheduleDayFlag].find("label")!=None):
            self.bot.send_message(self.userId, "Замены есть")  
        else:
            self.bot.send_message(self.userId,"Расписание не обновлено")

    def up_state_check(self):

        responce = requests.get(self.url_KBP, headers=self.headers)
        soup=BS(responce.text, "lxml")
    
        zameny = soup.find("tr", class_="zamena").find_all("th")
        if ("Замен нет" in zameny[self.day+1].get_text()):
            return "true"
        elif (zameny[self.day+1].find("label")!=None):
            return "true"
        else:
            return "false"

    def print_schedule(self):

        responce = requests.get(self.url_KBP, headers=self.headers)
        soup=BS(responce.text, "lxml")

        if(len(self.get_schedule(soup))!=0):
            self.bot.send_message(self.userId, "\n".join(self.get_schedule(soup)))
        if(len(self.find_notes(soup))!=0):
            self.bot.send_message(self.userId, "Заметки:\n"+"".join(self.find_notes(soup)))

    def get_schedule(self, soup):

        schedule_list = []
        lesson = soup.find_all("tr")
        for i in range(2, 17):
            subject = lesson[i].find_all("td")
            if (subject[self.day + self.sheduleDayFlag].find("div", class_="empty-pair")==None or subject[self.day + self.sheduleDayFlag].find("div", class_=f"pair lw_{self.day} added")!=None):
                num = subject[0].text
                if(subject[self.day + self.sheduleDayFlag].find("div", class_=f"pair lw_{self.day + self.sheduleDayFlag} added")==None):
                    sub = subject[self.day + self.sheduleDayFlag].find("div", class_="subject").find("a").text
                    cab = subject[self.day + self.sheduleDayFlag].find("div", class_="place").find("a").text
                    schedule_list.append(f'{num}-{sub} [{cab}]')
                    print(f"nothing updates at {sub}")
                else:
                    sub = subject[self.day + self.sheduleDayFlag].find("div", class_=f"pair lw_{self.day + self.sheduleDayFlag} added").find("div", class_="subject").find("a").text
                    cab = subject[self.day + self.sheduleDayFlag].find("div", class_=f"pair lw_{self.day + self.sheduleDayFlag} added").find("div", class_="place").find("a").text
                    schedule_list.append(f'{num}-{sub} [{cab}] *') 
                    print(f"update at {sub}")

        return schedule_list

    def find_notes(self, soup):
        write_sub_list = []
        lesson = soup.find_all("tr")
        for i in range(2, 17):
            subject = lesson[i].find_all("td")
            if (subject[self.day + self.sheduleDayFlag].find("div", class_="empty-pair")==None or subject[self.day + self.sheduleDayFlag].find("div", class_=f"pair lw_{self.day + self.sheduleDayFlag} added")!=None):
                sub = self.get_sub_at_day(subject)
                if(self.FileOperatorObject.read_sub_inf(sub)!="null"):
                    write_sub_list.append(sub +":\n"+ self.FileOperatorObject.read_sub_inf(sub)+"\n")  
        write_sub_list = list(set(write_sub_list))
        return write_sub_list

    def get_sub_at_day(self, subject):
        if(subject[self.day + self.sheduleDayFlag].find("div", class_=f"pair lw_{self.day + self.sheduleDayFlag} added")==None):
            return subject[self.day + self.sheduleDayFlag].find("div", class_="subject").find("a").text
        else:
            return subject[self.day + self.sheduleDayFlag].find("div", class_=f"pair lw_{self.day + self.sheduleDayFlag} added").find("div", class_="subject").find("a").text
