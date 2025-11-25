import json
import numpy as np
from scipy.interpolate import CubicSpline
from matplotlib import pyplot as plt

def json_to_splines():
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
    for day in forecasts:
        for hour in day['hour']:
            temps.append(hour['temp_c'])
            humidities.append(hour['humidity'])
            
    #Cubic Spline Interpolation
    x = np.arange(0, 24*14, 1)
    return { "temperature": CubicSpline(x, temps), "humidity": CubicSpline(x, humidities) }

if __name__ == "__main__":
    splines = json_to_splines()
    outdoor_temp_by_hour = splines['temperature']
    outdoor_humidity_by_hour = splines['humidity']
    print( f"Start outdoor temp: {outdoor_temp_by_hour(0)}" )
    print( f"End outdoor temp: {outdoor_temp_by_hour(3)}" )
    print( f"Start outdoor hum: {outdoor_humidity_by_hour(0)}" )
    print( f"End outdoor hum: {outdoor_humidity_by_hour(3)}" )
    x_smooth = np.linspace(0, 24*14-1, 1000)
    x = np.arange(0, 24*14, 1)
    temps = [outdoor_temp_by_hour(xi) for xi in x]
    plt.scatter(x, temps, label='Temperature', color='red')

    plt.plot(x, outdoor_temp_by_hour(x), label='Cubic Spline Temp')

    plt.xlabel('Hour')
    plt.ylabel('Temperature (\u00B0C)')
    plt.title('Cubic Spline Interpolation of Temperature over 14 Days')
    plt.legend()
    plt.savefig('misc/cubic_spline_temp.png')