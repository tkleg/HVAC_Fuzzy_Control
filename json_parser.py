import json
import numpy as np
from scipy.interpolate import CubicSpline
#from matplotlib import pyplot as plt

##Read JSON file
with open('output.json', 'r') as file:
    data = json.load(file)

temps = []
humidities = []
#Command to get JSON file from weatherapi.com
# curl "http://api.weatherapi.com/v1/forecast.json?key=**REDACTED**&q=31207&days=14&aqi=yes&alerts=yes" -o output.json
#extract forecasts
#14 days, 24 Hrs each days
forecasts = data['forecast']['forecastday']
for index_day, day in enumerate(forecasts):
    for index_hr, hour in enumerate(day['hour']):
        temps.append(hour['temp_c'])
        humidities.append(hour['humidity'])

#percent_noise = 1 # Percent noise to add
#Convert to numpy arrays
#temps = np.array(temps) * np.random.uniform( 1 - percent_noise / 100, 1 + percent_noise / 100, size=len(temps))
#humidities = np.array(humidities) * np.random.uniform(1 - percent_noise / 100, 1 + percent_noise / 100, size=len(humidities))

#Cubic Spline Interpolation
x = np.arange(0, 24*14, 1)
outdoor_temp_by_hour = CubicSpline(x, temps)
outdoor_humidity_by_hour = CubicSpline(x, humidities)

if __name__ == "__main__":
    print( len(temps), len(humidities) )
    #x_smooth = np.linspace(0, 24*14-1, 1000)

    #plt.scatter(x, temps, label='temp data', color='red')

    #plt.plot(x, cs_temps(x), label='Cubic Spline Temp')

    #plt.savefig('cubic_spline_temp.png')