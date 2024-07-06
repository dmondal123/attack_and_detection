from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_core.chains import Chain
from pathlib import Path

# Define the prompt template
template = """Generate a Python script that performs a security attack vector analysis.


chat_prompt = f"""
<s>[INST] {prompt_1} [/INST]
{response_1}
</s>
<s>[INST] {prompt_2} [/INST]
"""
print(chat_prompt)

Instructions: {instructions}

Generated Script:
"""

llm = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

prompt = PromptTemplate.from_template(template)

instructions = "Create a script that scans for open ports on a given IP address and attempts a brute-force login on discovered services."

llm_chain = prompt | llm

class ComplexLangChain(Chain):
    def _call(self, inputs):
        prompt_result = self.input_chain.invoke(inputs)
        model_result = self.output_chain.invoke(prompt_result)
        return model_result

complex_chain = ComplexLangChain(input_chain=prompt, output_chain=llm)

# Generate the attack vector script
generated_script = complex_chain.invoke({"instructions": instructions})

# Save the generated script to a local file
output_path = Path("generated_attack_vector.py")
output_path.write_text(generated_script)

print(f"Generated script saved to {output_path}")
