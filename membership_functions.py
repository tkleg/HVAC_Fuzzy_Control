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
temperature['cold'] = fuzz.trapmf(universes['temperature'], [-15, 5, 12, 18])
temperature['warm'] = fuzz.trapmf(universes['temperature'], [15, 18, 27, 35])
temperature['hot'] = fuzz.trapmf(universes['temperature'], [22, 32, mm.TEMP_MAX, mm.TEMP_MAX])

humidity = ctrl.Antecedent(universes['humidity'], 'humidity')      # 0 to 100%
humidity['dry'] = 1 - fuzz.trapmf(universes['humidity'], [0, 40, mm.HUM_MAX, mm.HUM_MAX])
humidity['comfortable'] = fuzz.trapmf(universes['humidity'], [30, 50, 70, 90])
humidity['humid'] = fuzz.trapmf(universes['humidity'], [60, 90, mm.HUM_MAX, mm.HUM_MAX])

delta_temperature = ctrl.Antecedent(universes['delta_temperature'], 'delta_temperature')  # -10 to 10 degrees Celsius change
delta_temperature['decreasing'] = 1 - fuzz.trapmf(universes['delta_temperature'], [-7,-2, mm.DELTA_TEMP_MAX, mm.DELTA_TEMP_MAX])
delta_temperature['stable'] = fuzz.trimf(universes['delta_temperature'], [-3, 0, 3])
delta_temperature['increasing'] = fuzz.trapmf(universes['delta_temperature'], [2, 7, mm.DELTA_TEMP_MAX, mm.DELTA_TEMP_MAX])

delta_humidity = ctrl.Antecedent(universes['delta_humidity'], 'delta_humidity')  # -20 to 20% change
delta_humidity['decreasing'] = 1 - fuzz.trapmf(universes['delta_humidity'], [-15, -2, mm.DELTA_HUM_MAX, mm.DELTA_HUM_MAX])
delta_humidity['stable'] = fuzz.trimf(universes['delta_humidity'], [-1, 0, 1])  # Much narrower stable zone
delta_humidity['increasing'] = fuzz.trapmf(universes['delta_humidity'], [2, 15, mm.DELTA_HUM_MAX, mm.DELTA_HUM_MAX])

ac_heater_power = ctrl.Consequent(universes['ac_heater_power'], 'ac_heater_power')
ac_heater_power['cooling'] = fuzz.trapmf(universes['ac_heater_power'], [mm.AC_HEATER_POWER_MIN, mm.AC_HEATER_POWER_MIN, -20, 15])
ac_heater_power['off'] = fuzz.trimf(universes['ac_heater_power'], [-5, 0, 15])
ac_heater_power['heating'] = fuzz.trapmf(universes['ac_heater_power'], [-5, 30, mm.AC_HEATER_POWER_MAX, mm.AC_HEATER_POWER_MAX])

humidifier_dehumidifier_power = ctrl.Consequent(universes['humidifier_dehumidifier_power'], 'humidifier_dehumidifier_power')
humidifier_dehumidifier_power['dehumidifying'] = 1 - fuzz.trapmf(universes['humidifier_dehumidifier_power'], [-60, -20, mm.HUMIDIFIER_DEHUMIDIFIER_POWER_MAX, mm.HUMIDIFIER_DEHUMIDIFIER_POWER_MAX])
humidifier_dehumidifier_power['off'] = fuzz.trimf(universes['humidifier_dehumidifier_power'], [-25, 0, 25])
humidifier_dehumidifier_power['humidifying'] = fuzz.trimf(universes['humidifier_dehumidifier_power'], [20, mm.HUMIDIFIER_DEHUMIDIFIER_POWER_MAX, mm.HUMIDIFIER_DEHUMIDIFIER_POWER_MAX])
# Weighted cooling (1.5x importance, but clamped to max 1.0)
#ac_heater_power['cooling_temp'] = np.minimum(ac_heater_power['cooling'].mf * 1.5, 1.0)

# Weighted heating (1.5x importance, but clamped to max 1.0) 
#ac_heater_power['heating_temp'] = np.minimum(ac_heater_power['heating'].mf * 1.5, 1.0)

# Weighted off (1.5x importance, but clamped to max 1.0)
#ac_heater_power['off_temp'] = np.minimum(ac_heater_power['off'].mf * 1.5, 1.0)

variables = {'temperature': temperature, 'humidity': humidity, 'ac_heater_power': ac_heater_power,
             'humidifier_dehumidifier_power': humidifier_dehumidifier_power,
             'delta_temperature': delta_temperature, 
             'delta_humidity': delta_humidity
            }

units = {'temperature': '°C', 'humidity': '%', 'delta_temperature': '°C', 'delta_humidity': '%',
         'ac_heater_power': '%', 'humidifier_dehumidifier_power': '%'}