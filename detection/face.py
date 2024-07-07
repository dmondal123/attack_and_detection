import os
import json
import re
from dotenv import load_dotenv
from groq import Groq
_ = load_dotenv()


# GPT_MODEL = "gpt-3.5-turbo"

#   openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
#   openai_response = openai_client.chat.completions.create(
#     model = GPT_MODEL,
#     messages = [{'role': 'user', 'content': msg}],
#     tools = functions)
#   return openai_response



client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
def query_mistral(msg, functions=None):
    """
    This function sends a request to the Mistral TGI endpoint using a Groq API token.
    """
    response = client.chat.completions.create(model = "mixtral-8x7b-32768",
    messages = [{'role': 'user', 'content':msg}],
    tools = functions)

    return response

openai_function = {
  "type": "function",
  "function": {
    "name": "draw_clown_face",
    "description": "Draws a customizable, simplified clown face using matplotlib.",
    "parameters": {
      "type": "object",
      "properties": {
        "face_color": {
          "type": "string",
          "description": "Color of the clown's face."
        },
        "eye_color": {
          "type": "string",
          "description": "Color of the clown's eyes."
        },
        "nose_color": {
          "type": "string",
          "description": "Color of the clown's nose."
        }
        }
      }
    }
  }



openai_msg = \
"Hey can you draw a pink clown face with a red nose"

result = query_mistral(openai_msg, functions=[openai_function])

print (result.choices[0].message.tool_calls[0].function)

tool_name = result.choices[0].message.tool_calls[0].function.name
tool_args = result.choices[0].message.tool_calls[0].function.arguments
function_call = f"{tool_name}(**{tool_args})"
print (function_call)

exec(function_call)