import datetime

ride_start = datetime.now()
# CODE HERE
ride_now = datetime.now()

def get_daytime():
    current_time = datetime.now()
    h = current_time.hour
    if h < 7 or h > 19:
        print("Night")
    else:
        print("Day")

count_sleep = 0
count_yawn = 0
