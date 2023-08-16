import pandas as pd
import numpy as np
import warnings
from pathlib import Path

from data_processing import processing

processing() #make sure to run processing before making a new computation
fuel2 = fuel = pd.read_csv('fuel_mpl.csv') #could directly process fuel_mpl here

def journey_cost(distance, ppl, data=fuel2, roof_racks=None, fuel_type=None, driving_style=None):
    df = data.copy()
    
    for var, name in ((roof_racks, 'roof_racks'),
                      (fuel_type, 'fuel_type'),
                      (driving_style, 'driving_style')):
        if var != None:
            if name == 'driving_style':
                df['driving_style'] = df['driving_style'].shift(-1)
                
            df = df[df[name] == var]
            
    average_miles_per_liter = df['miles_per_liter'].mean()
    
    liters = distance / average_miles_per_liter
    price = liters * ppl / 100
    
    print(f"AVG MPL: {average_miles_per_liter:.4f} mpl")
    print(f"DIST: {distance} mi")
    print(f"LITERS: {liters:.1f} l")
    print(f"\033[1mPrice: £{price:.2f}\033[0m")
    
    return price

def journey_calculator():
    distance = float(input("Enter distance (mi): "))
    ppl = float(input("Enter price per liter: "))
    
    apply_filters = input("Apply filters? (y/n): ").lower()
    
    variables = {
        'roof_racks': None,
        'fuel_type': None,
        'driving_style': None
    }
    
    if apply_filters == 'y':

        for var_name, name, options in (("roof_racks", "Roof Racks", ["On", "Off"]),
                                       ("fuel_type", "Fuel Type", ["E10", "E5"]),
                                       ("driving_style", "Driving Style", ["Normal", "Motorway"])):
            option_str = "/".join(options + ["None"])
            temp = input(f"Enter {name} filter ({option_str}): ")

            for option in options:
                if temp.lower().strip() == option.lower():
                    variables[var_name] = option

            print(f"{name} Filter: {variables[var_name]}")
        
        print(variables["roof_racks"], "RR")
        print(variables["driving_style"], "DS")
                
        journey_cost(distance, ppl, 
                     roof_racks=variables["roof_racks"], 
                     fuel_type=variables["fuel_type"],
                     driving_style=variables["driving_style"])
    else:
        journey_cost(distance, ppl)

if __name__ == "__main__":
    journey_calculator()