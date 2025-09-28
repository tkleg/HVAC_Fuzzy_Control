import skfuzzy as fuzz
import skfuzzy.control as ctrl
import matplotlib.pyplot as plt
from mins_maxs import TEMP_MAX, TEMP_MIN, HUM_MAX, HUM_MIN
from universes import TEMP_UNIVERSE, HUM_UNIVERSE

# Define the universe of discourse for temperature and humidity
temperature = ctrl.Antecedent(TEMP_UNIVERSE, 'temperature')  # -50 to 50 degrees Celsius
humidity = ctrl.Antecedent(HUM_UNIVERSE, 'humidity')      # 0 to 100%
#delta_temp = ctrl.Antecedent(np.linspace(-100, 100, num_points), 'delta_temp')  # -100 to 100 degrees Celsius change
#delta_humidity = ctrl.Antecedent(np.linspace(-100, 100, num_points), 'delta_humidity')  # -100 to 100% change

temperature['freezing'] = 1 - fuzz.trapmf(TEMP_UNIVERSE, [-20, 10, TEMP_MAX, TEMP_MAX])

# Access the membership values correctly
plt.plot(TEMP_UNIVERSE, temperature['freezing'].mf, label='Freezing')
plt.xlabel('Temperature (°C)')
plt.ylabel('Membership')
plt.title('Temperature Membership Functions')
plt.legend()
plt.grid(True)
plt.savefig('basic/images/universes_freezing.png', dpi=300)