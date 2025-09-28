import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import matplotlib.pyplot as plt

NUM_POINTS = 10000

X_TEMP_MIN = -50
X_TEMP_MAX = 50

X_HUM_MIN = 0
X_HUM_MAX = 100

TEMP_UNIVERSE = np.linspace(X_TEMP_MIN, X_TEMP_MAX, NUM_POINTS)  # Temperature range from -50 to 50 degrees Celsius
HUM_UNIVERSE = np.linspace(X_HUM_MIN, X_HUM_MAX, NUM_POINTS)    # Humidity range from 0 to 100%

# Define the universe of discourse for temperature and humidity
temperature = ctrl.Antecedent(TEMP_UNIVERSE, 'temperature')  # -50 to 50 degrees Celsius
humidity = ctrl.Antecedent(HUM_UNIVERSE, 'humidity')      # 0 to 100%
#delta_temp = ctrl.Antecedent(np.linspace(-100, 100, num_points), 'delta_temp')  # -100 to 100 degrees Celsius change
#delta_humidity = ctrl.Antecedent(np.linspace(-100, 100, num_points), 'delta_humidity')  # -100 to 100% change

temperature['freezing'] = 1 - fuzz.trapmf(TEMP_UNIVERSE, [-20, 10, X_TEMP_MAX, X_TEMP_MAX])

# Access the membership values correctly
plt.plot(TEMP_UNIVERSE, temperature['freezing'].mf, label='Freezing')
plt.xlabel('Temperature (°C)')
plt.ylabel('Membership')
plt.title('Temperature Membership Functions')
plt.legend()
plt.grid(True)
plt.savefig('basic/images/universes_freezing.png', dpi=300)
