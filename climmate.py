import pandas as pd
import folium
from folium import plugins
import requests
from datetime import datetime

# Function to fetch live weather data from OpenWeatherMap
def fetch_live_weather_data(api_key, lat, lon):
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for {lat}, {lon}: {response.status_code}")
        return None


def convert_unix_to_datetime(unix_timestamp):
    return datetime.utcfromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')


def get_current_datetime():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


api_key = '45a9478f21851ae5fbc7ef7a6620e15c'


locations = [
    {'Latitude': 27.7172, 'Longitude': 85.3240},  # Kathmandu
    {'Latitude': 28.3949, 'Longitude': 84.1240},  # Pokhara
    {'Latitude': 27.6730, 'Longitude': 85.3240},  # Patan
    {'Latitude': 26.4500, 'Longitude': 87.2833},  # Biratnagar
    {'Latitude': 27.6760, 'Longitude': 83.4474},  # Bhairahawa
    {'Latitude': 27.5700, 'Longitude': 84.3550},  # Hetauda
    {'Latitude': 28.2074, 'Longitude': 83.9856},  # Lekhnath
    {'Latitude': 27.6841, 'Longitude': 83.4323},  # Butwal
    {'Latitude': 29.4004, 'Longitude': 82.1365},  # Jumla
    {'Latitude': 26.8043, 'Longitude': 87.2780},  # Birgunj
    {'Latitude': 28.5000, 'Longitude': 81.2333},  # Dhangadhi
    {'Latitude': 27.5330, 'Longitude': 85.3333},  # Kirtipur
    {'Latitude': 28.0167, 'Longitude': 84.6333},  # Bandipur
    {'Latitude': 26.9167, 'Longitude': 87.2500},  # Itahari        
    {'Latitude': 27.0000, 'Longitude': 84.8667}  # Bharatpur   
]


live_data = []
current_datetime = get_current_datetime()  
for loc in locations:
    lat = loc.get('Latitude')
    lon = loc.get('Longitude')
    if lat is not None and lon is not None:
        weather_data = fetch_live_weather_data(api_key, lat, lon)
        if weather_data and 'main' in weather_data and 'weather' in weather_data and 'dt' in weather_data:
            live_data.append({
                'Latitude': lat,
                'Longitude': lon,
                'Datetime': convert_unix_to_datetime(weather_data['dt']),  
                'Current Time': current_datetime,  
                'Temperature': weather_data['main']['temp'],
                'Weather': weather_data['weather'][0]['description']
            })
        else:
            print(f"Weather data for {lat}, {lon} is missing required keys or is incomplete.")
    else:
        print(f"Location data for {loc} is missing 'Latitude' or 'Longitude'.")


live_df = pd.DataFrame(live_data)

if live_df.empty:
    print("No live data available. Please check the API responses and location coordinates.")
else:
   
    m = folium.Map(location=[live_df['Latitude'].mean(), live_df['Longitude'].mean()], zoom_start=8)

    for idx, row in live_df.iterrows():
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=10,
            popup=f"Date & Time: {row['Datetime']}<br>Current Time: {row['Current Time']}<br>Temperature: {row['Temperature']}°C<br>Weather: {row['Weather']}",
            color='red' if row['Temperature'] > 20 else 'blue',
            fill=True,
            fill_color='red' if row['Temperature'] > 20 else 'blue'
        ).add_to(m)

    heat_data = [[row['Latitude'], row['Longitude'], row['Temperature']] for index, row in live_df.iterrows()]
    plugins.HeatMap(heat_data).add_to(m)

    m.save('temperature_map.html')
    print("Map created and saved to 'temperature_map.html'")
