import uuid
from flask import Flask, json, request, jsonify, session

app = Flask(__name__)
app.secret_key = '925555fc-f493-11ee-96ea-900f0c7891b4'
from flask_cors import CORS
CORS(app)

# Mock data for movies, theaters, seats, etc.
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
    # Your addUser function logic goes here
    return jsonify({'message': 'User signed up successfully'})

@app.route('/signin', methods=['POST'])
def signin():
    data = request.json
    usernameOrEmail = data['username'].strip().lower()
    password = data['password'].strip()
    # Your checkUser function logic goes here
    user_id = 1  # Placeholder for user ID
    username = "example_username"  # Placeholder for username
    session['user_id'] = user_id
    session['username'] = username
    session['sessionId'] = str(uuid.uuid1())
    session['authenticated'] = True
    return jsonify({'message': 'User signed in successfully'})

@app.route('/movies', methods=['GET'])
def get_movies():
    return jsonify(movies_data)

@app.route('/theaters/<int:movie_id>', methods=['GET'])
def get_theaters(movie_id):
    movie = next((movie for movie in movies_data if movie['id'] == movie_id), None)
    if movie:
        return jsonify(movie['theaters'])
    else:
        return jsonify({'error': 'Movie not found'}), 404

@app.route('/book', methods=['POST'])
def book_seat():
    data = request.json
    seat_id = data.get('seat_id')
    if seat_id:
        return jsonify({'message': 'Seat booked successfully'})
    else:
        return jsonify({'error': 'Seat ID not provided'}), 400

if __name__ == '__main__':
    app.run(port=5000)
