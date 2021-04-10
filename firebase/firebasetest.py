from firebase import firebase

firebase = firebase.FirebaseApplication('https://vigilant-73f45-default-rtdb.firebaseio.com/', None)
data =  { 'Name': 'Yash Jungade',
        'Sleepy': 'Yes',
        'Yawning': 'Yes',
          }
result = firebase.post('/vigilant-73f45-default-rtdb/Driver/',data)
print(result)