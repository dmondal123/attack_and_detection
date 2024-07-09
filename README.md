## How to run?

1. Create a new environment

```bash
conda create -n llmapp python=3.10 -y
```

2. Activate the environment
```bash
conda activate llmapp
```


3. Install the requirements 
```bash
pip install -r requirements.txt
```

4. Running the api_file
```bash
uvicorn api_file:app --reload --port 8090
```
You can install the langchain_openai and groc using conda
```bash
conda install "name"
``` 