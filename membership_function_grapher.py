import os
import matplotlib.pyplot as plt
from membership_functions import variables, units
from universes import universes

# Ensure the output directory exists
os.makedirs('membership_functions', exist_ok=True)

for var_name, fuzzySets in variables.items():

    for fuzzySetName in fuzzySets:
        plt.plot(universes[var_name], fuzzySets[fuzzySetName].mf, label=fuzzySetName.title())

    var_title = var_name.replace('_', ' ').title()
    if var_title.startswith('Ac'):
        var_title = var_title.replace('Ac ', 'AC/')
    
    print(f"Saving plot for {var_title} membership functions...")
    plt.title(var_title + ' Membership Functions', fontweight='bold')
    plt.xlabel(var_title + ' (' + units[var_name] + ')')
    plt.ylabel('Membership')
    plt.grid(True)
    plt.legend(title='Fuzzy Sets')
    filename = f'membership_functions/{var_name}_membership.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.clf()