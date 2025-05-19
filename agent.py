from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig

from tools import execute_sql
from typing import TypedDict, Optional

# Define the state
class AgentState(TypedDict):
    input: str
    output: Optional[str]

llm = ChatOpenAI(model="gpt-4", temperature=0)

# ✅ Define prompt for tool-calling agent
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert SQL assistant connected to a database. Use tools to answer user's query."),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# ✅ Create the agent with prompt
agent = create_tool_calling_agent(llm=llm, tools=[execute_sql], prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=[execute_sql], verbose=True)

# ✅ Define the function used in the graph
def run_agent_step(state: AgentState) -> AgentState:
    if "input" not in state:
        raise ValueError("State must contain 'input'")
    result = agent_executor.invoke({"input": state["input"]}, config=RunnableConfig())
    return {"input": state["input"], "output": result.get("output")}

# ✅ Build LangGraph
graph = StateGraph(AgentState)
graph.add_node("agent_step", run_agent_step)
graph.set_entry_point("agent_step")
graph.add_edge("agent_step", END)

agent_graph = graph.compile()
