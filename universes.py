import numpy as np
import mins_maxs as mm

NUM_POINTS = 10000

TEMP_UNIVERSE = np.linspace(mm.TEMP_MIN, mm.TEMP_MAX, NUM_POINTS)  # Temperature range from -50 to 50 degrees Celsius
HUM_UNIVERSE = np.linspace(mm.HUM_MIN, mm.HUM_MAX, NUM_POINTS)    # Humidity range from 0 to 100%

AC_HEATER_POWER_UNIVERSE = np.linspace(mm.AC_HEATER_POWER_MIN, mm.AC_HEATER_POWER_MAX, NUM_POINTS)  # AC/Heater power range from -100 to 100

universes = {
    'temperature': TEMP_UNIVERSE,
    'humidity': HUM_UNIVERSE,
    'ac_heater_power': AC_HEATER_POWER_UNIVERSE
}