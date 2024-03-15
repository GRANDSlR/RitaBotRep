from TimeOperator import *
from datetime import date, timedelta
from bs4 import BeautifulSoup as BS
import requests

class SheduleOperator:

    def __init__(self, userId, bot, day):
        self.url_KBP='https://kbp.by/rasp/timetable/view_beta_kbp/?page=stable&cat=group&id=53'

        self.headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }

        self.userId=userId

        self.bot=bot


    def schedule_checker(self):
        
        responce = requests.get(self.url_KBP, headers=self.headers)
        soup=BS(responce.text, "lxml")

        if(self.up_state_check(soup, (int)(time.strftime('%w'))+1)=="true"):
            self.up_state(1)
            self.print_schedule()

            if (TimeOperator.sleep_until_evening() == False):
                return

            while True:
                if (TimeOperator.time_gateway()):
                    self.up_state(1)
                    self.print_schedule()
                    TimeOperator.sleep_until_next_day()
                    break

            time.sleep(30) 

    def up_state(self, sheduleDayFlag):

        responce = requests.get(self.url_KBP, headers=self.headers)
        soup=BS(responce.text, "lxml")

        tomorrow = (date.today() + timedelta(days=sheduleDayFlag)).strftime("%d-%m")
        zameny = soup.find("tr", class_="zamena").find_all("th")

        self.bot.send_message(self.userId, f"Раписание на {tomorrow}")

        if ("Замен нет" in zameny[self.day].get_text()):
            self.bot.send_message(self.userId, "Замен нет")
        elif (zameny[self.day].find("label")!=None):
            self.bot.send_message(self.userId, "Замены есть")  
        else:
            self.bot.send_message(self.userId,"Расписание не обновлено")

    def up_state_check(self):

        responce = requests.get(self.url_KBP, headers=self.headers)
        soup=BS(responce.text, "lxml")
    
        zameny = soup.find("tr", class_="zamena").find_all("th")
        if ("Замен нет" in zameny[self.day].get_text()):
            return "true"
        elif (zameny[self.day].find("label")!=None):
            return "true"
        else:
            return "false"

    def print_schedule(self, sheduleDayFlag):

        responce = requests.get(self.url_KBP, headers=self.headers)
        soup=BS(responce.text, "lxml")

        if(len(self.get_schedule(soup, self.day))!=0):
            self.bot.send_message(self.userId, "\n".join(self.get_schedule(soup, self.day)))
        if(len(self.find_notes(soup, self.day))!=0):
            self.bot.send_message(self.userId, "Заметки:\n"+"".join(self.find_notes(soup, self.day)))

    def get_schedule(self, soup):

        schedule_list = []
        lesson = soup.find_all("tr")
        for i in range(2, 17):
            subject = lesson[i].find_all("td")
            if (subject[self.day].find("div", class_="empty-pair")==None or subject[self.day].find("div", class_=f"pair lw_{self.day} added")!=None):
                num = subject[0].text
                if(subject[self.day].find("div", class_=f"pair lw_{self.day} added")==None):
                    sub = subject[self.day].find("div", class_="subject").find("a").text
                    cab = subject[self.day].find("div", class_="place").find("a").text
                    schedule_list.append(f'{num}-{sub} [{cab}]')
                else:
                    sub = subject[self.day].find("div", class_=f"pair lw_{self.day} added").find("div", class_="subject").find("a").text
                    cab = subject[self.day].find("div", class_=f"pair lw_{self.day} added").find("div", class_="place").find("a").text
                    schedule_list.append(f'{num}-{sub} [{cab}] *') 
        return schedule_list

    def find_notes(self, soup):
        write_sub_list = []
        lesson = soup.find_all("tr")
        for i in range(2, 17):
            subject = lesson[i].find_all("td")
            if (subject[self.userId].find("div", class_="empty-pair")==None or subject[self.userId].find("div", class_=f"pair lw_{self.userId} added")!=None):
                sub = self.get_sub_at_day(subject)
                if(self.read_sub_inf(sub)!="null"):
                    write_sub_list.append(sub +":\n"+ self.read_sub_inf(sub)+"\n")  
        write_sub_list = list(set(write_sub_list))
        return write_sub_list

    def get_sub_at_day(self, subject):
        if(subject[self.day].find("div", class_=f"pair lw_{self.day} added")==None):
            return subject[self.day].find("div", class_="subject").find("a").text
        else:
            return subject[self.day].find("div", class_=f"pair lw_{self.day} added").find("div", class_="subject").find("a").text












