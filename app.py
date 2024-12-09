
from flask import Flask, render_template, request, redirect, url_for, make_response
import json
import csv
import os

app = Flask(__name__)

def get_scenarios():
    try:
        with open('scenarios.json', 'r') as f:
            scenarios = json.load(f)
    except FileNotFoundError:
        scenarios = []
    return scenarios

def save_user_details(details):
    file_exists = os.path.isfile('user_details.csv')
    with open('user_details.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['First Name', 'Last Name', 'Email', 'Address', 'Zip Code', 'Country', 'City', 'Preference Message'])
        writer.writerow(details)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/current_patterns')
def current_patterns():
    return render_template('current_patterns.html')

@app.route('/baseline', methods=['GET', 'POST'])
def baseline():
    if request.method == 'POST':
        car_usage = request.form.get('carUsage', type=int)
        public_transport_usage = request.form.get('publicTransportUsage', type=int)
        avg_travel_time = request.form.get('avgTravelTime', type=int)
        avg_cost = request.form.get('avgCost', type=float)

        data = {
            'car': car_usage,
            'public_transport': public_transport_usage,
            'avg_travel_time': avg_travel_time,
            'avg_cost': avg_cost
        }

        return render_template('baseline.html', data=data)
    else:
        return render_template('baseline.html')

@app.route('/policy_builder', methods=['GET', 'POST'])
def policy_builder():
    if request.method == 'POST':
        try:
            bus_time_reduction = request.form.get('busTimeReduction', type=int)
            parking_fee_increase = request.form.get('parkingFeeIncrease', type=int)
            bus_frequency = request.form.get('busFrequency', type=int)
            park_and_ride = request.form.get('parkAndRide') == 'yes'

            # Calculate projected mode share (dummy calculation)
            projected_mode_share = {
                "car": max(0, 100 - bus_time_reduction - parking_fee_increase - bus_frequency),
                "public_transport": min(100, bus_time_reduction + parking_fee_increase + bus_frequency),
                "avg_travel_time": 30 - bus_time_reduction,
                "avg_cost": 10 + parking_fee_increase,
                "car_trips_avoided": bus_time_reduction * 10,
                "emissions_reduction": bus_time_reduction * 0.5
            }

            scenarios = get_scenarios()
            scenarios.append({
                "inputs": {
                    "bus_time_reduction": bus_time_reduction,
                    "parking_fee_increase": parking_fee_increase,
                    "bus_frequency": bus_frequency,
                    "park_and_ride": park_and_ride
                },
                "outputs": projected_mode_share
            })

            with open('scenarios.json', 'w') as f:
                json.dump(scenarios, f)

            return render_template('result.html', data=projected_mode_share)
        except Exception as e:
            return render_template('result.html', error=str(e))
    else:
        return render_template('policy_builder.html')

@app.route('/result', methods=['POST'])
def result():
    try:
        bus_time_reduction = request.form.get('busTimeReduction', type=int)
        parking_fee_increase = request.form.get('parkingFeeIncrease', type=int)
        bus_frequency = request.form.get('busFrequency', type=int)
        park_and_ride = request.form.get('parkAndRide') == 'yes'

        # Calculate projected mode share (dummy calculation)
        projected_mode_share = {
            "car": max(0, 100 - bus_time_reduction - parking_fee_increase - bus_frequency),
            "public_transport": min(100, bus_time_reduction + parking_fee_increase + bus_frequency),
            "avg_travel_time": 30 - bus_time_reduction,
            "avg_cost": 10 + parking_fee_increase,
            "car_trips_avoided": bus_time_reduction * 10,
            "emissions_reduction": bus_time_reduction * 0.5
        }

        scenarios = get_scenarios()
        scenarios.append({
            "inputs": {
                "bus_time_reduction": bus_time_reduction,
                "parking_fee_increase": parking_fee_increase,
                "bus_frequency": bus_frequency,
                "park_and_ride": park_and_ride
            },
            "outputs": projected_mode_share
        })

        with open('scenarios.json', 'w') as f:
            json.dump(scenarios, f)

        return render_template('result.html', data=projected_mode_share)
    except Exception as e:
        return render_template('result.html', error=str(e))

@app.route('/comparison')
def comparison():
    scenarios = get_scenarios()
    return render_template('comparison.html', scenarios=scenarios)

@app.route('/delete_scenario/<int:index>', methods=['POST'])
def delete_scenario(index):
    try:
        scenarios = get_scenarios()
        if 0 <= index < len(scenarios):
            scenarios.pop(index)
            with open('scenarios.json', 'w') as f:
                json.dump(scenarios, f)
    except Exception as e:
        return str(e)
    return redirect(url_for('comparison'))

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['email']
        address = request.form['address']
        zip_code = request.form['zipCode']
        country = request.form['country']
        city = request.form['city']
        message = request.form['message']

        user_details = [first_name, last_name, email, address, zip_code, country, city, message]
        save_user_details(user_details)

        response = make_response(redirect(url_for('index')))
        response.set_cookie('isSignedIn', 'true')
        return response
    return render_template('sign_in.html')

@app.route('/google_sign_in')
def google_sign_in():
    # Implement Google Sign-In logic here
    return redirect(url_for('index'))

# Other routes and logic...

if __name__ == '__main__':
    app.run(debug=True)