import skfuzzy.control as ctrl
import matplotlib.pyplot as plt
from fuzzy_rules import rules
from environment_simulator import calc_new_temp_and_hum
from json_parser import json_to_splines
import random
import numpy as np

splines = json_to_splines()

controller = ctrl.ControlSystem(rules)
simulator = ctrl.ControlSystemSimulation(controller)

seconds = int(input("Enter the number of seconds for each step: "))

#step is in hours
step = seconds / 3600

start = 0 

cur_time = start

outdoor_temps = [16.3]

#initial_temp = -5 + splines['temperature'](0) * random.uniform(0.9, 1.1)  # %10 variation in initial temperature
initial_temp = 17.5
initial_hum = 50.0
#initial_hum = 5 + splines['humidity'](0) * random.uniform(0.9, 1.1)  # %10 variation in initial humidity
initial_delta_temp = 0  # Initial change in temperature
#initial_delta_hum = -5  # Initial change in humidity

cur_temp = initial_temp
cur_hum = initial_hum
cur_delta_temp = initial_delta_temp
#cur_delta_hum = initial_delta_hum

temps = [initial_temp]
hums = [initial_hum]
delta_temps = [initial_delta_temp]
#delta_hums = [initial_delta_hum]
times = [0]
#336 hours = 14 days

ac_control_data = []
hum_control_data = []

max_time = int(input("Enter the total number of hours to simulate: "))

max_ac_power = float(input("Enter the maximum AC/Heater power (in W): "))
wall_heat_loss_factor = float(input("Enter the wall heat loss factor: "))
while cur_time < max_time:
    # Set inputs
    simulator.input['temperature'] = cur_temp
    simulator.input['humidity'] = cur_hum
    simulator.input['delta_temperature'] = cur_delta_temp
    #simulator.input['delta_humidity'] = cur_delta_hum
    # Compute the control action
    print(f"Computing for Time: {cur_time:.6f} hrs, Temp: {cur_temp:.6f} C, Humidity: {cur_hum:.6f} %, Delta Temp: {cur_delta_temp:.6f} C")
    simulator.compute()

    # Get the output values
    try:
        heating_power = simulator.output['ac_heater_power']
    except KeyError:
        print('inputs:', simulator.input)
        exit(1)
    humidifier_power = simulator.output['humidifier_dehumidifier_power']

    new_data = calc_new_temp_and_hum(cur_temp, cur_hum, heating_power, humidifier_power, cur_time, seconds, splines, max_ac_power, wall_heat_loss_factor)
    new_temp = new_data["outputs"]['temperature']
    new_hum = new_data["outputs"]['humidity']
    ac_control_data.append(new_data['ac_heater_control'])
    hum_control_data.append(new_data['humidifier_control'])

    print(f"Time: {cur_time:.6f} hrs, Temp: {cur_temp:.6f} C, Humidity: {cur_hum:.6f} %, Delta Temp: {cur_delta_temp:.6f} C, Heating Power: {heating_power:.6f} % -> New Temp: {new_temp:.6f} C, New Humidity: {new_hum:.6f} %, Outdoor Temp: {splines['temperature'](cur_time):.6f} C")

    # Store the results
    temps.append(cur_temp)
    hums.append(cur_hum)
    delta_temps.append(cur_delta_temp)
    outdoor_temps.append(splines['temperature'](cur_time))

    cur_delta_temp = new_temp - cur_temp
    #cur_delta_hum = new_hum - cur_hum

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
plt.tight_layout()
plt.savefig('results/temperature_over_time.png')
plt.clf()

plt.plot(times, hums, label='Humidity over Time', lw = 1)
plt.plot(times, [splines['humidity'](t) for t in times], label='Outdoor Humidity over Time', lw = 1)
plt.xlabel('Time (hours)')
plt.ylabel('Humidity (%)')
plt.title('Room Humidity Over Time with Fuzzy Logic Control')
plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig('results/humidity_over_time.png')
plt.clf()


plt.plot(times[2:], delta_temps[2:], label='Delta Temperature over Time', lw = 1)
#plt.plot(times, np.array(temps) - np.array(outdoor_temps), label='Temperature Difference (Indoor - Outdoor)', lw = 1)
plt.xlabel('Time (hours)')
plt.ylabel('Delta Temperature (°C)')
plt.title('Change in Room Temperature Over Time with Fuzzy Logic Control')
plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig('results/delta_temperature_over_time.png')
plt.clf()

plt.plot(times[1:], ac_control_data, label='AC/Heater Control Signal', lw = 1)
plt.xlabel('Time (hours)')
plt.ylabel('AC/Heater Control (%)')
plt.title('AC/Heater Control Signal Over Time')
plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig('results/ac_heater_control_over_time.png')
plt.clf()

plt.plot(times[1:], hum_control_data, label='Humidifier/Dehumidifier Control Signal', lw = 1)
plt.xlabel('Time (hours)')
plt.ylabel('Humidifier/Dehumidifier Control (%)')
plt.title('Humidifier/Dehumidifier Control Signal Over Time')
plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig('results/humidifier_dehumidifier_control_over_time.png')
plt.clf()

time_to_begin_delta_temp = float(input("Enter the time in hours of when the delta temperature graph should begin: "))
shift_help = np.array(times[2:]) >= time_to_begin_delta_temp
delta_temps_shifted = np.array(delta_temps)[2:][shift_help]
times_delta_temp_shifted = np.array(times)[2:][shift_help]
plt.plot(times_delta_temp_shifted, delta_temps_shifted, label='Delta Temperature over Time', lw = 1)
plt.xlabel('Time (hours)')
plt.ylabel('Delta Temperature (°C)')
plt.title('Change in Room Temperature Over Time with Fuzzy Logic Control (Shifted)')
plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig('results/shifted/delta_temperature_over_time_shifted.png')
plt.clf()

time_to_begin_ac_control = float(input("Enter the time in hours of when the AC/Heater control graph should begin: "))
shift_help_ac = np.array(times[1:]) >= time_to_begin_ac_control
ac_control_data_shifted = np.array(ac_control_data)[shift_help_ac]
times_ac_control_shifted = np.array(times)[1:][shift_help_ac]
plt.plot(times_ac_control_shifted, ac_control_data_shifted, label='AC/Heater Control Signal', lw = 1)
plt.xlabel('Time (hours)')
plt.ylabel('AC/Heater Control (%)')
plt.title('AC/Heater Control Signal Over Time (Shifted)')
plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig('results/shifted/ac_heater_control_over_time_shifted.png')
plt.clf()

time_to_begin_hum_control = float(input("Enter the time in hours of when the Humidifier/Dehumidifier control graph should begin: "))
shift_help_hum = np.array(times[1:]) >= time_to_begin_hum_control
hum_control_data_shifted = np.array(hum_control_data)[shift_help_hum]
times_hum_control_shifted = np.array(times)[1:][shift_help_hum]
plt.plot(times_hum_control_shifted, hum_control_data_shifted, label='Humidifier/Dehumidifier Control Signal', lw = 1)
plt.xlabel('Time (hours)')
plt.ylabel('Humidifier/Dehumidifier Control (%)')
plt.title('Humidifier/Dehumidifier Control Signal Over Time (Shifted)')
plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig('results/shifted/humidifier_dehumidifier_control_over_time_shifted.png')
plt.clf()