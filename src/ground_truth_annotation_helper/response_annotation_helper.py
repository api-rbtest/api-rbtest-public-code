import os
import sys
import pandas as pd
import openpyxl
# read excel file

def annotation_helper(description):
    # if the following keywords are in the description, return "Yes"
    keywords = ["ISO", "Unix"]
    for keyword in keywords:
        if keyword in description:
            return "Yes"
    return "No"

def excel_helper(file_path):
    # read excel file
    df = pd.read_excel(file_path, engine="openpyxl")
    # apply annotation_helper function to the "Description" column
    df["Helper's annotation"] = df["Description"].apply(annotation_helper)
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

    file_path = "ground_truth/StripeClone API/ground_truth_response_body_constraints.xlsx"

    # read excel file
    df = excel_helper(file_path)
    # write excel file
    write_excel(df, file_path)


# Path: response-verification/annotation_helper/annotation_helper.py

