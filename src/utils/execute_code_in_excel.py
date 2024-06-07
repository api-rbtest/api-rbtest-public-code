import json
import os
import pandas as pd
from src.constraints_test_generation import execute_request_parameter_constraint_verification_script

def fix_json(json_str):
    # if // is in the json_str and // not inside double quote, delete until the end of the line, or { or [
    lines = json_str.split("\n")
    new_lines = []
    for line in lines:
        if "//" in line:
            # if // is in the json_str and // not inside double quote, delete until the end of the line, or { or [
            new_line = ""
            inside_double_quote = False
            for i in range(len(line)):
                if line[i] == '"':
                    inside_double_quote = not inside_double_quote
                if not inside_double_quote:
                    if line[i:i+2] == "//":
                        break
                new_line += line[i]
            line = new_line
        new_lines.append(line)
    return "\n".join(new_lines)


def re_execute_code(code_excel):
    df = pd.read_excel(code_excel)
    df = df.fillna("")
    count = 0
    for index, row in df.iterrows():
        constraint_correctness = row["constraint_correctness"]
        if constraint_correctness != "TP":
            continue

        re_execute = row["re_execute"]
        if re_execute != "y":
            continue

        request_info = row["request information"]

        code = row["verification script"]
        api_response = row["API response"]

        request_info = row["request information"]

        executable_script, new_execution_status = execute_request_parameter_constraint_verification_script(code, api_response, request_info)


        df.at[index, "status"] = new_execution_status
        df.at[index, "executable script"] = executable_script

        code = row["revised script"]
        if code:
            executable_script, new_execution_status = execute_request_parameter_constraint_verification_script(code, api_response, request_info)
            df.at[index, "revised status"] = new_execution_status
            df.at[index, "revised executable script"] = executable_script
            if new_execution_status == "code error":
                print(f"Error in code {index}" )

        
        with open("code/{index}.py".format(index=index), "w") as f:
            f.write(executable_script)

        if new_execution_status == "code error":
            print(f"Error in code {row}" )
            print(api_response)
            input()

        count += 1

    df.to_excel(code_excel.replace(".xlsx", "_re_executed.xlsx"), index=False)
    print(f"Re-executed {count} code")


if __name__ == "__main__":
    if not os.path.exists("code"):
        os.makedirs("code")
    re_execute_code("approaches/api_rbtest/GitLab Groups API/response_body_input_parameter_constraints_continue.xlsx")
