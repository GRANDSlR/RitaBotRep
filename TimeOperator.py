import time, datetime


class TimeOperator:

    secondMessageTime=[19, 30]

    @staticmethod
    def get_remaining_time(flag):

        current_time = time.time()

        if(flag):
            target_time = time.mktime(time.strptime(time.strftime(f"%Y-%m-%d {TimeOperator.secondMessageTime[0]}:{TimeOperator.secondMessageTime[1]}:00"), "%Y-%m-%d %H:%M:%S"))
            return int(target_time - current_time)
        else:
            target_time = time.mktime(time.strptime(time.strftime("%Y-%m-%d 23:59:00"), "%Y-%m-%d %H:%M:%S"))
            return int(target_time - current_time)+36000
        
    @staticmethod
    def time_gateway():

        current_time = datetime.datetime.now().time()

        set_time = datetime.time(TimeOperator.secondMessageTime[0], TimeOperator.secondMessageTime[1])

        if (current_time > datetime.time(10, 0) and current_time < set_time):
            return True
        else:
            return False
    
if __name__ == "__main__":
    print(TimeOperator.time_gateway())