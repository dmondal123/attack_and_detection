import os
import json
import re
from dotenv import load_dotenv
from groq import Groq
load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

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

logs = "./filteredlogs.log"

mixtral_msg = f"Detect the sql injection attack with the logs, {logs}"

def query_mistral(msg, functions=None):
    """
    This function sends a request to the Mistral TGI endpoint using a Groq API token.
    """
    response = client.chat.completions.create(model="mixtral-8x7b-32768",
                                              messages=[{'role': 'user', 'content': msg}],
                                              tools=functions)

    return response


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

# Extract tool call details from the response
tool_call = result.choices[0].message.tool_calls[0]
#print(tool_call)

# print (result.choices[0].message.tool_calls[0].function)

# Extract the function name and arguments
tool_name = tool_call.function.name
tool_args = json.loads(tool_call.function.arguments)

# Ensure the arguments are properly formatted as a dictionary
if isinstance(tool_args, str):
    tool_args = json.loads(tool_args)

# Call the function with the correct arguments
response = detect_sql_injection_in_log_file(**tool_args)
#print(response)

solution_msg = f"Give a solution for sql injection attack with the logs, {logs}"

def query_solution(msg):
    """
    This function sends a request to the Mistral TGI endpoint using a Groq API token.
    """
    response = client.chat.completions.create(model="mixtral-8x7b-32768",
                                              messages=[{'role': 'user', 'content': msg}],
                                              max_tokens=200)

    return response

solution = query_solution(solution_msg)
#print(solution)
content = solution.choices[0].message.content
#print(content)

response["solution"] = content
print(response)
# Save summary as JSON file
save_folder = "summary"
os.makedirs(save_folder, exist_ok=True)  # Create folder if it doesn't exist
save_path = os.path.join(save_folder, "summary.json")

with open(save_path, 'w') as json_file:
    json.dump(response, json_file, indent=4)

print("Response stored in JSON format")