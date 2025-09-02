from mins_maxs_universes import *
import random

test_values = [
    (15, 20),   # cold & dry
    (25, 50),   # warm & normal
    (35, 80),   # hot & humid
    (10, 90),   # cold & humid
    (30, 30),   # hot & dry
]

random_test_values = [
    (random.uniform(temp_min, temp_max), 
    random.uniform(humidity_min, humidity_max))
    for _ in range(5)
]

test_values.extend(random_test_values)
