import time, datetime


class TimeOperator:

    secondMessageTime=[22, 38]

    @staticmethod
    def sleep_until_evening():

        current_time = time.time()

        target_time = time.mktime(time.strptime(time.strftime(f"%Y-%m-%d {TimeOperator.secondMessageTime[0]}:{TimeOperator.secondMessageTime[1]}:00"), "%Y-%m-%d %H:%M:%S"))
        
        sleep_time = int(target_time - current_time) - 120

        if (sleep_time>0):
            time.sleep(sleep_time)
            return True 
        else:
            time.sleep(TimeOperator.sleep_until_next_day())
            return False
        
    @staticmethod
    def sleep_until_next_day():

        current_time = time.time()

        target_time = time.mktime(time.strptime(time.strftime("%Y-%m-%d 23:59:00"), "%Y-%m-%d %H:%M:%S"))

        time.sleep(int(target_time - current_time) + 36000)

    @staticmethod
    def time_gateway():

        current_time = datetime.datetime.now().time()

        set_time = datetime.time(TimeOperator.secondMessageTime[0], TimeOperator.secondMessageTime[1])

        if (current_time >= set_time):
            return True
        else:
            return False
    
if __name__ == "__main__":
    print(TimeOperator.time_gateway())