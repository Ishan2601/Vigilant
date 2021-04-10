from flask import Flask, render_template, Response, request
from camera import VideoCamera
import json
import requests
import firebase_admin
from firebase_admin import credentials, auth
cred = credentials.Certificate('./fbAdminConfig.json')

# TO DO
#1. Log all data to Firebase
#2. Integrate Location, Twilio
#3. Nearby API
#4. Rpi Code
#5. Homepage


user = {}
app = Flask(__name__)

FIREBASE_WEB_API_KEY = "AIzaSyCEJKHbCFEfVE8XMV8Rd_tTLhHTEr1QpAI"
rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"

config = {
        "apiKey": "AIzaSyCEJKHbCFEfVE8XMV8Rd_tTLhHTEr1QpAI",
        "authDomain": "vigilant-73f45.firebaseapp.com",
        "databaseURL": "https://vigilant-73f45-default-rtdb.firebaseio.com",
        "projectId": "vigilant-73f45",
        "storageBucket": "vigilant-73f45.appspot.com",
        "messagingSenderId": "71056574999",
        "appId": "1:71056574999:web:c35fb0b1d641e3ec632a52"}

firebase_admin.initialize_app(cred, config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # GET USER DETAILS
        print(request.form.get('fname'))
        print(user.uid)
    return render_template('login.html', task=1)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        global user
        email = request.form.get('email')
        pwd = request.form.get('password')
        user = auth.create_user(email = email, password = pwd)
        return render_template('details.html')
    return render_template('login.html', task=0)

@app.route('/logged_in', methods=['POST'])
def logged_in():
        if request.method == "POST":
            email = request.form.get('email')
            pwd = request.form.get('password')
            payload = json.dumps({
                "email": email,
                "password": pwd,
                "returnSecureToken": True
            })
            r = requests.post(rest_api_url,params={"key": FIREBASE_WEB_API_KEY},data=payload)
            #print(r.json())
            return render_template('camera.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=False)
