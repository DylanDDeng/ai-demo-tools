from agno.agent import Agent  
from agno.models.openrouter import OpenRouter
from agno.tools.thinking import ThinkingTools
from agno.tools.yfinance import YFinanceTools    
from textwrap import dedent  


""" 

This is a example of using the thinking tool published by Anthropic. 
This example is from Agno   


"""



thinking_agent = Agent(
    model = OpenRouter(id="anthropic/claude-3.7-sonnet",max_tokens = 8192), 
    tools = [
        ThinkingTools(), 
        YFinanceTools(stock_price=True, analyst_recommendations =True, company_info=True,company_news=True), 
    ], 
    instructions = dedent("""\
   ## Using the thinking tool 
    Before taking any action, starting tool calls or responding to user's query after receiving tool results, use the thinking tool as a scratchpad. 
    """),  
    show_tool_calls = True, 
    markdown = True
) 

thinking_agent.print_response("Is it a good time to sell Apple stock?", stream=True) 


