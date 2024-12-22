from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import sqlite3
import requests
import matplotlib.pyplot as plt
import io

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database file
DB_FILE = 'weather_data.db'
API_KEY = '91c233a7eb3141bcdcbafa5f16d66182'  

# Ensure database exists
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                temperature REAL,
                humidity INTEGER,
                description TEXT
            )
        ''')
        conn.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_city', methods=['POST'])
def add_city():
    city = request.form['city']
    if not city:
        flash("City name cannot be empty!", "error")
        return redirect(url_for('home'))

    # Fetch weather data
    weather_data = fetch_weather(city)
    if weather_data:
        save_to_db(city, weather_data)
        flash(f"Weather data for {city} added successfully!", "success")
    else:
        flash(f"Failed to fetch weather data for {city}. Please check the city name.", "error")

    return redirect(url_for('home'))

@app.route('/weather')
def weather():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT city, temperature, humidity, description FROM weather')
        data = cursor.fetchall()
    return render_template('weather.html', weather_data=data)

@app.route('/plot')
def plot():
    # Generate a plot of weather data
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT city, temperature FROM weather')
        data = cursor.fetchall()

    if not data:
        flash("No weather data available to plot.", "error")
        return redirect(url_for('weather'))

    cities = [row[0] for row in data]
    temperatures = [row[1] for row in data]

    plt.figure(figsize=(10, 6))
    plt.bar(cities, temperatures, color='skyblue')
    plt.title('City Temperatures')
    plt.xlabel('City')
    plt.ylabel('Temperature (°C)')
    plt.tight_layout()

    #in-memory buffer to store the plot and deleted after application stop
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')

def fetch_weather(city):
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        return {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description']
        }
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None

def save_to_db(city, weather_data):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO weather (city, temperature, humidity, description)
            VALUES (?, ?, ?, ?)
        ''', (city, weather_data['temperature'], weather_data['humidity'], weather_data['description']))
        conn.commit()

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
