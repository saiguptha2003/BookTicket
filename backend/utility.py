from pymongo import MongoClient
import re
from bson import ObjectId
client = MongoClient('mongodb://localhost:27017/')
db = client['MovieTicketBooking']
users = db['Users']
movies = db['Movies']
Theaters=db['Theaters']
from bson import json_util



def isEmailCorrect(email):
    pattern = r'^[\w\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))


def isPasswordInPattern(password):
    return len(password) >= 8


def isUserEmailExist(email):
    user = users.find_one({'email': email.lower()})
    return user is not None


def isUserNameExist(username):
    user = users.find_one({'username': username.lower()})
    return user is not None

def checkUser(usernameOrEmail, password):
    result={'message': 'Invalid email or password', 'success': False,'isUserNameExist':isUserNameExist(usernameOrEmail), 'isUserEmailExist':isUserEmailExist(usernameOrEmail),'isPasswordInPattern':isPasswordInPattern(password),'isEmailCorrect':isEmailCorrect(usernameOrEmail)}
    if  isPasswordInPattern(password) and (isUserEmailExist(usernameOrEmail) or isUserNameExist(usernameOrEmail)):
        user = users.find_one({'email': usernameOrEmail.lower()}) if isEmailCorrect(usernameOrEmail) else users.find_one({'username': usernameOrEmail.lower()})
        if user['password'] == password:
            return {'message': 'User signed in successfully', 'success': True, 'user_id': str(user['_id']), 'username': user['username']}
        else:
            return {'error':1, 'success': False, 'message': "Invalid email or password"}
    return result

def addUser(email, username, password,phoneNumber,country):
    if isEmailCorrect(email) and isPasswordInPattern(password) and not isUserEmailExist(email) and not isUserNameExist(username):
        user_data = {
            'email': email.lower(),
            'username': username.lower(),
            'password': password,
            'phoneNumber': phoneNumber,
            'country': country
        }
        result = users.insert_one(user_data)
        if result.inserted_id:
            return {'user_id': str(result.inserted_id), 'message': 'User added successfully', 'success': True}
    return {'message': 'Invalid email or password', 'success': False,'isUserNameExist':isUserNameExist(username), 'isUserEmailExist':isUserEmailExist(email),'isPasswordInPattern':isPasswordInPattern(password),'isEmailCorrect':isEmailCorrect(email)}


from bson import ObjectId
from bson import json_util

def sendBookTicket(uuid, theaterId, movieId, seats, time, date, totalPrice):
    print(uuid,';afadsfasdf')
    collection = db['Bookings']
    booking_data = {
        'uuid': str(uuid),  # Convert ObjectId to string
        'theaterId': theaterId,
        'movieId': movieId,
        'seats': seats,
        'time': time,
        'date': date,
        'totalPrice': totalPrice
    }
    result = collection.insert_one(booking_data)
    if result.inserted_id:
        print(str(result.inserted_id),'bookindID')
        booking_data['booking_id'] = str(result.inserted_id)
        print(type(booking_data['booking_id']))
        users.update_one(
            {'_id': ObjectId(uuid)},
            {'$push': {'booked_tickets': booking_data}}
        )
        return json_util.dumps({'message': 'Ticket booked successfully', 'success': True, 'ticketDetails': booking_data})
    return json_util.dumps({'message': 'Ticket booked unsuccessfully', 'success': False})


def getBookingDetails(bookingid):
    collection = db['Bookings']
    result = collection.find_one({'_id': ObjectId(bookingid)})
    print(result,'fghfhgfgh')
    return json_util.dumps(result)

def addMovie(movie):
    collection = db['Movies']
    result = collection.insert_one(movie)
    if result.inserted_id:
        return json_util.dumps({'message': 'Movie added successfully', 'success': True})
    return json_util.dumps({'message': 'Movie added unsuccessfully', 'success': False})

def getAllBookedTickets(userId):
    user = users.find_one({'_id': ObjectId(userId)})
    if user and 'booked_tickets' in user:
        return user['booked_tickets']
    else:
        return None
    
def getAllMoviesDetails():
    collection = db['Movies']
    all_movies = collection.find()
    movies_details = []
    for movie in all_movies:
        movie_details = {
            'id': str(movie['_id']),  # Convert ObjectId to string
            'title': movie['title'],
            'description': movie['description'],
            'director': movie['director'],
            'favorite_percentage': movie['favorite_percentage'],
            'releaseDate': movie['releaseDate'],
            'duration': movie['duration'],
            'theaters': movie['theaters']  # Assuming theaters field contains theater details
        }
        movies_details.append(movie_details)
    return json_util.dumps(movies_details)