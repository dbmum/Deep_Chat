import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os



class DataBase:
    
    def __init__(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]  = 'serviceAccountkey.json'
        firebase_admin.initialize_app(credentials.ApplicationDefault(),{
            'projectId': "deep--storage",
        })

        self.db = firestore.client()
        # self.selfauth = firebase.auth()
        # self.storage = firebase.storage()
        self.current_user = None
        self.is_authenticated = False

    def ViewFeed(self):
        feed = self.db.collection('posts').get()
        dictionary  = {}
        my_list = []
        for result in feed:
            data = result.to_dict()
            my_list.append(data)
            

        dictionary['results'] = my_list
        return dictionary


    def MakeUser(self, user, passw):
        username = user
        password = passw
        result = self.db.collection('users').document(username).get()
        if result.exists:
            return False
        else:
            data = {'user':username,
                    "password": password}
            self.db.collection('users').document(username).set(data)
            return True

    def MakePost(self, post):
        
        data = {'user': self.current_user,
                'post': post,
                'time': firestore.SERVER_TIMESTAMP}
        self.db.collection('posts').add(data)
            

    def UpdatePassword(self):
        new_password = input('What would you like to change your password to?\n')
        result = self.db.collection('users').document(self.current_user).get()

        data = result.to_dict()
        data['password'] = new_password

        self.db.collection('users').document(self.current_user).set(data)

    def DeleteUser(self):
        user = input('to delete your account FOREVER, type your username:\n')
        user_check = self.db.collection('users').document(user).get()

        if user_check.exists and user == self.current_user:
            user_check.reference.delete()

            print(f'User ~~{user}~~ has been deleted')

            self.is_authenticated = False
        
            
                
    def Authenticate(self, user, passw):
        self.is_authenticated = False
        user = user
        password = passw
        user_check = self.db.collection('users').document(user).get()
        if user_check.exists:
            data = user_check.to_dict()
            if password == data['password']:
                self.current_user = user
                self.is_authenticated = True
            
