# Chatbot Project

## Environment Setup
1. **Create and activate a Conda environment**:
    ```bash
    conda create -y -n chatbot python=3.11
    conda activate chatbot
    ```
2. **Install required packages**:
    ```bash
    pip install -r requirements.txt
    ```
3. **Set up environment variables**:
    - Write your `OPENAI_API_KEY` in the `.env` file. A template can be found in `.env.example`. 
    ```bash
    source .env
    ```
## Running the Application
To start the application, use the following command:

```bash
chainlit run app.py
```
## Router Chain Implementation
<img src="images/implementation.png" alt="Setting Panel" width="50%">

## Features

### User Setting Panel
Users have the option to select the specific LLM (language learning model) they prefer for generating responses. The switch between different LLMs can be accomplished within a single conversation session.
<img src="images/setting_panel.png" alt="Setting Panel" width="50%">


### QA with RAG
- **Various Information Source**: The chatbot can retrieve information from web pages, YouTube videos, and PDFs.
- **Source Display**: You can view the source of the information at the end of each answer.
- **LLM Model Identification**:  The specific LLM model utilized for generating the current response is indicated.
- **Router retriever**: Easy to adapt to different domains, as each domain can be equipped with a different retriever.

### Conversation Memory
- **Memory Management**: The chatbot is equipped with a conversation memory feature. If the memory exceeds 500 tokens, it is automatically summarized.

## Presentation

Below is a preview of the web interface for the chatbot:

![Web Page](images/present_web.gif)

## Configuration

To customize the chatbot according to your needs, define your configurations in the `config.toml` file.

## Langsmith Evaluation

To evaluate model generation against human references or log outputs for specific test queries, use Langsmith.

1. Register an account at [Langsmith](https://smith.langchain.com/).
2. Add your `LANGCHAIN_API_KEY` to the `.env` file.
3. Execute the script with your dataset name: 
   ```bash
   python langsmith_tract.py --dataset_name <YOUR DATASET NAME>
   ```
4. Modify the data path in langsmith_evaluation/config.toml if necessary (e.g., path to a CSV file with question and answer pairs).
<img src="images/langsmith-correctness.png" alt="Langsmith" width="50%">