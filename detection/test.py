import os
import json
import re
from dotenv import load_dotenv
from groq import Groq
load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def detect_sql_injection_in_log_file(logs):
    """
    Detect SQL injection patterns in log entries and return a summary.

    This function analyzes the provided log entries and detects lines that
    match common SQL injection patterns. It returns a summary in JSON format indicating
    the number of attacks found, the specific logs with the attacks, and a recommended solution.

    Parameters:
    logs (str): The log entries to be analyzed.

    Returns:
    dict: A summary containing the number of attacks found, the specific logs with the attacks, 
          and a recommended solution. The summary is also saved as a JSON file in a 'summary' folder.
    """
    # Define the regex pattern to detect SQL injection patterns
    sql_injection_patterns = [
        r"SELECT", r"UNION", r"INSERT", r"UPDATE", r"DELETE", r"DROP", r"ALTER", r"AND", r"OR",
        r"--", r";", r"/\*", r"\*/", r"'", r"\""
    ]
    pattern = re.compile('|'.join(sql_injection_patterns), re.IGNORECASE)
    
    # Split logs into lines
    lines = logs.split('\n')
    suspicious_lines = []

    for line in lines[-50000:]:  # Analyze the last 50,000 lines
        if pattern.search(line):
            suspicious_lines.append(line.strip())

    # Summarize findings in JSON format
    summary = {
        "attacks_found": len(suspicious_lines),
        "logs_with_attacks": suspicious_lines,
        "solution": ""
    }

    return summary


logs = '''
172.16.93.1 - - [03/Nov/2013:18:25:07 +0000] "GET /vuln.php?id=1%20AND%20MID((SELECT%20IFNULL(CAST(surname%20AS%20CHAR),0x20)%20FROM%20user%20ORDER%20BY%20id%20LIMIT%200,1),3,1)>64 HTTP/1.1" 200 127 "Python-urllib/2.7"

172.16.93.1 - - [03/Nov/2013:18:25:07 +0000] "GET /vuln.php?id=1%20AND%20MID((SELECT%20IFNULL(CAST(surname%20AS%20CHAR),0x20)%20FROM%20user%20ORDER%20BY%20id%20LIMIT%200,1),3,1)>96 HTTP/1.1" 200 127 "Python-urllib/2.7"

172.16.93.1 - - [03/Nov/2013:18:25:07 +0000] "GET /vuln.php?id=1%20AND%20MID((SELECT%20IFNULL(CAST(surname%20AS%20CHAR),0x20)%20FROM%20user%20ORDER%20BY%20id%20LIMIT%200,1),3,1)>112 HTTP/1.1" 200 75 "Python-urllib/2.7"

172.16.93.1 - - [03/Nov/2013:18:25:07 +0000] "GET /vuln.php?id=1%20AND%20MID((SELECT%20IFNULL(CAST(surname%20AS%20CHAR),0x20)%20FROM%20user%20ORDER%20BY%20id%20LIMIT%200,1),3,1)>108 HTTP/1.1" 200 127 "Python-urllib/2.7"

172.16.93.1 - - [03/Nov/2013:18:25:07 +0000] "GET /vuln.php?id=1%20AND%20MID((SELECT%20IFNULL(CAST(surname%20AS%20CHAR),0x20)%20FROM%20user%20ORDER%20BY%20id%20LIMIT%200,1),3,1)>108 HTTP/1.1" 200 75 "Python-urllib/2.7"

172.16.93.1 - - [03/Nov/2013:18:25:07 +0000] "GET /vuln.php?id=1%20AND%20MID((SELECT%20IFNULL(CAST(surname%20AS%20CHAR),0x20)%20FROM%20user%20ORDER%20BY%20id%20LIMIT%200,1),3,1)>106 HTTP/1.1" 200 75 "Python-urllib/2.7"

172.16.93.1 - - [03/Nov/2013:18:25:07 +0000] "GET /vuln.php?id=1%20AND%20MID((SELECT%20IFNULL(CAST(surname%20AS%20CHAR),0x20)%20FROM%20user%20ORDER%20BY%20id%20LIMIT%200,1),3,1)>105 HTTP/1.1" 200 75 "Python-urllib/2.7"

172.16.93.1 - - [03/Nov/2013:18:25:07 +0000] "GET /vuln.php?id=1%20AND%20MID((SELECT%20IFNULL(CAST(surname%20AS%20CHAR),0x20)%20FROM%20user%20ORDER%20BY%20id%20LIMIT%200,1),4,1)>128 HTTP/1.1" 200 75 "Python-urllib/2.7"

172.16.93.1 - - [03/Nov/2013:18:25:07 +0000] "GET /vuln.php?id=1%20AND%20MID((SELECT%20IFNULL(CAST(surname%20AS%20CHAR),0x20)%20FROM%20user%20ORDER%20BY%20id%20LIMIT%200,1),4,1)>264 HTTP/1.1" 200 127 "Python-urllib/2.7"

172.16.93.1 - - [03/Nov/2013:18:25:07 +0000] "GET /vuln.php?id=1%20AND%20MID((SELECT%20IFNULL(CAST(surname%20AS%20CHAR),0x20)%20FROM%20user%20ORDER%20BY%20id%20LIMIT%200,1),4,1)>296 HTTP/1.1" 200 127 "Python-urllib/2.7"
'''

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
                "logs": {
                    "type": "string",
                    "description": "The logs of a vulnerable application with sql injection vulnerability."
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
print(response)

solution_msg = f"Give a solution for sql injection attack with the logs, {logs}"

def query_solution(msg):
    """
    This function sends a request to the Mistral TGI endpoint using a Groq API token.
    """
    response = client.chat.completions.create(model="mixtral-8x7b-32768",
                                              messages=[{'role': 'user', 'content': msg}],
                                              max_tokens=100)

    return response

solution = query_solution(solution_msg)
#print(solution)
content = solution.choices[0].message.content
print(content)

response["solution"] = content

# Save summary as JSON file
save_folder = "summary"
os.makedirs(save_folder, exist_ok=True)  # Create folder if it doesn't exist
save_path = os.path.join(save_folder, "summary.json")

with open(save_path, 'w') as json_file:
    json.dump(response, json_file, indent=4)

print("Response stored in JSON format")