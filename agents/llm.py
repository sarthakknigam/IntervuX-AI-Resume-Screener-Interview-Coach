import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

print("Imported successfully")

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
print("API Key:", api_key)

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=api_key,
    temperature=0,
)

print("LLM Created")