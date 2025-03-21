from openai import OpenAI
import os
from typing import Optional, List, Dict, Any

from agno.agent import Agent
from agno.tools import Toolkit
from agno.utils.log import logger


class PerplexityTools(Toolkit):
    """
    A toolkit for interacting with Perplexity AI's API within the Agno framework.
    
    This toolkit provides methods to query Perplexity AI for information with citations.
    """
    
    DEFAULT_SYSTEM_PROMPT = (
        "You are an artificial intelligence assistant and you need to "
        "engage in a helpful, detailed, polite conversation with a user."
    )
    
    def __init__(self, api_key: Optional[str] = None, model: str = "sonar-pro"):
        """
        Initialize the PerplexityTools toolkit.
        
        Args:
            api_key (str, optional): Perplexity API key. If None, uses PERPLEXITY_API_KEY environment variable.
            model (str, optional): Perplexity model to use.
        """
        super().__init__(name="perplexity_tools")  
        
        # Get API key from environment variable if not provided
        if api_key is None:
            api_key = os.environ.get("PERPLEXITY_API_KEY")
            if not api_key:
                raise ValueError(
                    "No API key provided. Either pass api_key parameter or set PERPLEXITY_API_KEY environment variable."
                )
        
        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=self.api_key, base_url="https://api.perplexity.ai")
        
        # Register the methods that can be called by the agent
        self.register(self.query_perplexity)
        self.register(self.search_with_citations)
    
    def query_perplexity(self, query: str, system_prompt: Optional[str] = None) -> str:
        """
        Query Perplexity AI with a specific question and return the response content as a formatted string.
        
        Args:
            query (str): The user's question to ask Perplexity.
            system_prompt (str, optional): The system prompt to guide the AI's behavior.
            
        Returns:
            str: Formatted response from Perplexity AI.
        """
        logger.info(f"Querying Perplexity AI: {query}")
        
        # Use default system prompt if not provided
        if system_prompt is None:
            system_prompt = self.DEFAULT_SYSTEM_PROMPT
        
        # Set up messages
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ]
        
        try:
            # Make API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
            )
            
            # Extract content and citations
            content = response.choices[0].message.content
            citations = response.citations if hasattr(response, 'citations') else []
            
            logger.info(f"Received response with {len(citations)} citations")
            
            # Format the response as a string
            formatted_response = content
            
            # Add citations if available
            if citations:
                formatted_response += "\n\n**Citations:**\n"
                for i, citation in enumerate(citations, 1):
                    formatted_response += f"{i}. {citation}\n"
            
            return formatted_response
            
        except Exception as e:
            logger.warning(f"Failed to query Perplexity AI: {e}")
            return f"Error: Failed to query Perplexity AI: {e}"
    
    def search_with_citations(self, 
                              query: str, 
                              system_prompt: Optional[str] = None,
                              include_formatted_citations: bool = True) -> str:
        """
        Search for information using Perplexity AI and format the response with citations.
        
        Args:
            query (str): The search query to ask Perplexity.
            system_prompt (str, optional): The system prompt to guide the AI's behavior.
            include_formatted_citations (bool, optional): Whether to include formatted citations in the response.
            
        Returns:
            str: Formatted response with content and optionally citations.
        """
        logger.info(f"Searching with citations: {query}")
        
        # Use query_perplexity directly since it now returns a properly formatted string
        return self.query_perplexity(query, system_prompt)


# Example usage with Agno Agent
if __name__ == "__main__":
    # Set your API key in environment variable before running
    # os.environ["PERPLEXITY_API_KEY"] = "your-api-key-here"
    
    # For demonstration purposes, you can also set the API key directly
    # api_key = "your-api-key-here"
    # perplexity_tools = PerplexityTools(api_key=api_key)
    
    # Or use the environment variable (recommended)
    perplexity_tools = PerplexityTools()
    
    # Create an Agno agent with the Perplexity toolkit
    agent = Agent(
        tools=[perplexity_tools],
        show_tool_calls=True,
        markdown=True,
    )
    
    # Example query
    agent.print_response("What are the latest advancements in quantum computing?")