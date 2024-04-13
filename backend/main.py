import uuid
from flask import Flask, json, request, jsonify, session
from utility import * 
app = Flask(__name__)
app.secret_key = '925555fc-f493-11ee-96ea-900f0c7891b4'
from flask_cors import CORS
CORS(app)
cities = {
    'City X': [101],
    'City Y': [102],
    'City Z': [103, 104],
    'City P': [105]
}
theaters_data = {
    101: {'name': 'Theater X', 'location': 'City X'},
    102: {'name': 'Theater Y', 'location': 'City Y'},
    103: {'name': 'Theater Z', 'location': 'City Z'},
    104: {'name': 'Theater W', 'location': 'City Z'},
    105: {'name': 'Theater P', 'location': 'City P'}
}

movies_data = [
    {
        'id': 1,
        'title': 'Movie A',
        'description': 'A thrilling action movie.',
        'favorite_percentage': 85,
        'duration': 120,
        'director': 'Director A',
        'language': 'English',
        'theaters': [
            {
                'id': 101,
                'name': 'Theater X',
                'seating_arrangement': [
                    ['A1', 'A2', 'A3', 'A4', 'A5'],
                    ['B1', 'B2', 'B3', 'B4', 'B5'],
                    ['C1', 'C2', 'C3', 'C4', 'C5'],
                    ['D1', 'D2', 'D3', 'D4', 'D5'],
                    ['E1', 'E2', 'E3', 'E4', 'E5']
                ],
                'booked_seats': ['A2', 'B3', 'C4']
            }
        ]
    },
    {
        'id': 2,
        'title': 'Movie B',
        'description': 'A heartwarming romantic comedy.',
        'favorite_percentage': 92,
        'duration': 110,
        'director': 'Director B',
        'language': 'English',
        'theaters': [
            {
                'id': 102,
                'name': 'Theater Y',
                'seating_arrangement': [
                    ['A1', 'A2', 'A3', 'A4', 'A5'],
                    ['B1', 'B2', 'B3', 'B4', 'B5'],
                    ['C1', 'C2', 'C3', 'C4', 'C5'],
                    ['D1', 'D2', 'D3', 'D4', 'D5'],
                    ['E1', 'E2', 'E3', 'E4', 'E5']
                ],
                'booked_seats': ['B2', 'C3', 'D4']
            }
        ]
    },
    {
        'id': 3,
        'title': 'Movie C',
        'description': 'An intense psychological thriller.',
        'favorite_percentage': 78,
        'duration': 130,
        'director': 'Director C',
        'language': 'English',
        'theaters': [
            {
                'id': 103,
                'name': 'Theater Z',
                'seating_arrangement': [
                    ['A1', 'A2', 'A3', 'A4', 'A5'],
                    ['B1', 'B2', 'B3', 'B4', 'B5'],
                    ['C1', 'C2', 'C3', 'C4', 'C5'],
                    ['D1', 'D2', 'D3', 'D4', 'D5'],
                    ['E1', 'E2', 'E3', 'E4', 'E5']
                ],
                'booked_seats': ['A2', 'B3', 'C4']
            }
        ]
    },
    {
        'id': 4,
        'title': 'Movie D',
        'description': 'A gripping mystery drama.',
        'favorite_percentage': 88,
        'duration': 140,
        'director': 'Director D',
        'language': 'English',
        'theaters': [
            {
                'id': 104,
                'name': 'Theater W',
                'seating_arrangement': [
                    ['A1', 'A2', 'A3', 'A4', 'A5'],
                    ['B1', 'B2', 'B3', 'B4', 'B5'],
                    ['C1', 'C2', 'C3', 'C4', 'C5'],
                    ['D1', 'D2', 'D3', 'D4', 'D5'],
                    ['E1', 'E2', 'E3', 'E4', 'E5']
                ],
                'booked_seats': ['B2', 'C3', 'D4']
            }
        ]
    },
    {
        'id': 5,
        'title': 'Movie E',
        'description': 'A heart-pounding action thriller.',
        'favorite_percentage': 90,
        'duration': 120,
        'director': 'Director E',
        'language': 'English',
        'theaters': [
            {
                'id': 105,
                'name': 'Theater P',
                'seating_arrangement': [
                    ['A1', 'A2', 'A3', 'A4', 'A5'],
                    ['B1', 'B2', 'B3', 'B4', 'B5'],
                    ['C1', 'C2', 'C3', 'C4', 'C5'],
                    ['D1', 'D2', 'D3', 'D4', 'D5'],
                    ['E1', 'E2', 'E3', 'E4', 'E5']
                ],
                'booked_seats': []
            }
        ]
    },
    # Add more movies here...
]


