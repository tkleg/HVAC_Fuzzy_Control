
muS = {}

def triangular(x, a, b, c):
    """Triangular membership function"""
    if x <= a or x >= c:
        return 0.0
    elif x == b:
        return 1.0
    elif a < x < b:
        return (x - a) / (b - a)
    else:  # b < x < c
        return (c - x) / (c - b)


# Temperature fuzzy sets
def cold(x): return triangular(x, 0, 0, 20)
def warm(x): return triangular(x, 10, 20, 30)
def hot(x):  return triangular(x, 20, 40, 40)

# Humidity fuzzy sets
def dry(x):    return triangular(x, 0, 0, 40)
def normal(x): return triangular(x, 30, 50, 70)
def humid(x):  return triangular(x, 60, 100, 100)

# Fan input fuzzy sets
def input_low(x):    return triangular(x, 0, 0, 50)
def input_medium(x): return triangular(x, 25, 50, 75)
def input_high(x):   return triangular(x, 50, 100, 100)


def fuzzify(input_temp, input_humidity ):
    muS['cold'] = cold(input_temp)
    muS['warm'] = warm(input_temp)
    muS['hot']  = hot(input_temp)

    muS['dry']    = dry(input_humidity)
    muS['normal'] = normal(input_humidity)
    muS['humid']  = humid(input_humidity)
