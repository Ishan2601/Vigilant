import firebase_admin
from firebase_admin import credentials, firestore
from firebase import Firebase


class GoogleFire:
    def __init__(self):
        # Use the application default credentials
        self.config = {
        "apiKey": "AIzaSyCEJKHbCFEfVE8XMV8Rd_tTLhHTEr1QpAI",
        "authDomain": "vigilant-73f45.firebaseapp.com",
        "databaseURL": "https://vigilant-73f45-default-rtdb.firebaseio.com",
        "projectId": "vigilant-73f45",
        "storageBucket": "vigilant-73f45.appspot.com",
        "messagingSenderId": "71056574999",
        "appId": "1:71056574999:web:c35fb0b1d641e3ec632a52"}
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, self.config)
        self.fireb = Firebase(self.config)
        #self.db = firestore.client()

    def create_user(self,email,password):
        self.fireb.auth.create_user_with_email_and_password(email = email, password = password)

    def auth_user(self,email, password):
        self.fireb.auth.sign_in_with_email_and_password(email, password)

    def update_ride_details(self, data, uid):
        doc = self.db.collection(u'Drivers').document(f'{uid}').collection('Rides').document()
        doc.set(data)
        return "Ride Details Updated"

    def fetch_user(self, uid):
        pass