@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data['username'].strip().lower()
    password = data['password'].strip()
    email = data['email'].strip().lower()
    phoneNumber=data['phoneNumber'].strip()
    country = data['country'].strip().lower()
    result=addUser(email, username, password,phoneNumber,country)
    
    return result

@app.route('/signin', methods=['POST'])
def signin():
    data = request.json
    usernameOrEmail = data['usernameOrEmail'].strip().lower()
    password = data['password'].strip()
    result=checkUser(usernameOrEmail, password)
    if(result['success']):
        username = result['username']
        session['user_id'] = result['user_id']
        session['username'] = usernameOrEmail
        session['sessionId'] = str(uuid.uuid1())
        session['authenticated'] = True
    return result

@app.route('/movies', methods=['GET'])
def get_movies():
    # result=getAllMoviesDetails()
    return movies_data

@app.route('/book', methods=['POST'])
def book_seat():
    data = request.json
    seat_id = data.get('seat_id')
    if seat_id:
        return jsonify({'message': 'Seat booked successfully'})
    else:
        return jsonify({'error': 'Seat ID not provided'}), 400
    
    
@app.route('/movies/<city>', methods=['POST', 'GET'])
def get_movies_by_city(city):
    city = city.strip()
    if city in cities:
        theater_ids = cities[city]
        city_movies = [movie for movie in movies_data for theater in movie['theaters'] if theater['id'] in theater_ids]
        return jsonify(city_movies)
    else:
        return jsonify({'error': 'City not found'}), 404
    
@app.route('/theater/<int:id>')
def getTheater(id):
    return theaters_data.get(id)


@app.route('/theaters/<int:movie_id>', methods=['GET'])
def get_theaters(movie_id):
    movie = next((movie for movie in movies_data if movie['id'] == movie_id), None)
    if movie:
        theaters = movie['theaters']
        for theater in theaters:
            print(theater)
            theater_id = theater['id']
            theater_data = theaters_data.get(theater_id)
            if theater_data:
                theater.update(theater_data)  # Merge theater data into the theaters object
        return jsonify(theaters)
    else:
        return jsonify({'error': 'Movie not found'}), 404
    
    
@app.route('/seats/<city>/<int:theater_id>/<int:movie_id>', methods=['GET'])
def get_seats(city, theater_id, movie_id):
    try:
        movie = next((movie for movie in movies_data if movie['id'] == movie_id), None)
        if movie:
            theater = next((theater for theater in movie['theaters'] if theater['id'] == theater_id), None)
            if theater and theater.get('location') == city:
                seating_arrangement = theater.get('seating_arrangement')
                booked_seats = theater.get('booked_seats')
                if seating_arrangement:
                    all_seats = [seat for row in seating_arrangement for seat in row]
                    available_seats = [seat for seat in all_seats if seat not in booked_seats]
                    return jsonify({
                        'seating_arrangement': seating_arrangement,
                        'booked_seats': booked_seats,
                        'available_seats': available_seats
                    })
                else:
                    return jsonify({'error': 'Seating arrangement data is missing for this theater'}), 400
            else:
                return jsonify({'error': 'Theater not found in the specified city'}), 404
        else:
            return jsonify({'error': 'Movie not found'}), 404
    except StopIteration:
        return jsonify({'error': 'Movie or theater not found'}), 404

@app.route('/<uuid>/bookTicket', methods=['POST', 'GET'])
def bookTicket(uuid):
    data = request.json
    uuid=data.get('uuid')
    seats = data.get('selectedSeats')
    movieId = data.get('movieId')
    theaterId = data.get('theaterId')
    time = data.get('Time')
    date = data.get('date')
    totalPrice = data.get('totalAmount')
    if seats and movieId and theaterId and time and date:
        result = sendBookTicket(uuid, theaterId, movieId, seats, time, date, totalPrice)
        if result:
            return {'message': 'Ticket booked successfully', 'success': True, 'ticketDetails': result}
        else:
            return jsonify({'message': 'Ticket booking failed', 'success': False}), 500
    else:
        return jsonify({'message': 'Invalid request data', 'success': False}), 400

