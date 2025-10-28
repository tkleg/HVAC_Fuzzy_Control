import os
import matplotlib.pyplot as plt
from membership_functions import variables, units
from universes import universes

#Prompt user to enter a directory to save the plots
output_dir = input("Enter the directory to save the plot. Note that the path starts at the root of the devcontainer: ")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    os.makedirs(os.path.join(output_dir, 'membership_functions'))
else:
    print(f"Directory {output_dir} already exists. You must enter a path which does not already exist.")
    exit(1)
    
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
    filename = f'{output_dir}/membership_functions/{var_name}_membership.png'
    if os.path.exists(filename):
        os.remove(filename)
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.clf()