# 🔹 1. Importing Required Libraries
from fastapi import FastAPI
# ✔️ FastAPI is a Python framework used to build REST APIs.

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# ✔️ These are from LangChain core:
# •	ChatPromptTemplate → Used to define how we talk to the model.
# •	StrOutputParser → Helps convert the model's response to clean string output.

from langchain_groq import ChatGroq
# ✔️ This imports the Groq model class from LangChain's Groq integration.

import os
from dotenv import load_dotenv
# ✔️ These help you load environment variables (like API keys) from a .env file.

from langserve import add_routes
# ✔️ langserve lets you convert your LangChain chain into a REST API route.

# 🔹 2. Load Environment Variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
# ✔️ Loads .env file and gets the Groq API key from there.
# 🧠 You should have a .env file with:
# GROQ_API_KEY=your_api_key_here

# 🔹 3. Initialize the LLM Model
model = ChatGroq(
    model_name="llama-3.1-8b-instant",
    groq_api_key=groq_api_key
)
# ✔️ This line connects to the Gemma 2-9b model using your Groq API key.

# 🔹 4. Create a Prompt Template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])
# 🧠 What's happening here?
# ✔️ You're telling the model what to do:
# •	System message gives the instruction (e.g., "Translate into French")
# •	User message gives the actual input text (e.g., "Hello")
# So, this works like:
# System: "Translate the following into French:"
# User: "Hello"


# 🔹 5. Create an Output Parser
parser = StrOutputParser()
# ✔️ Converts the model's output (which might include extra formatting) into a clean string.

# 🔹 6. Create the LangChain Chain
chain = prompt_template | model | parser
# ✔️ This combines everything into a chain:
# 1.	Prompt is built using your input
# 2.	Model gives response
# 3.	Output is parsed to clean string

# 🔹 7. Create the FastAPI App
app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API server using Langchain runnable interfaces"
)
# ✔️ This creates your API app with a name, version, and description.

# 🔹 8. Add the Chain as an API Route
add_routes(
    app,
    chain,
    path="/chain"
)
# ✔️ This line turns your chain into an API endpoint at:
# /chain
# Which means:
# •	You can send requests to /chain/invoke to get translations.
# •	FastAPI automatically builds API docs at /docs.

# 🔹 9. Run the Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
# ✔️ Starts the API server locally:
# •	Address: http://127.0.0.1:8000
# •	Docs: http://127.0.0.1:8000/docs
# 🧠 This allows you to test your API in browser or Postman.











