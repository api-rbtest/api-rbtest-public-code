import os

import pandas as pd

CONSTRAINT_TYPE = "Response-property"

def evaluate_response_property_constraint_mining(approach_folder, ground_truth_folder, api_folders, csv_file, export=False):
    if not os.path.exists(csv_file):
        with open(csv_file, "w") as f:
            f.write("API,Constraint_Type,TP,FP,FN,Precision,Recall,F1\n")

    for api_folder in api_folders:
        if api_folder == ".DS_Store":
            continue
        approach_file = f'{approach_folder}/{api_folder}/response_property_constraints.xlsx'
        ground_truth_file = f'{ground_truth_folder}/{api_folder}/response_property_constraints.xlsx'
        
        
        if not os.path.exists(approach_file) or not os.path.exists(ground_truth_file):
            continue
        ground_truth_df = pd.read_excel(ground_truth_file, engine='openpyxl')

        print(f"Processing {approach_file}, on {ground_truth_file}")
        approach_df = pd.read_excel(approach_file, engine='openpyxl')
        if approach_df.empty:
            continue
        approach_df["constraint_correctness"] = ""
        for row, data in approach_df.iterrows():
            description = data["description"]

            mask = (ground_truth_df["description"] == description)
            found_mapping = ground_truth_df[mask]
            if found_mapping.empty:
                approach_df.at[row, "constraint_correctness"] = "FP"
            else:
                approach_df.at[row, "constraint_correctness"] = "TP"

        if export:
            approach_df.to_excel(approach_file, index=False)

        approach_df = approach_df[['attribute', 'description', ]].drop_duplicates()
        ground_truth_df = ground_truth_df[['attribute', 'description', ]].drop_duplicates()

        ground_truth_df["concat"] = ground_truth_df["attribute"] + ground_truth_df["description"]
        approach_df["concat"] = approach_df["attribute"] + approach_df["description"]

        gt_values = set(ground_truth_df["concat"].values)
        approach_values = set(approach_df["concat"].values)
        tps = gt_values.intersection(approach_values)
        fps = approach_values - gt_values
        fns = gt_values - approach_values
        

        precision = len(tps) / (len(tps) + len(fps))
        recall = len(tps) / (len(tps) + len(fns))
        f1 = 2 * (precision * recall) / (precision + recall)

        with open(csv_file, "a") as f:
            f.write(f"{api_folder},{CONSTRAINT_TYPE},{len(tps)},{len(fps)},{len(fns)},{precision},{recall},{f1}\n")


            
            


    