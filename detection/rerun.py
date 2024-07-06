import os
import re
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from groq import Groq
import json

# Initialize Groq with the API key
#client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

chat = ChatGroq(
    temperature=0,
    model="mixtral-8x7b-32768",
    api_key="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"
)

# Define a chain of thought prompt template
sys = """
    You are an expert in cybersecurity and programming. Your task is to detect SQL injection vulnerabilities in the given log entries.
    Follow these steps:
    
    1. Parse the log entries to extract the URL part.
    2. Identify patterns typically associated with SQL injection attacks.
    3. Implement a function to detect these patterns in the log entries.
    4. Return a summary in JSON format indicating which specific logs have the attacks and provide a solution for this attack.

    Log entries:
    {logs}

    Output:
    Using the function provided in Python, detect whether SQL injection is found or not, and return a summary in JSON format indicating which logs have the attacks and provide a solution for this attack
    """


human = "Using the function provided in Python, detect whether SQL injection is found or not, and return a summary in JSON format indicating which logs have the attacks and provide a solution for this attack."

def detect_sql_injection_in_log_file(log_file_path):
    """
    Detect SQL injection patterns in a log file and return a summary.

    This function reads the last 50,000 lines of a log file and detects lines that
    match common SQL injection patterns. It returns a summary in JSON format indicating
    the number of attacks found, the specific logs with the attacks, and a recommended solution.

    Parameters:
    log_file_path (str): The path to the log file to be analyzed.

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
    
    with open(log_file_path, 'r') as log_file:
        lines = log_file.readlines()
        suspicious_lines = []

        for line in lines[-50000:]:  # Analyze the last 50,000 lines
            if pattern.search(line):
                suspicious_lines.append(line.strip())

        
        # Summarize findings in JSON format
        summary = {
            "attacks_found": len(suspicious_lines),
            "logs_with_attacks": suspicious_lines,
            "solution": "Sanitize inputs and use parameterized queries to prevent SQL injection."
        }
        # Save summary as JSON file
        save_folder = "summary"
        os.makedirs(save_folder, exist_ok=True)  # Create folder if it doesn't exist
        save_path = os.path.join(save_folder, "summary.json")

        with open(save_path, 'w') as json_file:
            json.dump(summary, json_file, indent=4)

    return summary

prompt = ChatPromptTemplate.from_messages([("system", sys), ("human", human)])

chain = prompt | chat

log_filepath = "./sqllogs.log"
# Execute the chain to get the detection code and summary
response = chain.invoke({"logs": log_filepath})

# Print the response from Mistral
print(response)

# Example of how to use the function to detect SQL injection and get a summary

summary = detect_sql_injection_in_log_file(log_filepath)
#print(summary)
