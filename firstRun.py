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

cur_temp = initial_temp
cur_hum = initial_hum

temps = [initial_temp]
hums = [initial_hum]

for hour in range(24*14):
    # Set inputs
    rules.input['temperature'] = cur_temp
    rules.input['humidity'] = cur_hum
    rules.input[]

    # Compute the control action
    rules.compute()

    # Get the output values
    heating_power = rules.output['ac_heater_power']

    new_data = calc_new_temp_and_hum(cur_temp, cur_hum, heating_power, hour)
    new_temp = new_data['temperature']
    new_hum = new_data['humidity']



    # Store the results
    temps.append(cur_temp)
    hums.append(cur_hum)