@app.route('/bookingDetails/<bookingId>', methods=['GET', 'POST'])
def bookingDetails(bookingId):
    data=getBookingDetails(bookingId)
    return jsonify({'message': 'Booking details fetched successfully', 'success': True, 'bookingDetails': {data}})
@app.route('/getBookedTickets/<uuid>', methods=['GET'])
def get_booked_tickets(uuid):
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['MovieTicketBooking']
        users = db['Users']
        user = users.find_one({'_id': ObjectId(uuid)})
        if user and 'booked_tickets' in user:
            booked_tickets = user['booked_tickets']
            for ticket in booked_tickets:
                movie_id = int(ticket['movieId'])
                theater_id = int(ticket['theaterId'])
                movie = next((m for m in movies_data if m['id'] == movie_id), None)
                if movie:
                    theater = next((t for t in movie['theaters'] if t['id'] == theater_id), None)
                    if theater:
                        ticket['movie_name'] = movie['title']
          
                        ticket['theater_name'] = theater['name']
                    else:
                        ticket['movie_name'] = 'Unknown'
                        ticket['city_name'] = 'Unknown'
                        ticket['theater_name'] = 'Unknown'
                else:
                    ticket['movie_name'] = 'Unknown'
                    ticket['city_name'] = 'Unknown'
                    ticket['theater_name'] = 'Unknown'
            # Convert ObjectId to string
            user['_id'] = str(user['_id'])
            # Convert to JSON using json.dumps
            user_json = json.dumps(user, default=str)
            return user_json
        else:
            return jsonify({'success': True, 'message': 'No booked tickets found for the user.'})
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error occurred while fetching booked tickets.', 'error': str(e)})

@app.route('/adminLogin', methods=['POST', 'GET'])
def adminLogin():
    data = request.json
    username = data['usernameOrEmail']
    password = data['password']
    print(data)
    if username == 'admin' and password == 'admin':
        session['admin_authenticated'] = True
        return jsonify({'message': 'Admin signed in successfully', 'success': True,'userId':'Admin'})
    else:
        return jsonify({'message': 'Invalid username or password', 'success': False}), 401
@app.route('/admin/AddMovies', methods=['POST', 'GET'])
def addMovies():
    data=request.json
    result=addMovie(data)
    return {'helo':123}
@app.route('/admin/AddCities', methods=['POST'])
def add_cities():
    try:
        cities_data = request.json
        client = MongoClient('mongodb://localhost:27017/')
        db = client['MovieTicketBooking']
        cities_collection = db['Cities']
        
        for city_name, theater_ids in cities_data.items():
            city_query = {'name': city_name}
            existing_city = cities_collection.find_one(city_query)
            if existing_city:
                updated_theater_ids = existing_city.get('theater_ids', []) + theater_ids
                cities_collection.update_one(city_query, {'$set': {'theater_ids': updated_theater_ids}})
            else:
                cities_collection.insert_one({'name': city_name, 'theater_ids': theater_ids})
        
        return jsonify({'message': 'Cities updated/added successfully', 'success': True})
    except Exception as e:
        return jsonify({'message': str(e), 'success': False})

    
from bson import ObjectId

@app.route('/admin/UpdateCity/<city_id>', methods=['POST'])
def update_city(city_id):
    try:
        new_theater_ids = request.json
        client = MongoClient('mongodb://localhost:27017/')
        db = client['MovieTicketBooking']
        cities_collection = db['Cities']
        
        city_query = {'_id': ObjectId(city_id)}
        city_data = cities_collection.find_one(city_query)
        
        if city_data:
            updated_theater_ids = city_data['theater_ids'] + new_theater_ids
            cities_collection.update_one(city_query, {'$set': {'theater_ids': updated_theater_ids}})
            return jsonify({'message': f'Theaters updated successfully for city with _id: {city_id}', 'success': True})
        else:
            return jsonify({'message': f'City with _id {city_id} not found', 'success': False})
    except Exception as e:
        return jsonify({'message': str(e), 'success': False})
    
@app.route('/admin/Cities', methods=['GET'])
def get_cities():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['MovieTicketBooking']
        cities_collection = db['Cities']
        
        # Retrieve all cities from the collection
        cities_data = list(cities_collection.find({}, {'_id': 0}))  # Exclude _id field
        
        return jsonify({'cities': cities_data, 'success': True})
    except Exception as e:
        return jsonify({'message': str(e), 'success': False})

if __name__ == '__main__':
    app.run(port=5000,debug=True)
