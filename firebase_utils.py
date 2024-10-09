import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("./keyfile.json")
firebase_app = firebase_admin.initialize_app(cred, {
    'storageBucket': "explore-my-city-12ea0.appspot.com"
})
