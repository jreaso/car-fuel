import pandas as pd
import numpy as np

import warnings
from pathlib import Path

def processing():
    fuel = pd.read_csv('fuel.csv')

    fuel.columns = ['_'.join(col.lower().split()) for col in fuel.columns]
    fuel["date"] = pd.to_datetime(fuel["date"], format="%d/%m/%Y")
    fuel["mileage"] = pd.to_numeric(fuel["mileage"].str.replace(",", ""))
    fuel.rename(columns={'mileage': 'total_mileage'}, inplace=True)
    fuel["filled_tank"] = fuel["filled_tank"].map({"Y": True, "N": False})
    fuel["roof_racks"] = fuel["roof_racks"].replace({"Y": "On", "N": "Off"})
    fuel["fuel_type"] = fuel["fuel_type"].replace("Supreme", "SUP")

    for col in ("fuel_type", "driving_style"):
        fuel[col] = fuel[col].str.strip()

    fuel = fuel.sort_values('date')

    #fuel_processed
    fuel.to_csv('fuel_processed.csv', index=False)

    def process_fuel_data(fuel_df):
        df = fuel_df.copy()

        for index, row in fuel_df.iterrows():
            # pass any columns with a filled tank
            if row['filled_tank']:
                continue

            # drop final row and raise error
            if index == df.index[-1]:
                df.drop(index, inplace=True)
                warnings.warn("The final entry had filled_tank = False, so data was lost in processing")
                continue

            # update next column in data frame
            for col in ('liters', 'price'):
                df.at[index + 1, col] += row[col] 

            df.at[index + 1, 'ppl'] = (100*(df.at[index + 1, 'price'] / df.at[index + 1, 'liters'])).round(1)

            for col in ('fuel_type', 'driving_style', 'roof_racks'):
                if df.at[index + 1, col] != row[col]:
                    df.at[index + 1, col] = "Mixed"

            #drop column
            df.drop(index, inplace=True)

        #computes mileage and miles_per_liter
        df['mileage'] = df['total_mileage'].diff()
        df['miles_per_liter'] = df['mileage'] / df['liters']

        return(df.reset_index(drop=True).sort_values('date'))

    fuel2 = process_fuel_data(fuel)

    #fuel_mpl
    fuel2.to_csv('fuel_mpl.csv', index=False)
    
if __name__ == "__main__":
    processing()