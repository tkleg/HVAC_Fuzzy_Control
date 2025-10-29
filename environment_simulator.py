import random

def specific_heat_by_humidity(humidity):
    cp_dry_air = 1005  # J/(kg·K)
    cp_water_vapor = 1860  # J/(kg·K)
    
    # Calculate specific heat
    specific_heat = cp_dry_air + (humidity / 100.0) * cp_water_vapor
    return specific_heat  # in J/(kg·K)

def calc_new_temp_and_hum(temp, humidity, ac_heater_control, humidifier_control, hour, step_seconds, splines, ac_heater_max_power=1000, wall_heat_loss_factor=1):

    # Square floor 10 meters, 3 meters tall
    room_volume = 10 * 10 * 3 # in cubic meters

    air_density = 1.225 # kg/m^3 at sea level

    air_mass = room_volume * air_density

    # Fix: Make humidifier_max_change per hour, not per second
    humidifier_max_change = 5.0  # 5% per hour (reasonable rate)

    specific_heat = specific_heat_by_humidity(humidity)  # J/(kg·K)
    
    ac_heater_power = ac_heater_control/100 * ac_heater_max_power 

    sum_power = ac_heater_power

    thermal_conductivity = 0.002  # W/(m·K) Concrete
    wall_area = 10 * 3 * 4  # m^2 (4 walls, 3m tall, 10m wide)
    wall_thickness = 0.2 # m
    outdoor_temp = splines["temperature"](hour)  # in Celsius
    temp_difference = temp - outdoor_temp # in Celsius

    heat_loss = wall_heat_loss_factor * (thermal_conductivity * wall_area * temp_difference) / wall_thickness  # in Celsius

    sum_power -= heat_loss

    temp_change = (sum_power * step_seconds) / (air_mass * specific_heat)  # in Kelvin

    # Fix: Proper humidity calculation (convert step_seconds to hours)
    step_hours = step_seconds / 3600  # Convert seconds to hours
    humidity_change = (humidifier_control / 100) * humidifier_max_change * step_hours
    humidity_change += (humidity - splines["humidity"](hour)) * 0.01 * step_hours
    #print('humidity', humidity, 'humidifier_control', humidifier_control, 'humidity_change', humidity_change, 'step_seconds', step_seconds, 'humidifier_max_change', humidifier_max_change)
    env_outputs = {"temperature": temp + temp_change, "humidity": humidity + humidity_change, "outdoor_temperature": outdoor_temp}
    percent_noise = 0.05 / 100  # 0.05% noise
    for key in env_outputs:
       env_outputs[key] *= random.uniform(1 - percent_noise, 1 + percent_noise)  # Add some noise
    return {'outputs':env_outputs, 'ac_heater_control': ac_heater_control, 'humidifier_control': humidifier_control}
