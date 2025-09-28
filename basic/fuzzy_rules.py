import skfuzzy.control as ctrl
from membership_functions import variables

temp = variables['temperature']
hum = variables['humidity']
ac_heater = variables['ac_heater_power']

rules = [
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