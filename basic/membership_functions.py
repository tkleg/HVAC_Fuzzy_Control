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

temperature['freezing'] = 1 - fuzz.trapmf(TEMP_UNIVERSE, [-20, 0, TEMP_MAX, TEMP_MAX])
temperature['cold'] = fuzz.trapmf(TEMP_UNIVERSE, [-20, 0, 5, 8])
temperature['warm'] = fuzz.trapmf(TEMP_UNIVERSE, [5, 10, 20, 30])
temperature['hot'] = fuzz.trapmf(TEMP_UNIVERSE, [20, 35, TEMP_MAX, TEMP_MAX])

humidity['dry'] = 1 - fuzz.trapmf(HUM_UNIVERSE, [0, 20, HUM_MAX, HUM_MAX])
humidity['comfortable'] = fuzz.trapmf(HUM_UNIVERSE, [20, 30, 50, 60])

variables = {'temperature': temperature, 'humidity': humidity}
units = {'temperature': '°C', 'humidity': '%', 'delta_temp': '°C', 'delta_humidity': '%'}

for var_name, fuzzySets in variables.items():

    for fuzzySetName in fuzzySets:
        plt.plot(TEMP_UNIVERSE, fuzzySets[fuzzySetName].mf, label=fuzzySetName.title())

    plt.title(var_name.title() + ' Membership Functions', fontweight='bold')
    plt.xlabel(var_name.title() + ' (' + units[var_name] + ')')
    plt.ylabel('Membership')
    plt.grid(True)
    plt.legend(title='Fuzzy Sets')
    filename = f'basic/images/{var_name}_membership.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.clf()