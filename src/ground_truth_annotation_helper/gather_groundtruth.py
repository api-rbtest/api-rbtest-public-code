import os

import pandas as pd
from utils import get_knowledge_base, parse_potential_mappings_data, extract_numbers

annotation_folder = "ground_truth"

# Read Excel file into DataFrame
# service = "StripeClone"
service = "GitLab Repository"
file = f'{annotation_folder}/{service} API/ground_truth_request_response_constraints.xlsx'
directory = os.path.dirname(file)
annotation_file = os.path.join(directory, 'annotation.xlsx')

knowledge_base = get_knowledge_base(annotation_folder, "")
# sort by the "attribute" 
knowledge_base = knowledge_base.sort_values(by="attribute")

mappings_df = pd.DataFrame(columns=["attribute", "response resource", "parameter", "parameter description"])

for row, data in knowledge_base.iterrows():
    potential_mappings_data = data["data"]
    potential_mappings_dict = parse_potential_mappings_data(potential_mappings_data)

    input_data = data["input"]
    indices = extract_numbers(input_data)
    print(f"input_data: {input_data}, indices: {indices}")

    mappings = []
    for index in indices:
        index = str(index)
        if index in potential_mappings_dict:
            corresponding_attribute, corresponding_attribute_description = potential_mappings_dict[index]
            mappings_df = mappings_df._append({"attribute": data["attribute"], 
                                                "response resource": data["response resource"],
                                                "parameter": corresponding_attribute,
                                                "parameter description": corresponding_attribute_description,
                                                "API": data["API"]
                                                }, ignore_index=True)
            
api_folders = os.listdir(annotation_folder)
mappings_df.to_excel(f"mappings.xlsx", index=False)
for api_folder in api_folders:
    if api_folder == ".DS_Store":
        continue
    file = f'{annotation_folder}/{api_folder}/ground_truth_request_response_constraints.xlsx'
    
    if not os.path.exists(file):
        continue
    print(f"Processing {file}")

    ground_truth_df = pd.read_excel(file, engine='openpyxl')
    rows_to_remove = []
    for row, data in ground_truth_df.iterrows():
        attribute = data["attribute"]
        response_resource = data["response resource"]
        parameter = data["corresponding attribute"]
        parameter_description = data["corresponding attribute description"]
        # print(f"attribute: {attribute}, response_resource: {response_resource}, parameter: {parameter}, parameter_description: {parameter_description}")

        mask = (mappings_df["attribute"] == attribute) & (mappings_df["response resource"] == response_resource) & (mappings_df["parameter"] == parameter)
        found_mapping = mappings_df[mask]
        if found_mapping.empty:
            # remove current row
            rows_to_remove.append(row)
        # else:
        #     print(f"Found mapping: {found_mapping}")

    ground_truth_df.drop(rows_to_remove, inplace=True)
    # print(f"ground_truth_df: {len(ground_truth_df)}")
    # ground_truth_df["concat"] = ground_truth_df["attribute"] + ground_truth_df["description"] + ground_truth_df["corresponding attribute"] + \
    # ground_truth_df["corresponding attribute description"] + ground_truth_df["response resource"]
    # print(f"ground_truth_df: {len(ground_truth_df)}")

    # ground_truth_df.drop_duplicates(subset=["concat"], keep="first", inplace=True)
    # print(f"ground_truth_df: {len(ground_truth_df)}")

    ground_truth_df.to_excel(file.replace(".xlsx", "_updated.xlsx"), index=False)
            
            


    