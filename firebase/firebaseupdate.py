from firebase import firebase

firebase = firebase.FirebaseApplication('https://vigilant-73f45-default-rtdb.firebaseio.com/', None)
firebase.put('/vigilant-73f45-default-rtdb/Driver/-MXvinFMl_9RrzJgY70w', 'Sleepy', 'No')
print('Record Updated')