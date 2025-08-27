import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
load_dotenv()
# OpenAI API Key (Replace with your key)
api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = api_key

llm = init_chat_model("openai:gpt-4.1")