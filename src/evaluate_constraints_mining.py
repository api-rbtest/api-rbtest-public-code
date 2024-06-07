import os
from eval.request_approach_evaluate import evaluate_request_response_constraint_mining
from eval.response_approach_evaluate import evaluate_response_property_constraint_mining


def main():
    approach_folder = "approaches/baseline"
    ground_truth_folder = "approaches/ground_truth"
    csv_file = f"{approach_folder}/approach_evaluation.csv"

    if os.path.exists(csv_file):
        os.remove(csv_file)

    api_folders = os.listdir(ground_truth_folder)
    api_folders = [f for f in api_folders if not f.startswith(".") and os.path.isdir(os.path.join(ground_truth_folder, f))]
    api_folders.sort()

    evaluate_request_response_constraint_mining(approach_folder, ground_truth_folder, api_folders, csv_file)
    evaluate_response_property_constraint_mining(approach_folder, ground_truth_folder, api_folders, csv_file)

if __name__ == "__main__":
    main()
    