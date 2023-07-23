from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from alpaca_stock_screener.tool import StockScreenerTool
from util import load_secrets

load_secrets()

tools = [StockScreenerTool()]
llm = ChatOpenAI(model_name='gpt-4', temperature=0)
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

agent.run(
    "Which top 5 stocks are currently a good buy?"
)