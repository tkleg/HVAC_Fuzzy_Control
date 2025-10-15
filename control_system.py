import os
import skfuzzy.control as ctrl
import numpy as np
import matplotlib.pyplot as plt
from fuzzy_rules import rules
import mins_maxs as mm

controller = ctrl.ControlSystem(rules)
simulator = ctrl.ControlSystemSimulation(controller)

temp = range(mm.TEMP_MIN, mm.TEMP_MAX + 1, 1)
hum = range(mm.HUM_MIN, mm.HUM_MAX + 1, 1)
TEMP, HUM = np.meshgrid(temp, hum)

Z = np.zeros_like(TEMP)

# Iterate through the meshgrid using proper indexing
for i in range(len(temp)):
    for j in range(len(hum)):
        x = TEMP[j, i]  # Temperature value from meshgrid
        y = HUM[j, i]   # Humidity value from meshgrid
        
        simulator.input['temperature'] = x
        simulator.input['humidity'] = y
        simulator.input['delta_temperature'] = 0
        simulator.input['delta_humidity'] = 0
        simulator.compute()
        
        Z[j, i] = simulator.output['ac_heater_power']  # Store result at correct position
        print(f'Temperature: {x}, Humidity: {y} => AC/Heater Power: {Z[j, i]}')

fig = plt.figure(figsize=(10, 7))
ax = plt.axes(projection='3d')

# Use plot_surface instead of plot3D for better color mapping
surf = ax.plot_surface(TEMP, HUM, Z, cmap='viridis', alpha=0.8, 
                      linewidth=0)

ax.set_xlabel('Temperature (°C)')
ax.set_ylabel('Humidity (%)')
ax.set_zlabel('AC/Heater Power (%)')
ax.set_title('Fuzzy Control Surface for AC/Heater Power')

# Add color scale/colorbar
colorbar = fig.colorbar(surf, shrink=0.5, aspect=20, pad=0.1)
colorbar.set_label('AC/Heater Power (%)', rotation=270, labelpad=20)

max_file_num = 0
print( os.listdir('outputs/ac_heater_power'))
for file in os.listdir('outputs/ac_heater_power'):
    max_file_num = max(max_file_num, int(file[file.index('_')+1:file.index('.png')]))
max_file_num += 1

ac_heater_power_output_path = f'outputs/ac_heater_power/surface_{max_file_num}.png'
plt.savefig(ac_heater_power_output_path, dpi=300, bbox_inches='tight')
print(f'AC/Heater power surface saved to {ac_heater_power_output_path}')
plt.clf()

heatmap = plt.imshow(Z, cmap='viridis', origin='lower', aspect='equal',
                     extent=[temp[0], temp[-1], hum[0], hum[-1]])

plt.colorbar(heatmap, label='AC/Heater Power (%)')
plt.xlabel('Temperature (°C)')
plt.ylabel('Humidity (%)')
plt.title('Fuzzy Control System - 2D Heatmap')

heatmap_output_path = f'outputs/ac_heater_power/heatmap_{max_file_num}.png'
plt.savefig(heatmap_output_path, dpi=300, bbox_inches='tight')
print(f'AC/Heater power heatmap saved to {heatmap_output_path}')
plt.close()