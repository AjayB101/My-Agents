from dotenv import load_dotenv
from langchain_groq import ChatGroq
load_dotenv(override=True)

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
