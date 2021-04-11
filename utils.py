import geocoder
import datetime
from twilio.rest import Client

class Util:
    def __init__(self):
        self.g = geocoder.ip('me')
        self.account_sid = 'ACeec1a4fa24498b488d9a387eb775e054'
        self.auth_token = '691886f4c9202a2623cb738ad8ba91d2'

    def get_lat_long(self):
        return self.g.latlng
    
    @staticmethod
    def get_time():
        return datetime.datetime.now()

    def get_daytime(self):
        current_time = self.get_time()
        h = current_time.hour
        if h < 7 or h > 19:
            return False
        else:
            return True
    
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

    def send_verify_link(self,to):
        if not to.startswith('+91'):
            to = '+91' + to
        verification = ( self.client.verify 
                        .services(self.service_sid) 
                        .verifications 
                        .create(to=to, channel='sms')
        )

    def check_verification_status(self,to,otp):
        if not to.startswith('+91'):
            to = '+91' + to
        verification_check = ( self.client.verify 
                           .services(self.service_sid) 
                           .verification_checks 
                           .create(to=to, code=otp)
        )
        #print(verification_check.status)
        return "approved" in verification_check.status