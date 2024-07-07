import os
import re
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from groq import Groq

# Initialize Groq with the API key
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

chat = ChatGroq(
    temperature=0,
    model="mixtral-8x7b-32768",
    api_key=client
)

# Define a chain of thought prompt template for SQL injection detection
sys = """
    You are an expert in cybersecurity and programming. Your task is to detect SQL injection vulnerabilities in the given log entries.
    Follow these steps:
    
    1. Parse the log entries from the file at {log_filepath} to extract the URL part.
    2. Identify patterns typically associated with SQL injection attacks.
    3. Implement a function to detect these patterns in the log entries.
    4. Return a summary in JSON format indicating which specific logs have the attacks and provide a solution for this attack.

    This is an example of a function you can use to detect the attack from the logs:
    ```
    # Function to detect SQL injection in a log file
    def detect_sql_injection_in_log_file(log_file_path):
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
                "solution": ""  # Placeholder for the solution
            }
        return summary
    ```
    """
human = "Using the function provided in Python, detect whether SQL injection is found or not, and return a summary in JSON format indicating which logs have the attacks and provide a solution for this attack."

# Prompt template to generate the solution using Mistral
solution_prompt = """
    Considering the SQL injection vulnerabilities found in the log entries, it is recommended to sanitize user inputs and use parameterized queries to prevent such attacks in the future.
    """


# Create a prompt template instance
sys_template = ChatPromptTemplate.from_messages([("system", sys), ("human", human)])

# Chain for SQL injection detection
chain = sys_template | chat

# Example of how to use the function to detect SQL injection and get a summary
log_filepath = "./sqllogs.log"

out = chain.invoke({"attacks_found": 0,  # Provide a default value or adjust based on actual findings
    'log_filepath': log_filepath
})

print(out)