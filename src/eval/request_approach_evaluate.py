import os

import pandas as pd

CONSTRAINT_TYPE = "Request-Response"



def evaluate_request_response_constraint_mining(approach_folder, ground_truth_folder, api_folders, csv_file):
    if not os.path.exists(csv_file):
        with open(csv_file, "w") as f:
            f.write("API,Constraint_Type,TP,FP,FN,Precision,Recall,F1\n")

    for api_folder in api_folders:
        if api_folder == ".DS_Store":
            continue
        approach_file = f'{approach_folder}/{api_folder}/request_response_constraints.xlsx'
        ground_truth_file = f'{ground_truth_folder}/{api_folder}/request_response_constraints.xlsx'
        print(f"Processing {approach_file}, on {ground_truth_file}")
        
        ground_truth_df = pd.read_excel(ground_truth_file, engine='openpyxl')
        
        if not os.path.exists(approach_file) or not os.path.exists(ground_truth_file):
            continue

        print(f"Processing {approach_file}, on {ground_truth_file}")
        approach_df = pd.read_excel(approach_file, engine='openpyxl')

        if approach_df.empty:
            continue
        approach_df["constraint_correctness"] = ""
        for row, data in approach_df.iterrows():
            attribute = data["attribute"]
            response_resource = data["response resource"]
            parameter = data["corresponding attribute"]
            parameter_description = data["corresponding attribute description"]
            attribute_inferred_from_operation = data["attribute inferred from operation"]

            mask = (ground_truth_df["attribute"] == attribute) & (ground_truth_df["response resource"] == response_resource) & (ground_truth_df["corresponding attribute"] == parameter)
            found_mapping = ground_truth_df[mask]
            if found_mapping.empty:
                approach_df.at[row, "constraint_correctness"] = "FP"
            else:
                approach_df.at[row, "constraint_correctness"] = "TP"

        # approach_df.to_excel(approach_file.replace(".xlsx", "_eval.xlsx"), index=False)


        tmp_ground_truth_df = ground_truth_df.copy()
        tmp_ground_truth_df["concat"] = tmp_ground_truth_df["attribute"] + tmp_ground_truth_df["response resource"] + tmp_ground_truth_df["corresponding attribute"] + tmp_ground_truth_df["attribute inferred from operation"]

        tmp_approach_df = approach_df.copy()
        tmp_approach_df["concat"] = tmp_approach_df["attribute"] + tmp_approach_df["response resource"] + tmp_approach_df["corresponding attribute"] + tmp_approach_df["attribute inferred from operation"]

        gt_values = set(tmp_ground_truth_df["concat"].values)
        approach_values = set(tmp_approach_df["concat"].values)
        
        tps = gt_values.intersection(approach_values)
        fps = approach_values - gt_values
        fns = gt_values - approach_values

        if len(tps) == 0:
            precision = "-"
            recall = "-"
            f1 = "-"
        else:
            precision = len(tps) / (len(tps) + len(fps))
            recall = len(tps) / (len(tps) + len(fns))
            f1 = 2 * (precision * recall) / (precision + recall)

        with open(csv_file, "a") as f:
            f.write(f"{api_folder},{CONSTRAINT_TYPE},{len(tps)},{len(fps)},{len(fns)},{precision},{recall},{f1}\n")




    