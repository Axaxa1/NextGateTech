import pyrebase
firebaseConfig = {
    'apiKey': "AIzaSyAcUdjvfpx6OObR1-zfcKWupvjAl3ua0jY",
    'databaseURL': "x-catwalk-310216.firebaseapp.com",
    'authDomain': "x-catwalk-310216.firebaseapp.com",
    'projectId': "x-catwalk-310216",
    'storageBucket': "x-catwalk-310216.appspot.com",
    'messagingSenderId': "692521060158",
    'appId': "1:692521060158:web:dd62273d90f81dada1ce6f"}



def createapp(config):
    return pyrebase.initialize_app(config)


def signup(app):
    pyrebase.initialize_app(firebaseConfig)
    auth = app.auth()
    mail = input("Mail : ")
    password = input("Password : ")
    auth.create_user_with_email_and_password(mail, password)


def login(app):
    auth = app.auth()
    mail = input("Mail : ")
    password = input("Password : ")
    try:
        auth.sign_in_with_email_and_password(mail, password)
        print("Login !")
    except:
        print("Failed !")


app = createapp(firebaseConfig)
signup(app)
login(app)