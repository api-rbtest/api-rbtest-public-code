# Repository for "Mining and Testing Constraints of Response Body for API Testing"

This repository contains the resources and code related to the paper "Mining and Testing Constraints of Response Body for API Testing."

## Folder Structure

- [`RBCTest_dataset`](RBCTest_dataset): Contains the dataset of 8 services, including an OpenAPI specification for each service.
- [`agora_dataset`](AGORA_dataset): Dataset used in experiment with AGORA.
- [`approaches`](approaches): Includes our ground-truth constraints, detected constraints from RBCTest, RBCTest--.
- [`src`](src): Source code.
- Benchmark for API Constraints Mining in [`approaches/ground_truth`](approaches/ground_truth).

## Usage

### Environment Setup

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file under the [`src`](src) directory with the following content:
   ```
   OPENAI_API_KEY=<your_openai_api_key>
   ```
   Please ensure that your key supports the required models.

### Constraint Mining

1. **Request-Response Constraints:**
   - For our approach:
     ```bash
     python src/request_response_constraint_mining.py
     ```
   - For the ablation approach:
     ```bash
     python src/response_property_constraint_mining_ablation.py
     ```

2. **Response Property Constraints:**
   - For our approach:
     ```bash
     python src/request_response_constraint_mining.py
     ```
   - For the ablation approach:
     ```bash
     python src/request_response_constraint_mining_ablation.py
     ```

### Constraint Test Generation

- Run the script:
  ```bash
  python src/constraints_test_generation.py
  ```

## Evaluation

- To re-evaluate constraints mining, run:
  ```bash
  python src/evaluate_constraints_mining.py
  ```

- To re-evaluate test generation, run:
  ```bash
  python src/evaluate_test_gen.py
  ```

## Experimental Results

### RQ1.1 Results on AGORA Dataset
- All AGORA detected invariants: [`AGORA-eval/agora_all.xlsx`](AGORA-eval/agora_all.xlsx)
- All RBCTest detected constraints: see sub-folders in [`approaches/rbctest_agora_data`](approaches/rbctest_agora_data)
- Overlapping analysis: [`AGORA-eval/overlapping_analysis_all.xlsx`](AGORA-eval/overlapping_analysis_all.xlsx)

**Annotation:**
- `o`: RBCTest constraint is better
- `a`: AGORA's invariant is better
- `=`: Equivalent

### RQ1.2, RQ2, RQ3 Results on RBCTest Dataset
- Results Analysis: [`approach_evaluation_test_gen.csv`](approaches/rbctest_agora_data/approach_evaluation_test_gen.csv)
- Details: see [`approaches/rbctest_our_data`](approaches/rbctest_our_data) (each subfolder is a SUT)

### RQ4 Usefulness
- Results Analysis: [`test_outcomes_analyze.csv`](approaches/rbctest_our_data/test_outcomes_analyze.csv)
- Detected mismatches: [`all_mismatches.xlsx`](approaches/rbctest_our_data/all_mismatches.xlsx) 

### RQ5 Ablation
- Ablation study: see [`approaches/ablation`](approaches/ablation)

