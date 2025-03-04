from flask import Blueprint, jsonify, render_template
import random
import names

main = Blueprint('main', __name__)

# ... [Keep the generate_random_stations() function from previous answer] ...

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/api/stations')
def get_stations():
    stations = generate_random_stations(10)
    return jsonify([{
        'number': s['number'],
        'name': s['name'],
        'position': s['position'],
        'bikes': s['available_bikes'],
        'stands': s['available_bike_stands'],
        'address': s['address'],
        'capacity': s['capacity']
    } for s in stations])
