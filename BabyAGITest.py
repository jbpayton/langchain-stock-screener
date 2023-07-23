from util import load_secrets
from typing import Optional
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.experimental import BabyAGI
from langchain.tools import DuckDuckGoSearchRun, Tool, WikipediaQueryRun
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from langchain.embeddings import OpenAIEmbeddings
from alpaca_stock_screener.tool import StockScreenerTool

load_secrets()

# Define your embedding model
embeddings_model = OpenAIEmbeddings()
# Initialize the vectorstore as empty
import faiss

embedding_size = 1536
index = faiss.IndexFlatL2(embedding_size)

vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})

from langchain.agents import ZeroShotAgent, AgentExecutor
from langchain import LLMChain

todo_prompt = PromptTemplate.from_template(
    "You are a planner who is an expert at coming up with a todo list for a given objective. Come up with a todo list "
    "for this objective: {objective} "
)

todo_chain = LLMChain(llm=ChatOpenAI(temperature=0, model_name="gpt-4"), prompt=todo_prompt)

tools = [
    DuckDuckGoSearchRun(),
    Tool(
        name="TODO",
        func=todo_chain.run,
        description="useful for when you need to come up with todo lists. Input: an objective to create a todo list "
                    "for. Output: a todo list for that objective. Please be very clear what the objective is!",
    ),
    StockScreenerTool()
]


prefix = """You are an AI who performs one task based on the following objective: {objective}. Take into account 
these previously completed tasks: {context}. """
suffix = """Question: {task}
{agent_scratchpad}"""
prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["objective", "task", "context", "agent_scratchpad"],
)

llm = ChatOpenAI(temperature=0, model_name="gpt-4")

llm_chain = LLMChain(llm=llm, prompt=prompt)
tool_names = [tool.name for tool in tools]
agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names, handle_parsing_errors=True)
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
)

OBJECTIVE = "I want to make money: Could you give me some suggestions on short term (held for two weeks) options that " \
            "I could purchase on today, in aggregate no larger than $2000 in value. I only want simple options like " \
            "PUT and CALL options. "

# Logging of LLMChains
verbose = False
# If None, will keep on going forever
max_iterations: Optional[int] = 10
baby_agi = BabyAGI.from_llm(
    llm=llm, vectorstore=vectorstore, task_execution_chain=agent_executor, verbose=verbose, max_iterations=max_iterations, handle_parsing_errors=True
)

baby_agi({"objective": OBJECTIVE})
