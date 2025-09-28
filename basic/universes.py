import numpy as np
from mins_maxs import TEMP_MIN, TEMP_MAX, HUM_MIN, HUM_MAX

NUM_POINTS = 10000

TEMP_UNIVERSE = np.linspace(TEMP_MIN, TEMP_MAX, NUM_POINTS)  # Temperature range from -50 to 50 degrees Celsius
HUM_UNIVERSE = np.linspace(HUM_MIN, HUM_MAX, NUM_POINTS)    # Humidity range from 0 to 100%