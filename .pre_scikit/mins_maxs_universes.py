import numpy as np

resolution = 10000

temp_max = 40
temp_min = 0
temp_universe = np.linspace(temp_min, temp_max, resolution)

humidity_max = 100
humidity_min = 0
humidity_universe = np.linspace(humidity_min, humidity_max, resolution)

temp_control_min = -100
temp_control_max = 100
temp_control_universe = np.linspace(temp_control_min, temp_control_max, resolution)

humidity_control_min = -100
humidity_control_max = 100
humidity_control_universe = np.linspace(humidity_control_min, humidity_control_max, resolution)

fan_control_min = 0
fan_control_max = 100
fan_control_universe = np.linspace(fan_control_min, fan_control_max, resolution)