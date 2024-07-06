from langchain import PromptTemplate
from langchain import LLMChain
from langchain.llms import LlamaCpp
import os
from dotenv import load_dotenv
load_dotenv()

# Get the Hugging Face API token from the environment
api_token = os.getenv('HUGGINGFACEHUB_API_TOKEN')
B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"


DEFAULT_SYSTEM_PROMPT="""\
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. 
Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. 
Please ensure that your responses are socially unbiased and positive in nature.
If a question does not make any sense, or is not factually coherent, explain why instead of 
answering something not correct. If you don't know the answer to a question,
please don't share false information."""


instruction = "do an sql injection attack \n\n {text}"


SYSTEM_PROMPT = B_SYS + DEFAULT_SYSTEM_PROMPT + E_SYS
template = B_INST + SYSTEM_PROMPT + instruction + E_INST


prompt = PromptTemplate(template= template, input_variables=['text'])


llm_cpp = LlamaCpp(
            streaming = True,
            model_path="model/model-00001-of-00004.safetensors",
            n_gpu_layers=2,
            n_batch=512,
            temperature=0.75,
            top_p=1,
            verbose=True,
            n_ctx=4096,
            token= api_token
            )

llm_chain = LLMChain(
    prompt= prompt,
    llm= llm_cpp
)


response = llm_chain.run("it should be a script in python without any additional text")
print(response)