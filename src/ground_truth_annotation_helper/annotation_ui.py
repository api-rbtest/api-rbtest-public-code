from copy import deepcopy
import os
from tkinter import scrolledtext
import pandas as pd
import tkinter as tk
from tkinter import messagebox
from request_annotation_helper import levenshtein_distance
from utils import find_in_knowedge_base, get_knowledge_base, merge_annotations

annotation_folder = "ground_truth"

# Read Excel file into DataFrame
# service = "StripeClone"
service = "GitLab Repository"
file = f'{annotation_folder}/{service} API/ground_truth_request_response_constraints.xlsx'
directory = os.path.dirname(file)
annotation_file = os.path.join(directory, 'annotation.xlsx')

knowledge_base = get_knowledge_base(annotation_folder, annotation_file)


if os.path.exists(annotation_file):
    df = pd.read_excel(annotation_file, engine='openpyxl')
    # fill NaN values with empty strings
    df = df.fillna("")

    for row, data in df.iterrows():
        found_annotation = find_in_knowedge_base(knowledge_base, data["attribute"], data["response resource"], data["data"])
        if found_annotation:
            # check if the previous annotation is the same as the current annotation
            current_annotation = data["input"]
            if current_annotation:
                common_indices = merge_annotations(current_annotation, found_annotation)
                df.at[row, "input"] = common_indices
                

else:
    df = pd.read_excel(file, engine='openpyxl')
    # group by the "attribute" and "response resource" columns
    unique_values = df.groupby(["attribute", "response resource"]).size().reset_index()

    display_df = unique_values.copy()
    display_df["input"] = ""
    display_df["data"] = ""
    for row, data in unique_values.iterrows():
        # find the rows that have the same "attribute" and "response resource" values in the original dataframe
        mask = (df["attribute"] == data["attribute"]) & (df["response resource"] == data["response resource"])
        display_data = ""
        count = 1
        potential_mappings = deepcopy(df[mask])
        potential_mappings["levenshtein_distance"] = potential_mappings.apply(lambda x: levenshtein_distance(x["corresponding attribute"], x["attribute"]), axis=1)
        potential_mappings = potential_mappings.sort_values(by="levenshtein_distance")
        for r1, d1 in potential_mappings.iterrows():
            # "attribute inferred from operation"	"corresponding attribute"	"corresponding attribute description"
            display_data += f"\n{count}. {d1['corresponding attribute']} ||| {d1['corresponding attribute description']}\n"
            count += 1
        
        display_df.at[row, "data"] = display_data

        found_annotation = find_in_knowedge_base(knowledge_base, data["attribute"], data["response resource"], display_data)
        if found_annotation:
            display_df.at[row, "input"] = " ".join(found_annotation)

    df = display_df





# Add 'input' column if it does not exist
if 'input' not in df.columns:
    df['input'] = ''

# Initialize row index
current_index = 0

# Create the main application window
root = tk.Tk()
root.title("Excel Data Viewer")
max_width = root.winfo_screenwidth()
max_height = root.winfo_screenheight()
root.geometry(f"{max_width}x{max_height}")
# root.geometry("1000x400")  # Set fixed window size



# Define UI elements
label_frame = tk.Frame(root)
label_frame.pack(pady=20)

# add a label on top of the frame, center it, to show the index of the current row. red color, bold, font size 30
index_label = tk.Label(label_frame, text=f"Row {current_index + 1} of {len(df)}", font=('Arial', 30, 'bold'), fg='red')
index_label.pack()

left_frame = tk.Frame(label_frame)
left_frame.pack(side=tk.LEFT, padx=10)
# create a line separator
separator = tk.Frame(label_frame, height=2, width=2, bd=1, relief=tk.SUNKEN)
separator.pack(side=tk.LEFT, fill=tk.Y, padx=10)

right_frame = tk.Frame(label_frame)
right_frame.pack(side=tk.RIGHT, padx=10)

left_label = tk.Label(left_frame, text="Response Body Property", font=('Arial', 20, 'bold'), fg='blue')
left_label.pack()

# input_label = tk.Label(left_frame, text="", wraplength=200)
# input_label.pack()
# set alignment to left, if over 200 characters, wrap to the next line
right_label = tk.Label(right_frame, text="Potential Mapping", font=('Arial', 20, 'bold'), anchor='w', justify='left', wraplength=800)
right_label.pack()

scrollable_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, width=100, height=20, font=('Arial', 20, 'bold'))
scrollable_text.pack(fill=tk.BOTH, expand=True)



entry_frame = tk.Frame(root)
entry_frame.pack(pady=10)

input_text = tk.StringVar()
# font size 20, width 50
entry = tk.Entry(entry_frame, textvariable=input_text, font=('Arial', 20), width=50)
entry.pack()
entry.bind("<Return>", lambda event: navigate(1))

button_frame = tk.Frame(root)
button_frame.pack(pady=20)

prev_button = tk.Button(button_frame, text="Previous", command=lambda: navigate(-1))
prev_button.pack(side=tk.LEFT, padx=5)

next_button = tk.Button(button_frame, text="Next", command=lambda: navigate(1))
next_button.pack(side=tk.RIGHT, padx=5)

save_button = tk.Button(root, text="Save", command=lambda: save_input())
save_button.pack(pady=10)

def update_ui():
    global current_index
    row_data = df.iloc[current_index].drop('input').to_dict()
    # left: Attribute and Response Resource, right: data
    left_text = f"{row_data['attribute']}\n - {row_data['response resource']}"
    right_text = row_data['data']

    left_label.config(text=left_text)

    
    scrollable_text.delete('1.0', tk.END)
    scrollable_text.insert(tk.INSERT, right_text)

    # right_label.config(text=right_text)
    # input_label.config(text=row_data['input'])
    input_text.set(df.at[current_index, 'input'])
    index_label.config(text=f"Row {current_index + 1} of {len(df)}")

def navigate(direction):
    global current_index
    save_input()
    new_index = current_index + direction
    if 0 <= new_index < len(df):
        current_index = new_index
        update_ui()
    else:
        messagebox.showwarning("Navigation Error", "No more rows in that direction.")
    df.to_excel(annotation_file, index=False)

def save_input():
    global current_index
    df.at[current_index, 'input'] = input_text.get()

update_ui()
root.mainloop()
df.to_excel(annotation_file, index=False)





