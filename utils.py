import geocoder
import datetime
from twilio.rest import Client

class Utils:
    def __init__(self):
        self.g = geocoder.ip('me')
        self.count_sleep = 0
        self.count_yawn = 0
        self.account_sid = 'ACeec1a4fa24498b488d9a387eb775e054'
        self.auth_token = '691886f4c9202a2623cb738ad8ba91d2'

    def get_lat_long(self):
        return self.g.latlng
    
    def get_time():
        return datetime.now()

    def get_daytime(self):
        current_time = self.get_time()
        h = current_time.hour
        if h < 7 or h > 19:
            return "Night"
        else:
            return "Day"
    
    def inc_count(self, which):
        if which == "sleep":
            self.count_sleep += 1
        else:
            self.count_yawn += 1

    def get_count(self, which = "both"):
        if which == "sleep":
            return self.count_sleep
        elif which == "yawn":
            return self.count_yawn
        else:
            return self.count_sleep, self.count_yawn
    
    def send_SMS(self, number):
        client = Client(self.account_sid, self.auth_token)
        ltlng = self.get_lat_long()
        sendNo = '+91'+str(number)
        message = client.messages \
            .create(
                body=f'http://maps.google.com/maps?q={ltlng[0]},{ltlng[1]}',
                from_='+13236132697',
                to=sendNo
            ) 
        return message.status