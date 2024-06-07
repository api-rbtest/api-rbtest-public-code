
import os
import re

import pandas as pd

def extract_numbers(input_string):
    if isinstance(input_string, float) or isinstance(input_string, int):
        input_string = str(input_string)
        if input_string.lower() == "nan":
            return []
    # Use regular expression to find all numbers in the string
    numbers = re.findall(r'\d+', input_string)
    # Convert the extracted numbers to integers
    numbers = [int(num) for num in numbers]
    return numbers


def merge_annotations(current_annotation, found_annotation_arr):
    if isinstance(current_annotation, float):
        current_annotation = ""
    current_annotation = str(current_annotation)
    if " " in current_annotation:
        current_indices = current_annotation.split(" ")
    elif "," in current_annotation:
        current_indices = current_annotation.split(",")
    else:
        current_indices = [current_annotation]

    current_indices = [str(int(index)) for index in current_indices if index != ""]

    # merge the current indices with the previous annotation
    result = list(set(current_indices + found_annotation_arr))
    result.sort()
    return_dats =  " ".join(result)
    return return_dats
    

def find_all_files_in_directory(directory, pattern, exception_file):
    # Find all files in the directory that match the pattern
    matched_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if pattern in file and not file.startswith("~$") and file != exception_file:
                matched_files.append(os.path.join(root, file))
    return matched_files

def parse_potential_mappings_data(potential_mappings_data):
    # split by the first "\n" character and remove empty strings
    potential_mappings_data = potential_mappings_data.split("\n")
    potential_mappings_lines = list(filter(None, potential_mappings_data))
    result = {}
    for line in potential_mappings_lines:
        # get the first . position
        first_dot_position = line.find(".")
        index = line[:first_dot_position]
        data = line[first_dot_position+1:]
        # for data, split by "|||"
        corresponding_attribute, corresponding_attribute_description = data.split("|||")
        result[index] = (corresponding_attribute.strip(), corresponding_attribute_description.strip())
    return result

def find_value_in_dict(value, dictionary):
    keys = []
    for key, val in dictionary.items():
        if value == val:
            keys.append(key)
    return keys

def get_knowledge_base(annotation_dir, exception_file):
    annotation_files = find_all_files_in_directory(annotation_dir, "annotation.xlsx", exception_file)
    total_df = pd.DataFrame()
    for annotation_file in annotation_files:
        api_folder = os.path.basename(os.path.dirname(annotation_file))
        df = pd.read_excel(annotation_file, engine='openpyxl')
        df["API"] = api_folder
        total_df = pd.concat([total_df, df])
        # fill NaN values with empty strings
        df = df.fillna("")
    return total_df

def find_in_knowedge_base(total_df, response_property, response_resource, potential_mappings_data):
    print(f"Find in knowledge base for {response_property}")
    potential_mappings_dict = parse_potential_mappings_data(potential_mappings_data)

    mask = (total_df["attribute"] == response_property) & (total_df["response resource"] == response_resource)
    response_property_df = total_df[mask]

    if response_property_df.empty:
        return None
    
    match_indexes = []
    for index, row in response_property_df.iterrows():
        data = row["data"]
        data_dict = parse_potential_mappings_data(data)
        input_data = row["input"]
        if input_data == "":
            continue
        else:
            if isinstance(input_data, float):
                input_data = str(input_data)
                if input_data.lower() == "nan":
                    continue
            input_data = str(input_data)

            chosen_indexes = input_data.split(" ")
            for chosen_index in chosen_indexes:
                # format chosen_index as a number which can be float or int
                if chosen_index == "":
                    continue
                chosen_index = str(int(float(chosen_index)))
                if chosen_index in data_dict:
                    chosen_corresponding_attribute, chosen_corresponding_attribute_description = data_dict[chosen_index]
                    # find the (corresponding_attribute, corresponding_attribute_description) in the potential_mappings_dict
                    matched_indices = find_value_in_dict((chosen_corresponding_attribute, chosen_corresponding_attribute_description), potential_mappings_dict)
                    for matched_index in matched_indices:
                        match_indexes.append(matched_index)
    match_indexes = list(set(match_indexes))
    match_indexes.sort()
    return match_indexes

        
    

    


