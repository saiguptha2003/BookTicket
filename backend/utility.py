from pymongo import MongoClient
import re

client = MongoClient('mongodb://localhost:27017/')
db = client['MovieBooking']
collection = db['Users']



def isEmailCorrect(email):
    pattern = r'^[\w\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))


def isPasswordInPattern(password):
    return len(password) >= 8


def isUserEmailExist(email):
    user = collection.find_one({'email': email.lower()})
    return user is not None


def isUserNameExist(username):
    user = collection.find_one({'username': username.lower()})
    return user is not None

def checkUser(usernameOrEmail, password):
    result={'message': 'Invalid email or password', 'success': False,'isUserNameExist':isUserNameExist(usernameOrEmail), 'isUserEmailExist':isUserEmailExist(usernameOrEmail),'isPasswordInPattern':isPasswordInPattern(password),'isEmailCorrect':isEmailCorrect(usernameOrEmail)}
    if  isPasswordInPattern(password) and (isUserEmailExist(usernameOrEmail) or isUserNameExist(usernameOrEmail)):
        user = collection.find_one({'email': usernameOrEmail.lower()}) if isEmailCorrect(usernameOrEmail) else collection.find_one({'username': usernameOrEmail.lower()})
        if user['password'] == password:
            return {'message': 'User signed in successfully', 'success': True, 'user_id': str(user['_id']), 'username': user['username']}
        else:
            return {'error':1, 'success': False, 'message': "Invalid email or password"}
    return result

def addUser(email, username, password):
    if isEmailCorrect(email) and isPasswordInPattern(password) and not isUserEmailExist(email) and not isUserNameExist(username):
        user_data = {
            'email': email.lower(),
            'username': username.lower(),
            'password': password
        }
        result = collection.insert_one(user_data)
        if result.inserted_id:
            return {'user_id': str(result.inserted_id), 'message': 'User added successfully', 'success': True}
    return {'message': 'Invalid email or password', 'success': False,'isUserNameExist':isUserNameExist(username), 'isUserEmailExist':isUserEmailExist(email),'isPasswordInPattern':isPasswordInPattern(password),'isEmailCorrect':isEmailCorrect(email)}



