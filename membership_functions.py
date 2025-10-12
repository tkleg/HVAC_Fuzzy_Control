import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import mins_maxs as mm
from universes import universes

# Define the universe of discourse for temperature and humidity
#delta_temp = ctrl.Antecedent(np.linspace(-100, 100, num_points), 'delta_temp')  # -100 to 100 degrees Celsius change
#delta_humidity = ctrl.Antecedent(np.linspace(-100, 100, num_points), 'delta_humidity')  # -100 to 100% change

temperature = ctrl.Antecedent(universes['temperature'], 'temperature')  # -50 to 50 degrees Celsius
temperature['freezing'] = 1 - fuzz.trapmf(universes['temperature'], [-20, 0, mm.TEMP_MAX, mm.TEMP_MAX])
temperature['cold'] = fuzz.trapmf(universes['temperature'], [-20, 0, 5, 8])
temperature['warm'] = fuzz.trapmf(universes['temperature'], [5, 10, 20, 30])
temperature['hot'] = fuzz.trapmf(universes['temperature'], [20, 35, mm.TEMP_MAX, mm.TEMP_MAX])

humidity = ctrl.Antecedent(universes['humidity'], 'humidity')      # 0 to 100%
humidity['dry'] = 1 - fuzz.trapmf(universes['humidity'], [0, 20, mm.HUM_MAX, mm.HUM_MAX])
humidity['comfortable'] = fuzz.trapmf(universes['humidity'], [15, 35, 55, 70])
humidity['humid'] = fuzz.trapmf(universes['humidity'], [45, 70, mm.HUM_MAX, mm.HUM_MAX])

delta_temperature = ctrl.Antecedent(universes['delta_temperature'], 'delta_temp')  # -10 to 10 degrees Celsius change
delta_temperature['decreasing'] = 1 - fuzz.trapmf(universes['delta_temperature'], [-7,-2, mm.DELTA_TEMP_MAX, mm.DELTA_TEMP_MAX])
delta_temperature['stable'] = fuzz.trimf(universes['delta_temperature'], [-3, 0, 3])
delta_temperature['increasing'] = fuzz.trapmf(universes['delta_temperature'], [2, 7, mm.DELTA_TEMP_MAX, mm.DELTA_TEMP_MAX])

delta_humidity = ctrl.Antecedent(universes['delta_humidity'], 'delta_hum')  # -20 to 20% change
delta_humidity['decreasing'] = 1 - fuzz.trapmf(universes['delta_humidity'], [-15, -5, mm.DELTA_HUM_MAX, mm.DELTA_HUM_MAX])
delta_humidity['stable'] = fuzz.trimf(universes['delta_humidity'], [-7, 0, 7])
delta_humidity['increasing'] = fuzz.trapmf(universes['delta_humidity'], [5, 15, mm.DELTA_HUM_MAX, mm.DELTA_HUM_MAX])

ac_heater_power = ctrl.Consequent(universes['ac_heater_power'], 'ac_heater_power')
ac_heater_power['cooling'] = 1 - fuzz.trapmf(universes['ac_heater_power'], [-50, 0, mm.AC_HEATER_POWER_MAX, mm.AC_HEATER_POWER_MAX])
ac_heater_power['off'] = fuzz.trimf(universes['ac_heater_power'], [-10, 0, 10])
ac_heater_power['heating'] = fuzz.trimf(universes['ac_heater_power'], [0, mm.AC_HEATER_POWER_MAX, mm.AC_HEATER_POWER_MAX])

# Weighted cooling (1.5x importance, but clamped to max 1.0)
#ac_heater_power['cooling_temp'] = np.minimum(ac_heater_power['cooling'].mf * 1.5, 1.0)

# Weighted heating (1.5x importance, but clamped to max 1.0) 
#ac_heater_power['heating_temp'] = np.minimum(ac_heater_power['heating'].mf * 1.5, 1.0)

# Weighted off (1.5x importance, but clamped to max 1.0)
#ac_heater_power['off_temp'] = np.minimum(ac_heater_power['off'].mf * 1.5, 1.0)

variables = {'temperature': temperature, 'humidity': humidity, 'ac_heater_power': ac_heater_power,
             'delta_temperature': delta_temperature, 'delta_humidity': delta_humidity}
units = {'temperature': '°C', 'humidity': '%', 'delta_temperature': '°C', 'delta_humidity': '%',
         'ac_heater_power': '%'}