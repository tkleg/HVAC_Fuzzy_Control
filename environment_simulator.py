from json_parser import outdoor_temp_by_hour
from math import exp

# Square floor 20 meters, 3 meters tall
room_volume = 20 * 20 * 3 # in cubic meters

air_density = 1.225 # kg/m^3 at sea level

air_mass = room_volume * air_density

def calc_satured_vapor_pressure(temp_c):
    """Calculate the saturated vapor pressure of water at a given temperature in Celsius."""
    if temp_c >= 0:
        return 6.112 * exp((17.67 * temp_c) / (temp_c + 243.5))  # in hPa
    else:
        return 6.112 * exp((22.46 * temp_c) / (temp_c + 272.62))  # in hPa
    
def specific_heat_by_humidity(humidity):
    """Calculate the specific heat of air at a given humidity (%) and temperature (Celsius)."""

    cp_dry_air = 1005  # J/(kg·K)
    cp_water_vapor = 1860  # J/(kg·K)
    
    # Calculate specific heat
    specific_heat = cp_dry_air + (humidity / 100.0) * cp_water_vapor
    return specific_heat  # in J/(kg·K)

def celsius_to_kelvin(temp_c):
    return temp_c + 273.15

def kelvin_to_celsius(temp_k):
    return temp_k - 273.15

def calc_new_temp_and_hum(temp, humidity, ac_heater_control, hour):
    """Calculate the new temperature after applying power for a given time step."""

    ac_heater_max_power = 750  # in Watts

    specific_heat = specific_heat_by_humidity(humidity)  # J/(kg·K)
    
    ac_heater_power = ac_heater_control * ac_heater_max_power 

    sum_power = ac_heater_power

    thermal_conductivity = 0.002  # W/(m·K) Concrete
    wall_area = 20 * 3 * 4  # m^2 (4 walls, 3m tall, 20m wide)
    wall_thickness = 0.3 # m
    temp_difference = temp - outdoor_temp_by_hour(hour)  # in Celsius

    heat_loss = (thermal_conductivity * wall_area * temp_difference) / wall_thickness  # in Celsius

    sum_power -= heat_loss

    # 5 for 5 seconds
    temp_change = (sum_power * 5) / (air_mass * specific_heat)  # in Kelvin

    return {"temperature": temp + temp_change, "humidity": humidity}

#print(f"Step hours: {step_hours}")
#for i in range(24*14):
#    env_temp = temp_by_hour(i * step_hours)
#    env_hum = humidity_by_hour(i * step_hours)
#    print(f"Hour {i*step_hours:.2f}: Temp {env_temp:.2f} C, Humidity {env_hum:.2f}%")
