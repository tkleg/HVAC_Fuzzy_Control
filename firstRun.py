import skfuzzy.control as ctrl
import matplotlib.pyplot as plt
from fuzzy_rules import rules
from environment_simulator import calc_new_temp_and_hum
from json_parser import json_to_splines

splines = json_to_splines()

controller = ctrl.ControlSystem(rules)
simulator = ctrl.ControlSystemSimulation(controller)

seconds = int(input("Enter the number of seconds for each step: "))
#15 second step
step = seconds / 60 / 60

start = 0 

cur_time = start

outdoor_temps = [16.3]

initial_temp = float(input("Enter the initial room temperature (in °C): "))
initial_hum = float(input("Enter the initial room humidity (in %): "))
initial_delta_temp = 0  # Initial change in temperature
initial_delta_hum = 0  # Initial change in humidity

cur_temp = initial_temp
cur_hum = initial_hum
cur_delta_temp = initial_delta_temp
cur_delta_hum = initial_delta_hum

temps = [initial_temp]
hums = [initial_hum]
delta_temps = [initial_delta_temp]
delta_hums = [initial_delta_hum]
times = [0]
#336 hours = 14 days

max_time = int(input("Enter the total number of hours to simulate: "))

max_ac_power = float(input("Enter the maximum AC/Heater power (in W): "))
wall_heat_loss_factor = float(input("Enter the wall heat loss factor: "))
while cur_time < max_time:
    # Set inputs
    simulator.input['temperature'] = cur_temp
    simulator.input['humidity'] = cur_hum
    simulator.input['delta_temperature'] = cur_delta_temp
    simulator.input['delta_humidity'] = cur_delta_hum
    # Compute the control action
    simulator.compute()

    # Get the output values
    heating_power = simulator.output['ac_heater_power']
    humidifier_power = simulator.output['humidifier_dehumidifier_power']

    new_data = calc_new_temp_and_hum(cur_temp, cur_hum, heating_power, humidifier_power, cur_time, seconds, splines, max_ac_power, wall_heat_loss_factor)
    new_temp = new_data['temperature']
    new_hum = new_data['humidity']

    print(f"Time: {cur_time:.6f} hrs, Temp: {cur_temp:.6f} C, Humidity: {cur_hum:.6f} %, Delta Temp: {cur_delta_temp:.6f} C, Heating Power: {heating_power:.6f} % -> New Temp: {new_temp:.6f} C, New Humidity: {new_hum:.6f} %, Outdoor Temp: {new_data['outdoor_temperature']:.6f} C")
    # Store the results
    temps.append(cur_temp)
    hums.append(cur_hum)
    delta_temps.append(cur_delta_temp)
    outdoor_temps.append(new_data['outdoor_temperature'])

    cur_delta_temp = new_temp - cur_temp
    cur_temp = new_temp
    cur_hum = new_hum
    cur_time += step
    times.append(cur_time)

plt.plot(times, temps, label='Temperature over Time', lw=1)
plt.plot(times, outdoor_temps, label='Outdoor Temperature over Time', lw=1)
#plt.plot(hums, label='Humidity (%)')
plt.xlabel('Time (hours)')
plt.ylabel('Temperature (°C)')
plt.title('Room Temperature Over Time with Fuzzy Logic Control')
plt.grid()
plt.legend()
plt.savefig('results/temperature_over_time.png')
plt.clf()

plt.plot(times, hums, label='Humidity over Time', lw = 1)
plt.xlabel('Time (hours)')
plt.ylabel('Humidity (%)')
plt.title('Room Humidity Over Time with Fuzzy Logic Control')
plt.grid()
plt.legend()
plt.savefig('results/humidity_over_time.png')
plt.clf()

times.pop(0)
delta_temps.pop(0)
plt.plot(times, delta_temps, label='Delta Temperature over Time', lw = 1)
plt.xlabel('Time (hours)')
plt.ylabel('Delta Temperature (°C)')
plt.title('Change in Room Temperature Over Time with Fuzzy Logic Control')
plt.grid()
plt.legend()
plt.savefig('results/delta_temperature_over_time.png')
#print( list( map( float, temps) ) )