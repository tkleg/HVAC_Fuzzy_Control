from fuzzySets import *
import mins_maxs_universes as mmu

# rules['low'] cold and dry
# rules['medium'] warm and normal
# rules['high'] hot or humid

rules = {}

for key in ['low', 'medium', 'high']:
    rules[key] = None  # Initialize all rules to None
    
def evaluate_rules():
    # Only evaluate rule if antecedent is triggered (nonzero)
    if min(muS['cold'], muS['dry']) > 0:
        rules['low'] = [min(muS['cold'], muS['dry'], input_low(x)) for x in mmu.fan_control_universe]
    if min(muS['warm'], muS['normal']) > 0:
        rules['medium'] = [min(muS['warm'], muS['normal'], input_medium(x)) for x in mmu.fan_control_universe]
    if max(muS['hot'], muS['humid']) > 0:
        rules['high'] = [max(muS['hot'], muS['humid'], input_high(x)) for x in mmu.fan_control_universe]