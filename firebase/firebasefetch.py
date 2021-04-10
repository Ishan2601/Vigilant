from firebase import firebase

firebase = firebase.FirebaseApplication('https://vigilant-73f45-default-rtdb.firebaseio.com/', None)
result = firebase.get('/vigilant-73f45-default-rtdb/Driver/', '')
print(result)