import pandas as pd

fuel2 = fuel = pd.read_csv('fuel_mpl.csv') #could directly process fuel_mpl here

def journey_cost(distance, ppl, data=fuel2, roof_racks=None, fuel_type=None, driving_style=None):
    df = data.copy()
    
    for var, name in ((roof_racks, 'roof_racks'),
                      (fuel_type, 'fuel_type'),
                      (driving_style, 'driving_style')):
        if var is not None:
            df = df[df[name] == var]
            
    average_miles_per_liter = df['miles_per_liter'].mean()
    
    liters = distance / average_miles_per_liter
    price = liters * ppl / 100
    
    print(f"AVG MPL: {average_miles_per_liter:.4f} mpl")
    print(f"DIST: {distance} mi")
    print(f"LITERS: {liters:.1f} l")
    print(f"\033[1mPrice: £{price:.2f}\033[0m")

def main():
    distance = float(input("Enter distance (mi): "))
    ppl = float(input("Enter price per liter: "))
    
    apply_filters = input("Apply filters? (y/n): ").lower()
    if apply_filters == 'y':
        roof_racks, fuel_type, driving_style = None, None, None
        for var, name, options in ((roof_racks, "Roof Racks", ["On", "Off"]),
                                   (fuel_type, "Fuel Type", ["E10", "E5"]),
                                   (driving_style, "Driving Style", ["Normal", "Motorway"])):
            option_str = "/".join(options + ["None"])
            temp = input(f"Enter {name} filter ({option_str}): ")
            for option in options:
                if temp.lower().strip() == option.lower():
                    var = option
                
        journey_cost(distance, ppl, roof_racks=roof_racks, fuel_type=fuel_type, driving_style=driving_style)
    else:
        journey_cost(distance, ppl)

if __name__ == "__main__":
    main()