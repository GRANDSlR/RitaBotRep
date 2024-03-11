import time

class TimeOperator:
    @staticmethod
    def get_remaining_time(flag):

        current_time = time.time()

        if(flag):
            target_time = time.mktime(time.strptime(time.strftime("%Y-%m-%d 19:30:00"), "%Y-%m-%d %H:%M:%S"))
            time_diff = target_time - current_time
            return int(time_diff)
        else:
            target_time = time.mktime(time.strptime(time.strftime("%Y-%m-%d 23:59:00"), "%Y-%m-%d %H:%M:%S"))
            time_diff = target_time - current_time
            return int(time_diff)+36000
        
    @staticmethod
    def time_gateway():

        current_time = time.localtime()
        hours = current_time.tm_hour

        if(hours>=10 and hours<=20):
            return True
        else:
            return False

    @staticmethod
    def curr_hour():

        current_time = time.localtime()
        return current_time.tm_hour
