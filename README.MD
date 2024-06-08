# Repository for "Mining and Testing Constraints of Response Body for API Testing"

This repository contains the resources and code related to the paper "Mining and Testing Constraints of Response Body for API Testing."

## Folder Structure

- `api_spec_dataset`: Contains the dataset of 8 services, including an OpenAPI specification for each service.

- `approaches`: Includes our ground-truth constraints, detected constraints from our approach, detected constraints from the baseline approach, and generated test cases from our method. 

- `src`: Contains the source code.

- Benchmark for API Constraints Mining in `approaches/ground_truth`

## Usage

## Environment Setup

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file under the `src` directory with the following content:
   ```
   OPENAI_API_KEY=<your_openai_api_key>
   ```

### Constraint Mining

1. **Request-Response Constraints:**
   - For our approach: 
     ```bash
     python src/request_response_constraint_mining.py
     ```
   - For baseline, run: 
     ```bash
     python src/response_property_constraint_mining_baseline.py
     ```

2. **Response Property Constraints:**
   - For our approach: 
     ```bash
     python src/request_response_constraint_mining.py
     ```
   - For baseline, run: 
     ```bash
     python src/request_response_constraint_mining_baseline.py
     ```

### Constraint Test Generation

- Run the script: 
  ```bash
  python src/constraints_test_generation.py
  ```

## Evaluation

- To evaluate test generation, run: 
  ```bash
  python src/evaluate_test_gen.py
  ```
- To evaluate constraints mining, run: 
  ```bash
  python src/evaluate_constraints_mining.py
  ```
