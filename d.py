import skfuzzy.control as ctrl
import skfuzzy as fuzz
from fuzzy_rules import rules
from membership_functions import variables

# Create controller
controller = ctrl.ControlSystem(rules)
simulator = ctrl.ControlSystemSimulation(controller)

# Test the exact scenario from your output
test_temp = 34.657450
test_hum = 35.314443
test_delta_temp = -0.342550

print("=== DEBUGGING HUMIDITY CONTROL ===")
print(f"Testing: Temp={test_temp:.1f}°C, Humidity={test_hum:.1f}%, Delta_Temp={test_delta_temp:.3f}")

# Check what happens WITHOUT delta_humidity input
try:
    simulator.input['temperature'] = test_temp
    simulator.input['humidity'] = test_hum
    simulator.input['delta_temperature'] = test_delta_temp
    # NOT setting delta_humidity - this might be the issue
    
    simulator.compute()
    
    humidifier_power = simulator.output['humidifier_dehumidifier_power']
    print(f"WITHOUT delta_humidity input: {humidifier_power:.10f}")
except Exception as e:
    print(f"ERROR without delta_humidity: {e}")

# Check what happens WITH delta_humidity input = 0
try:
    simulator.input['temperature'] = test_temp
    simulator.input['humidity'] = test_hum  
    simulator.input['delta_temperature'] = test_delta_temp
    simulator.input['delta_humidity'] = 0.0  # Set to 0
    
    simulator.compute()
    
    humidifier_power = simulator.output['humidifier_dehumidifier_power']
    print(f"WITH delta_humidity=0: {humidifier_power:.10f}")
except Exception as e:
    print(f"ERROR with delta_humidity=0: {e}")

# Check membership degrees for humidity
hum_var = variables['humidity']
dry_membership = fuzz.interp_membership(hum_var.universe, hum_var['dry'].mf, test_hum)
comfortable_membership = fuzz.interp_membership(hum_var.universe, hum_var['comfortable'].mf, test_hum)
humid_membership = fuzz.interp_membership(hum_var.universe, hum_var['humid'].mf, test_hum)

print(f"\nHumidity memberships at {test_hum:.1f}%:")
print(f"  dry: {dry_membership:.3f}")
print(f"  comfortable: {comfortable_membership:.3f}")  
print(f"  humid: {humid_membership:.3f}")