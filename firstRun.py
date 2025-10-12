import os
import skfuzzy.control as ctrl
import numpy as np
import matplotlib.pyplot as plt
from fuzzy_rules import rules
import mins_maxs as mm
from environment_simulator import calc_new_temp_and_hum

controller = ctrl.ControlSystem(rules)
simulator = ctrl.ControlSystemSimulation(controller)

initial_temp = 22  # Initial room temperature in Celsius
initial_hum = 50   # Initial room humidity in percentage
initial_delta_temp = 0  # Initial change in temperature

cur_temp = initial_temp
cur_hum = initial_hum
cur_delta_temp = initial_delta_temp

temps = [initial_temp]
hums = [initial_hum]
delta_temps = [initial_delta_temp]

for hour in range(24*14):
    # Set inputs
    simulator.input['temperature'] = cur_temp
    simulator.input['humidity'] = cur_hum
    simulator.input['delta_temperature'] = cur_delta_temp

    # Compute the control action
    simulator.compute()

    # Get the output values
    heating_power = simulator.output['ac_heater_power']

    new_data = calc_new_temp_and_hum(cur_temp, cur_hum, heating_power, hour)
    new_temp = new_data['temperature']
    new_hum = new_data['humidity']



    # Store the results
    temps.append(cur_temp)
    hums.append(cur_hum)
    delta_temps.append(cur_delta_temp)

    cur_delta_temp = new_temp - cur_temp
    cur_temp = new_temp
    cur_hum = new_hum

plt.plot(temps, label='Temperature over Time')
#plt.plot(hums, label='Humidity (%)')
plt.xlabel('Time (hours)')
plt.ylabel('Temperature (°C)')
plt.title('Room Temperature Over Time with Fuzzy Logic Control')
plt.grid()
plt.savefig('temperature_over_time.png')
plt.clf()

plt.plot(delta_temps, label='Delta Temperature over Time')
plt.xlabel('Time (hours)')
plt.ylabel('Delta Temperature (°C)')
plt.title('Change in Room Temperature Over Time with Fuzzy Logic Control')
plt.grid()
plt.savefig('delta_temperature_over_time.png')

#print( list( map( float, temps) ) )