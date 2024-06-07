import os
import sys
import pandas as pd
import openpyxl
# read excel file

def levenshtein_distance(s1, s2):
    # Initialize matrix of zeros
    rows = len(s1) + 1
    cols = len(s2) + 1
    dist = [[0 for _ in range(cols)] for _ in range(rows)]

    # Populate matrix of zeros with the indices of each character of both strings
    for i in range(1, rows):
        dist[i][0] = i
    for j in range(1, cols):
        dist[0][j] = j

    # Iterate over the matrix to compute the cost of deletions, insertions, and substitutions
    for i in range(1, rows):
        for j in range(1, cols):
            if s1[i-1] == s2[j-1]:
                cost = 0
            else:
                cost = 1

            dist[i][j] = min(dist[i-1][j] + 1,      # deletion
                             dist[i][j-1] + 1,      # insertion
                             dist[i-1][j-1] + cost) # substitution

    # The distance is the number in the bottom right corner of the matrix
    return dist[-1][-1]
        

def annotation_helper_name_sub_string(operation_parameters, operation_parameters_description, response_property, response_property_description):
    # if operation_parameters is in response_property_description, or vice versa, return "Yes"
    print(f"Checking '{operation_parameters}' in '{response_property_description}' or '{response_property}' in '{operation_parameters_description}'")
    if operation_parameters in response_property or response_property in operation_parameters:
        return "Yes"
    return "No"

def annotation_helper_name_in_description(operation_parameters, operation_parameters_description, response_property, response_property_description):
    # if operation_parameters is in response_property_description, or vice versa, return "Yes"
    print(f"Checking '{operation_parameters}' in '{response_property_description}' or '{response_property}' in '{operation_parameters_description}'")
    if operation_parameters in response_property_description or response_property in operation_parameters_description:
        return "Yes"
    return "No"

def excel_helper(file_path):
    # read excel file and make sure that all columns are string
    df = pd.read_excel(file_path, engine="openpyxl", dtype=str)
    for column in df.columns:
        # if nan is in the column, replace it with an empty string
        df[column] = df[column].fillna("")
    # apply annotation_helper function to the "Description" column
    # df["substring"] = df.apply(lambda x: annotation_helper_sub_string(x["corresponding attribute"], x["attribute"], x["corresponding attribute description"]), axis=1)
    df["name_in_name"] = df.apply(lambda x: annotation_helper_name_sub_string(x["corresponding attribute"], x["corresponding attribute description"],x["attribute"], x["description"]), axis=1)
    df["name_in_description"] = df.apply(lambda x: annotation_helper_name_in_description(x["corresponding attribute"], x["corresponding attribute description"],x["attribute"], x["description"]), axis=1)
    df["name_distance"] = df.apply(lambda x: levenshtein_distance(x["corresponding attribute"], x["attribute"]), axis=1)
    return df

def read_excel(file_path):
    # read excel file
    df = pd.read_excel(file_path, engine="openpyxl")
    return df

# write excel file
def write_excel(df, file_path):
    # if file does not exist, create a new file
    if not os.path.exists(file_path):
        df.to_excel(file_path, index=False)

    # else, read the existing file
    else:
        original_df = pd.read_excel(file_path, engine="openpyxl")
        # keep the original "Hieu's annotation" column
        df["Hieu's annotation"] = original_df["Hieu's annotation"]

        df.to_excel(file_path, index=False)

if __name__ == "__main__":
    # read file name from command line
    # args = sys.argv
    # file_path = args[1]

    rest_services = ["GitLab Branch", "GitLab Project", "GitLab Repository", "GitLab Commit", "GitLab Groups", "GitLab Issues", "StripeClone"]
    for rest_service in rest_services:
        file_path = f"ground_truth/{rest_service} API/ground_truth_request_response_constraints.xlsx"
        # read excel file
        df = excel_helper(file_path)
        # write excel file
        write_excel(df, file_path)


# Path: response-verification/annotation_helper/annotation_helper.py

