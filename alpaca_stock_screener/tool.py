# Import things that are needed generically
from langchain import LLMMathChain, SerpAPIWrapper
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool, StructuredTool, Tool, tool
from typing import Optional, Type, Any
from .StockScreener import StockScreener

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

class StockScreenerTool(BaseTool):
    name = "Stock Screener"
    description = (
        "This tool screens stocks using historical price data for specified stocks, computes various technical indicators, and allows "
        "queries based on these indicators. The technical indicators include current price, 52-week, 26-week, and 13-week "
        "high and low, short-term, medium-term, and long-term volatility, 5-day, 10-day, 20-day, 50-day, 100-day, and "
        "200-day moving averages, percent change from 52-week, 26-week, and 13-week high and low, percent change from "
        "200-day, 100-day, 50-day, 20-day, 10-day, and 5-day moving averages, 14-day RSI, and beta. Input: a natural language query "
        "specifying desired values of these technical indicators. Output: a list of stocks whose technical indicators match "
        "the query. Note: This tool does not handle queries involving fundamental indicators like earnings growth or "
        "debt-to-equity ratio. This tool uses an internal dataframe for this data, and handles this operation internally."
    )

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        screener = StockScreener()
        tool_output = screener.run(query)
        return tool_output

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Stock screener tool does not support async")
