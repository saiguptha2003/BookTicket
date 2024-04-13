from pymongo import MongoClient

def add_cities_to_database(cities_data):
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['MovieTicketBooking']
        cities_collection = db['Cities']
        
        # Insert cities data into MongoDB
        result = cities_collection.insert_one(cities_data)
        
        if result.inserted_id:
            print('Cities added successfully')
            return True
        else:
            print('Failed to add cities')
            return False
    except Exception as e:
        print('Error:', e)
        return False

# Test the function
cities = {
    'City X': [101],
    'City Y': [102],
    'City Z': [103, 104],
    'City P': [105]
}

add_cities_to_database(cities)
