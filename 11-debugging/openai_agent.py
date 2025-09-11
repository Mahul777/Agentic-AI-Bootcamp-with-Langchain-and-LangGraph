# 🔸 1. Import Required Libraries
from typing import Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import add_messages
# ChatGroq
from langchain_groq import ChatGroq
# TypedDict
from typing import TypedDict
import os
from dotenv import load_dotenv
#✅ Purpose of each:
# •	StateGraph: For building workflows.
# •	ChatOpenAI: LLM model.
# •	add_messages: Reducer to handle message state.
# •	load_dotenv(): Load .env file for API keys.

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAINAPI_KEY")

# 🔸 2. Create State Class
class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
# ✅ This State class will:
# •	Store a list of messages 💬.
# •	Use add_messages to collect new inputs during chat

# 🔸 3. Initialize the Model
model=ChatGroq(model="llama-3.3-70b-versatile")

# 🔸 4. Define Graph Function
def make_default_graph():
    workflow = StateGraph(State) 

    def call_model(state):
        return {"messages": model.invoke(state["messages"])}

    workflow.add_node("agent", call_model)
    workflow.set_entry_point("agent")
    workflow.set_finish_point("agent")

    workflow.add_edge(START, "agent")
    workflow.add_edge("agent", END)

    agent = workflow.compile()
    return agent
# ✅ What this does:
# •	📌 Creates a graph workflow.
# •	🧠 Adds a node "agent" that calls the model.
# •	🔁 Connects start → agent → end.
# •	✅ Compiles and returns the agent.

def make_alternate_graph():
    workflow = StateGraph(State)

    def add(a: int, b: int):
        return a + b

    tools = {"add": lambda a, b: add(a, b)}
    tool_node = ToolNode(tools)

    def call_model(state):
        return {"messages": model.invoke(state["messages"])}

    workflow.add_node("tools", tool_node)
    workflow.add_node("agent", call_model)

    workflow.set_entry_point("agent")
    workflow.set_finish_point("agent")

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", {
        "continue": END,
        "tool_call": "tools"
    })
    workflow.add_edge("tools", "agent")

    return workflow.compile()
# ✅ This graph has:
# •	👨‍💻 A tool: simple add function (a + b)
# •	🤖 Agent can now call tools like calculator.
# •	🔁 Workflow:
# •	START → agent → tool → agent → END

# 🔸 5. Call the Function
#agent = make_default_graph()
agent = make_alternate_graph()
# ✅ 🧾 Create Landgraf Config File (langgraph.json)
# {
#   "dependencies": ["."],
#   "graphs": {
#     "openai_agent": {
#       "entrypoint": "openai_agent.py:agent"
#     }
#   },
#   "env_file": "../.env"
# }
# ✅ Explanation:
# •	"dependencies" → Current folder.
# •	"entrypoint" → File and variable (openai_agent.py:agent).
# •	"env_file" → Path to .env file outside the folder

 
