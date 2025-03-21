from textwrap import dedent 
from agno.agent import Agent, RunResponse 
import os
import argparse
from agno.models.google import Gemini   
from agno.team.team import Team 
from perplexity_tool import PerplexityTools     
from firecrawl_tool import FirecrawlTools

def analyze_cryptocurrency(crypto_name, google_api_key, firecrawl_api_key, perplexity_api_key):
    """
    Analyze a cryptocurrency using AI agents.
    
    Args:
        crypto_name (str): Name of cryptocurrency to analyze
        google_api_key (str): Google Gemini API key
        firecrawl_api_key (str): FireCrawl API key
        perplexity_api_key (str): Perplexity API key
    """
    print(f"\n===== AI Finance Assistant =====")
    print(f"Analyzing cryptocurrency: {crypto_name}\n")
    
    # Set API keys as environment variables
    os.environ["GOOGLE_API_KEY"] = google_api_key
    os.environ["FIRECRAWL_API_KEY"] = firecrawl_api_key
    os.environ["PERPLEXITY_API_KEY"] = perplexity_api_key
    
    # Create researcher agent
    researcher = Agent(
        name="Financial Cryptocurrency Researcher",  
        role="Search for financial Cryptocurrency detailed information", 
        model=Gemini(id="gemini-2.0-flash", api_key=google_api_key),
        instructions=[
            'You are a financial cryptocurrency research assistant that can perform cryptocurrency research using firecrawl tool. The tool will search the web, analyze multiple resources, and provide a detailed research report about the coin.', 
            'When given a cryptocurrency name, you should perform a thorough research on the coin using firecrawl tool and provide a detailed research report about the coin.',  
            'You should also include the source of the information in your response.'
        ],
        tools=[FirecrawlTools(api_key=firecrawl_api_key)],
        show_tool_calls=True,
        markdown=True,
    )
    
    # Create analyst agent
    analyst = Agent(
        name="Financial Cryptocurrency Analyst", 
        role="Making Financial Decisions based on the research report to buy or sell the cryptocurrency", 
        model=Gemini(id="gemini-2.0-flash", api_key=google_api_key),
        instructions="""
        You are a famous financial cryptocurrency analyst.
        When given a research report, and user's requirements: 
        - You can always analyze the research report and make a financial decision to tell the user whether and when to buy or sell the cryptocurrency they ask and give your reason.  
        - You should also tell the user the risk level of the cryptocurrency and the potential return.  
        - You can also use `PerplexityTools` to search the web for more possible additional information to help you analyze and make a better decision.  
        - Including proper citations  
        """, 
        tools=[PerplexityTools(api_key=perplexity_api_key)],
        show_tool_calls=True,
        markdown=True, 
    )

    team = Team(
        name = "Financial Cryptocurrecy Team" , 
        model = Gemini(id="gemini-2.0-flash", api_key=google_api_key),   
        mode = "coordinate", 
        members = [researcher, analyst],  
        markdown = True,   
        # success_criteria = "Provide a concise decision to buy or sell the cryptocurrency, time and the reason",  
        instructions = [ 
            """First, perform a thorough and deep research on the coin using firecrawl tool. 
                Then, analyze the research findings and make a financial decision to tell the user whether and when to buy or sell the cryptocurrency they ask and give your reason.   
                Important: the analyst may want to use perplexity tool to search the web for more possible additional information to help analyze and make a better decision.  
            """

        ],
        # debug_mode=True, 
        show_members_responses = True, 
        enable_agentic_context = True, 
        share_member_interactions = True 
    ) 
    team.print_response(f"Is it a good time to sell {crypto_name}?")
    # print(response.content)



def main():
    parser = argparse.ArgumentParser(description="AI Finance Assistant - Cryptocurrency Analyzer")
    parser.add_argument("--crypto", required=True, help="Name of cryptocurrency to analyze")
    parser.add_argument("--google-api-key", required=True, help="Google Gemini API Key")
    parser.add_argument("--firecrawl-api-key", required=True, help="FireCrawl API Key")
    parser.add_argument("--perplexity-api-key", required=True, help="Perplexity API Key")
    
    args = parser.parse_args()
    
    try:
        analyze_cryptocurrency(
            args.crypto,
            args.google_api_key,
            args.firecrawl_api_key,
            args.perplexity_api_key
        )
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("Please check your API keys and try again.")

if __name__ == "__main__":
    main()
#  python 03-aisearch/aisearch_agent.py --crypto bitcoin --google-api-key AIzaSyB7ahTr-CMTOXpd9V72VrWxteMOPfImu3k --firecrawl-api-key fc-8540ab317e53490591ab570550759f02 --perplexity-api-key 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