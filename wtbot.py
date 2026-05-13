import requests, sys, os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.getenv('DOTENV_FILE_PATH'))

ir = os.getenv('ir').split(' ')
kv = os.getenv('kv').split(' ')
REPORT = os.getenv('report')

url = "https://api.open-meteo.com/v1/forecast"
params = {"timezone": "Europe/Kyiv"}

if len(sys.argv) == 1:
    print("select location !!!")
    exit()

if len(sys.argv) > 1:
    params['current'] = ["temperature_2m", "relativehumidity_2m", "wind_speed_10m", "precipitation_probability"]
    
    if sys.argv[1] ==  'kv':
        params['latitude'] = kv[0] 
        params['longitude'] = kv[1]

    elif sys.argv[1] ==  'ir':
        params['latitude'] = ir[0] 
        params['longitude'] = ir[1]

if len(sys.argv) == 3:
    if sys.argv[2] == 'd':
        params['forecast_days'] = 1
        params['hourly'] = ["temperature_2m", "precipitation_probability"]

    elif sys.argv[2] == 'w':
        params['forecast_days'] = 7
        params['daily'] = ["temperature_2m_max", "temperature_2m_min", "precipitation_probability_max"]

responses = requests.get(url, params=params)
data = responses.json()

if len(sys.argv) == 2:
    message = "Temperature 👉  " + str(data['current']['temperature_2m']) + "°C\nRelative Humidity 👉  " + str(data['current']['relativehumidity_2m']) + "%\nPrecipitation Probability 👉  " + str(data['current']['precipitation_probability']) + "%\nWind Speed 👉  " + str(data['current']['wind_speed_10m']) + "km/h"
    with open(REPORT, 'w') as f: f.write(message)
    print(message)

elif len(sys.argv) == 3:
    if sys.argv[2] == 'd':
        for id, i in enumerate(data['hourly']['time']):
            tmp = str(data['hourly']['temperature_2m'][id])
            prc_prb = str(data['hourly']['precipitation_probability'][id])
            message = i.split('T')[-1] + ' 👉  ' + tmp + '°C    ' + prc_prb + '%'
            with open(REPORT, 'a') as f: f.write(message+'\n')
            print(message)
    
    elif sys.argv[2] == 'w':
        for id, i in enumerate(data['daily']['time']):
            max_tmp = str(data['daily']['temperature_2m_max'][id])
            min_tmp = str(data['daily']['temperature_2m_min'][id])
            max_prc_prb = str(data['daily']['precipitation_probability_max'][id]) 
            message = i.split('-')[-1] + ' 👉  ' + max_tmp + '/' + min_tmp + '°C    ' + max_prc_prb + '%'
            with open(REPORT, 'a') as f: f.write(message+'\n')
            print(message)
