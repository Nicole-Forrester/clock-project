#!/usr/bin/env python3

import pandas as pd
import sys
import os

# ---- R Imports and Wrapper Function ----
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
from rpy2.rinterface_lib import openrlib

# Activate R <-> pandas conversion
pandas2ri.activate()

# Import R packages
base = importr("base")
dnamethyage = importr("dnaMethyAge")


def run_dnaMethyAge(csv_path, selected_clocks):
    # Load CSV into DataFrame
    betas_df = pd.read_csv(csv_path, index_col=0) # Reads file into pd df with first column used as the row names

    # Convert pandas DataFrame to R data.frame
    with openrlib.rlock:  # Ensures thread-safe access to the R interpreter
        with localconverter(pandas2ri.converter):
            betas_r = pandas2ri.py2rpy(betas_df)

        # Get available clocks from the R package
        avail_clocks = dnamethyage.availableClock() # Call directly as a function

        # Verify clocks are available
        for clock_name in selected_clocks:
            if clock_name not in avail_clocks:
                raise ValueError(f"{clock_name} Clock is not available.")

        # Initialize a dictionary to store results for all selected clocks
        all_results = {}

        # Loop through each selected clock and run methyAge
        for clock_name in selected_clocks:
            # Run the DNA methylation age calculation for each clock
            dnam_age_r = dnamethyage.methyAge(betas_r, clock=clock_name)

            # Convert R data.frame to pandas DataFrame
            with localconverter(pandas2ri.converter):
                dnam_age_df = pandas2ri.rpy2py(dnam_age_r)

            # Extract sample-age pairs and add them to the results list
            for index, row in dnam_age_df.iterrows():
                sample = row.iloc[0]  # Sample ID
                age = row.iloc[1]     # Predicted age
                if sample not in all_results:
                    all_results[sample] = {}
                all_results[sample][clock_name] = age

    # Sort samples for consistency
    sorted_samples = sorted(all_results.items())
    return sorted_samples


def main():
    # Get the job ID from the command line arguments to find temp folder
    job_id = sys.argv[1]
    
    # Define the paths to input and output files in the job folder
    job_folder = f"./data/temp/{job_id}"
    csv_path = os.path.join(job_folder, "data.csv")

    # Read the list of clocks selected by the user
    with open(os.path.join(job_folder, "clocks.txt"), "r") as f:
        selected_clocks = f.read().strip().split(",")

    # Run the clocks using the dnaMethyAge R package
    results = run_dnaMethyAge(csv_path, selected_clocks)

    # Format results as a DataFrame and save to results.csv
    df_rows = []
    for sample, clocks in results:
        row = {"Sample": sample}
        row.update(clocks)
        df_rows.append(row)

    df = pd.DataFrame(df_rows)
    df.to_csv(os.path.join(job_folder, "results.csv"), index=False)


if __name__ == "__main__":
    main()