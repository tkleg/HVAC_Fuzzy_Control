import skfuzzy.control as ctrl
import numpy as np
import matplotlib.pyplot as plt
from fuzzy_rules import rules
import mins_maxs as mm

controller = ctrl.ControlSystem(rules)
simulator = ctrl.ControlSystemSimulation(controller)

temp = range(mm.TEMP_MIN, mm.TEMP_MAX + 1, 5)
hum = range(mm.HUM_MIN, mm.HUM_MAX + 1, 5)
TEMP, HUM = np.meshgrid(temp, hum)

Z = np.zeros_like(TEMP)

# Iterate through the meshgrid using proper indexing
for i in range(len(temp)):
    for j in range(len(hum)):
        x = TEMP[j, i]  # Temperature value from meshgrid
        y = HUM[j, i]   # Humidity value from meshgrid
        
        simulator.input['temperature'] = x
        simulator.input['humidity'] = y
        simulator.compute()
        
        Z[j, i] = simulator.output['ac_heater_power']  # Store result at correct position
        print(f'Temperature: {x}, Humidity: {y} => AC/Heater Power: {Z[j, i]}')
fig = plt.figure()
ax = plt.axes(projection='3d')

ax.plot3D(TEMP, HUM, Z)
ax.set_xlabel('Temperature (°C)')
ax.set_ylabel('Humidity (%)')
ax.set_zlabel('AC/Heater Power (%)')
ax.set_title('Fuzzy Control Surface for AC/Heater Power')
plt.savefig('fuzzy_control_surface.png')