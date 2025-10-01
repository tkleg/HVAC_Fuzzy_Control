import skfuzzy.control as ctrl
from membership_functions import variables

temp = variables['temperature']
hum = variables['humidity']
ac_heater = variables['ac_heater_power']

rules = []

#Temperature only rules
temp_only_rules_scaled = [
    ctrl.Rule(temp['freezing'], ac_heater['heating_temp']),
    ctrl.Rule(temp['cold'], ac_heater['heating_temp']),
    ctrl.Rule(temp['warm'], ac_heater['off_temp']),
    ctrl.Rule(temp['hot'], ac_heater['cooling_temp'])
]
rules.extend(temp_only_rules_scaled)
temp_only_rules = [
    ctrl.Rule(temp['freezing'], ac_heater['heating']),
    ctrl.Rule(temp['cold'], ac_heater['heating']),
    ctrl.Rule(temp['warm'], ac_heater['off']),
    ctrl.Rule(temp['hot'], ac_heater['cooling'])
]
#rules.extend(temp_only_rules)


#Humidity only rules
humidity_only_rules = [
    ctrl.Rule(hum['dry'], ac_heater['heating']),
    ctrl.Rule(hum['comfortable'], ac_heater['off']),
    ctrl.Rule(hum['humid'], ac_heater['cooling'])
]
#rules.extend(humidity_only_rules)

#Combined temperature and humidity rules
temp_and_hum_rules = [
    ctrl.Rule(temp['freezing'] & hum['dry'], ac_heater['heating']),
    ctrl.Rule(temp['freezing'] & hum['comfortable'], ac_heater['heating']),
    ctrl.Rule(temp['freezing'] & hum['humid'], ac_heater['heating']),
    ctrl.Rule(temp['cold'] & hum['dry'], ac_heater['heating']),
    ctrl.Rule(temp['cold'] & hum['comfortable'], ac_heater['heating']),
    ctrl.Rule(temp['cold'] & hum['humid'], ac_heater['off']),
    ctrl.Rule(temp['warm'] & hum['dry'], ac_heater['off']),
    ctrl.Rule(temp['warm'] & hum['comfortable'], ac_heater['off']),
    ctrl.Rule(temp['warm'] & hum['humid'], ac_heater['cooling']),
    ctrl.Rule(temp['hot'] & hum['dry'], ac_heater['cooling']),
    ctrl.Rule(temp['hot'] & hum['comfortable'], ac_heater['cooling']),
    ctrl.Rule(temp['hot'] & hum['humid'], ac_heater['cooling'])
]
rules.extend(temp_and_hum_rules)