from fastapi import FastAPI, UploadFile, File, HTTPException
import os
import json
import re
from dotenv import load_dotenv
import sys
from typing import Dict

#sys.path.append('/Users/dmondal/miniforge3/envs/llmapp/lib/python3.10/site-packages')
from groq import Groq

load_dotenv()

# client = Groq(api_key="GROQ_API_KEY")
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

app = FastAPI()


def detect_sql_injection_in_log_file(log_filepath):
    """
    Detect SQL injection patterns in WebGoat log entries from a file and return a summary.

    This function analyzes the log entries from the provided file and detects lines that
    match SQL injection patterns specific to WebGoat logs. It returns a summary in JSON format 
    indicating the number of attacks found, the specific logs with the attacks, and a recommended solution.

    Parameters:
    log_filepath (str): The file path of the log entries to be analyzed.

    Returns:
    dict: A summary containing the number of attacks found, the specific logs with the attacks, 
          and a recommended solution. The summary is also saved as a JSON file in a 'summary' folder.
    """
    # Read the log file content
    with open(log_filepath, 'r') as file:
        logs = file.read()
    
    # Define the regex patterns to detect SQL injection in WebGoat logs
    sql_injection_patterns = [
        r'SqlInjectionAdvanced/attack6a',  # SQL Injection lesson endpoints
        r'parameters=\{masked\}',  # Masked parameters, potentially containing SQL injection
        r'Extracted JDBC value.*SqlInjection',  # Database activity related to SQL Injection lessons
        r'org\.owasp\.webgoat\.container\.lessons\.Assignment.*SqlInjection',  # SQL Injection lesson assignments
    ]
    pattern = re.compile('|'.join(sql_injection_patterns), re.IGNORECASE)
    
    # Split logs into lines
    lines = logs.split('\n')
    suspicious_lines = []

    for line_number, line in enumerate(lines, 1):
        if pattern.search(line):
            suspicious_lines.append(f"Line {line_number}: {line.strip()}")

    summary = {
        "attacks_found": len(suspicious_lines),
        "logs_with_attacks": suspicious_lines,
        "solution": ""
    }

    return summary


def query_mistral(msg: str, functions=None):
    """
    This function sends a request to the Mistral TGI endpoint using a Groq API token.
    """
    response = client.chat.completions.create(model="mixtral-8x7b-32768",
                                              messages=[{'role': 'user', 'content': msg}],
                                              tools=functions)
    return response


def query_solution(msg: str):
    """
    This function sends a request to the Mistral TGI endpoint using a Groq API token.
    """
    response = client.chat.completions.create(model="mixtral-8x7b-32768",
                                              messages=[{'role': 'user', 'content': msg}],
                                              max_tokens=200)
    return response


@app.post("/detect_sql_injection/")
async def detect_sql_injection(file: UploadFile = File(...)):
    try:
        # Save the uploaded file temporarily
        log_filepath = f"./temp_{file.filename}"
        with open(log_filepath, "wb") as buffer:
            buffer.write(file.file.read())

        # Detect SQL injection in the log file
        summary = detect_sql_injection_in_log_file(log_filepath)

        # Get the solution for the detected SQL injection
        mixtral_msg = f"Detect the sql injection attack with the logs, {log_filepath}"
        detect_sql_injection_function = {
            "type": "function",
            "function": {
                "name": "detect_sql_injection_in_log_file",
                "description": (
                    "Detects SQL injection patterns in a log file and returns a summary. "
                    "This function reads the last 50,000 lines of a log file and detects lines that "
                    "match common SQL injection patterns. It returns a summary in JSON format indicating "
                    "the number of attacks found, the specific logs with the attacks, and a recommended solution."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "log_filepath": {
                            "type": "string",
                            "description": "The file path of the logs of a vulnerable application with SQL injection vulnerability."
                        }
                    },
                },
            }
        }
        result = query_mistral(mixtral_msg, functions=[detect_sql_injection_function])
        tool_call = result.choices[0].message.tool_calls[0]
        tool_args = json.loads(tool_call.function.arguments)
        if isinstance(tool_args, str):
            tool_args = json.loads(tool_args)
        response = detect_sql_injection_in_log_file(**tool_args)

        solution_msg = f"Give a solution for sql injection attack with the logs, {log_filepath}"
        solution = query_solution(solution_msg)
        response["solution"] = solution.choices[0].message.content

        # Save summary as JSON file
        save_folder = "summary"
        os.makedirs(save_folder, exist_ok=True)
        save_path = os.path.join(save_folder, "summary.json")
        with open(save_path, 'w') as json_file:
            json.dump(response, json_file, indent=4)

        os.remove(log_filepath)  # Clean up the saved file
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
