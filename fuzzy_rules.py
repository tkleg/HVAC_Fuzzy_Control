import skfuzzy.control as ctrl
from membership_functions import variables

temp = variables['temperature']
hum = variables['humidity']
delta_temp = variables['delta_temperature']
delta_hum = variables['delta_humidity']

humidifier_dehumidifier = variables['humidifier_dehumidifier_power']
ac_heater = variables['ac_heater_power']

rules = []

ac_temp_rules = [
    ctrl.Rule(temp['freezing'], ac_heater['heating']),
    ctrl.Rule(temp['cold'], ac_heater['heating']),
    ctrl.Rule(temp['warm'], ac_heater['off']),
    ctrl.Rule(temp['hot'], ac_heater['cooling'])
]
rules.extend(ac_temp_rules)

ac_delta_temp_rules = [
    ctrl.Rule(delta_temp['decreasing'], ac_heater['heating']),
    ctrl.Rule(delta_temp['stable'], ac_heater['off']),
    ctrl.Rule(delta_temp['increasing'], ac_heater['cooling'])
]
rules.extend(ac_delta_temp_rules)


humidifier_humidity_rules = [
    ctrl.Rule(hum['dry'], humidifier_dehumidifier['humidifying']),
    ctrl.Rule(hum['comfortable'], humidifier_dehumidifier['off']),
    ctrl.Rule(hum['humid'], humidifier_dehumidifier['dehumidifying'])
]
rules.extend(humidifier_humidity_rules)

humidifier_delta_humidity_rules = [
    ctrl.Rule(delta_hum['decreasing'], humidifier_dehumidifier['humidifying']),
    ctrl.Rule(delta_hum['stable'], humidifier_dehumidifier['off']),
    ctrl.Rule(delta_hum['increasing'], humidifier_dehumidifier['dehumidifying'])
]
#rules.extend(humidifier_delta_humidity_rules)