# from TimeOperator import *
# from datetime import date, timedelta
# from bs4 import BeautifulSoup as BS
# import requests

# # from RitaBotOperator import *

# class SheduleOperator:

#     url_KBP='https://kbp.by/rasp/timetable/view_beta_kbp/?page=stable&cat=group&id=53'

#     headers = {
#     "User-Agent":
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
#     }

#     responce = requests.get(url_KBP, headers=headers)
#     soup=BS(responce.text, "lxml")


#     def schedule_checker():

#         if(SheduleOperator.up_state_check((int)(time.strftime('%w'))+1)=="true"):

#             SheduleOperator.up_state(id_, (int)(time.strftime('%w'))+1, 1)
#             SheduleOperator.print_schedule(id_, (int)(time.strftime('%w'))+1)

#             if (TimeOperator.sleep_until_evening() == False):
#                 return

#             while True:

#                 if (TimeOperator.time_gateway()):

#                     SheduleOperator.up_state(id_, (int)(time.strftime('%w'))+1, 1)
#                     SheduleOperator.print_schedule(id_, (int)(time.strftime('%w'))+1)

#                     TimeOperator.sleep_until_next_day()

#                     break

#             time.sleep(30) 


#     def up_state(id_, day, f):
#         tomorrow = (date.today() + timedelta(days=f)).strftime("%d-%m")

#         zameny=soup.find("tr", class_="zamena").find_all("th")
        
#         bot.send_message(id_, f"Раписание на {tomorrow}")
#         if ("Замен нет" in zameny[day].get_text()):
#             bot.send_message(id_, "Замен нет")
#         elif (zameny[day].find("label")!=None):
#             bot.send_message(id_, "Замены есть")  
#         else:
#             bot.send_message(id_,"Расписание не обновлено")


#     def up_state_check(day):

#         responce = requests.get(url_KBP, headers=headers)
#         soup=BS(responce.text, "lxml")

#         zameny=soup.find("tr", class_="zamena").find_all("th")

#         if ("Замен нет" in zameny[day].get_text()):
#             return "true"
#         elif (zameny[day].find("label")!=None):
#             return "true"
#         else:
#             return "false"


#     def print_schedule(id_, day):

#         if(len(SheduleOperator.get_schedule(day))!=0):
            
#             bot.send_message(id_, "\n".join(SheduleOperator.get_schedule(day)))

#         if(len(SheduleOperator.find_notes(day))!=0):

#             bot.send_message(id_, "Заметки:\n"+"".join(SheduleOperator.find_notes(day)))


#     def get_schedule(day):

#         schedule_list = []
#         lesson=soup.find_all("tr")

#         for i in range(2, 17):

#             subject=lesson[i].find_all("td")

#             if (subject[day].find("div", class_="empty-pair")==None or subject[day].find("div", class_=f"pair lw_{day} added")!=None):
#                 num=subject[0].text
#                 if(subject[day].find("div", class_=f"pair lw_{day} added")==None):
#                     sub=subject[day].find("div", class_="subject").find("a").text
#                     cab=subject[day].find("div", class_="place").find("a").text
#                     schedule_list.append(f'{num}-{sub} [{cab}]')

#                 else:
#                     sub=subject[day].find("div", class_=f"pair lw_{day} added").find("div", class_="subject").find("a").text
#                     cab=subject[day].find("div", class_=f"pair lw_{day} added").find("div", class_="place").find("a").text
#                     schedule_list.append(f'{num}-{sub} [{cab}] *') 
                    
#         return schedule_list


#     def find_notes(day):

#         write_sub_list = []
#         lesson=soup.find_all("tr")

#         for i in range(2, 17):

#             subject=lesson[i].find_all("td")

#             if (subject[day].find("div", class_="empty-pair")==None or subject[day].find("div", class_=f"pair lw_{day} added")!=None):

#                 sub=SheduleOperator.get_sub_at_day(subject, day)

#                 if(SheduleOperator.read_sub_inf(sub)!="null"):
#                     write_sub_list.append(sub +":\n"+ SheduleOperator.read_sub_inf(sub)+"\n")  

#         write_sub_list = list(set(write_sub_list))
        
#         return write_sub_list


#     def get_sub_at_day(subject, day):

#         if(subject[day].find("div", class_=f"pair lw_{day} added")==None):

#             return subject[day].find("div", class_="subject").find("a").text
        
#         else:
#             return subject[day].find("div", class_=f"pair lw_{day} added").find("div", class_="subject").find("a").text
