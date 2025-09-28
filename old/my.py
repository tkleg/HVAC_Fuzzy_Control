import mins_maxs_universes as mmu
import fuzzySets as fs
import testValues as tv
import rules as rl

for input_temp, input_humidity in tv.test_values:

    fs.fuzzify(input_temp, input_humidity)

    print(f"\nInputs: Temp = {input_temp}°C, Humidity = {input_humidity}%")
    print("Fuzzified values:")
    print("Temp: Cold =", fs.muS['cold'], "Warm =", fs.muS['warm'], "Hot =", fs.muS['hot'])
    print("Humidity: Dry =", fs.muS['dry'], "Normal =", fs.muS['normal'], "Humid =", fs.muS['humid'])


    rl.evaluate_rules()
    
    # Aggregation: only consider rules that are triggered
    aggregated_fan_control = [0.0] * len(mmu.fan_control_universe)
    for i in range(len(mmu.fan_control_universe)):
        values = []
        if rl.rules['low'] is not None:
            values.append(rl.rules['low'][i])
        if rl.rules['medium'] is not None:
            values.append(rl.rules['medium'][i])
        if rl.rules['high'] is not None:
            values.append(rl.rules['high'][i])
        if values:
            aggregated_fan_control[i] = max(values)

    # Defuzzification
    numerator = sum(mmu.fan_control_universe[i] * aggregated_fan_control[i] 
                    for i in range(len(mmu.fan_control_universe)))
    
    denominator = sum(aggregated_fan_control)
    if denominator == 0:
        crisp_output = 0
    else:
        crisp_output = numerator / denominator

    print("Defuzzified fan speed =", crisp_output)
