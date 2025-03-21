from firecrawl import FirecrawlApp
import os
import json
from typing import Optional, Dict, Any, Callable, List

from agno.agent import Agent
from agno.tools import Toolkit
from agno.utils.log import logger


class FirecrawlTools(Toolkit):
    """
    A toolkit for interacting with FireCrawl API within the Agno framework.
    
    This toolkit provides methods to perform deep research on topics using web crawling.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the FirecrawlTools toolkit.
        
        Args:
            api_key (str, optional): FireCrawl API key. If None, uses FIRECRAWL_API_KEY environment variable.
        """
        super().__init__(name="firecrawl_tools")
        
        # Get API key from environment variable if not provided
        if api_key is None:
            api_key = os.environ.get("FIRECRAWL_API_KEY")
            if not api_key:
                raise ValueError(
                    "No API key provided. Either pass api_key parameter or set FIRECRAWL_API_KEY environment variable."
                )
        
        self.api_key = api_key
        self.client = FirecrawlApp(api_key=self.api_key)
        
        # Register the methods that can be called by the agent
        self.register(self.deep_research)
        self.register(self.scrape_webpage)
        self.register(self.map_website)
    
    def _create_activity_callback(self) -> Callable:
        """
        Create a callback function for real-time updates that logs to Agno logger.
        
        Returns:
            Callable: A callback function that logs FireCrawl activities.
        """
        def on_activity(activity):
            activity_type = activity.get('type', 'UNKNOWN')
            message = activity.get('message', 'No message')
            logger.info(f"[FireCrawl {activity_type}] {message}")
        
        return on_activity
    
    def deep_research(self, 
                      query: str, 
                      max_depth: int = 5, 
                      time_limit: int = 180, 
                      max_urls: int = 15) -> str:
        """
        Perform deep research on a topic using FireCrawl's capabilities.
        
        Args:
            query (str): The research query to investigate.
            max_depth (int, optional): Number of research iterations (1-10).
            time_limit (int, optional): Time limit in seconds (30-300).
            max_urls (int, optional): Maximum URLs to analyze (1-1000).
            
        Returns:
            str: Formatted research results as Markdown.
        """
        logger.info(f"Starting deep research on: {query}")
        
        # Define research parameters
        params = {
            "maxDepth": max_depth,
            "timeLimit": time_limit,
            "maxUrls": max_urls
        }
        
        try:
            # Run deep research with activity callback
            results = self.client.deep_research(
                query=query,
                params=params,
                on_activity=self._create_activity_callback()
            )
            
            logger.info(f"Deep research completed with {len(results['data']['sources'])} sources")
            
            # Format the results as Markdown string
            sources = results['data']['sources']
            
            formatted_output = ["## Research Results on: " + query + "\n"]
            formatted_output.append(results['data']['finalAnalysis'])
            
            if sources:
                formatted_output.append("\n\n## Sources\n")
                for i, source in enumerate(sources, 1):
                    url = source.get("url", "No URL")
                    title = source.get("title", "No title")
                    formatted_output.append(f"{i}. [{title}]({url})")
            
            return "\n".join(formatted_output)
            
        except Exception as e:
            logger.warning(f"Failed to perform deep research: {e}")
            return f"Error performing research on '{query}': {e}"
    
    def scrape_webpage(self, 
                       url: str, 
                       only_main_content: bool = True, 
                       mobile: bool = False) -> str:
        """
        Scrape content from a single webpage.
        
        Args:
            url (str): The URL to scrape.
            only_main_content (bool, optional): Extract only the main content, filtering out navigation, etc.
            mobile (bool, optional): Use mobile viewport for scraping.
            
        Returns:
            str: Scraped content in Markdown format.
        """
        logger.info(f"Scraping webpage: {url}")
        
        try:
            # Set up scraping options
            options = {
                "formats": ["markdown"],
                "onlyMainContent": only_main_content,
                "mobile": mobile
            }
            
            # Scrape the webpage
            result = self.client.scrape(url=url, **options)
            
            logger.info(f"Successfully scraped {url}")
            
            # Format as Markdown
            title = result.get("title", "Scraped Content")
            content = result.get("markdown", "No content extracted")
            
            formatted_output = [
                f"# {title}\n",
                f"Source: {url}\n",
                content
            ]
            
            return "\n".join(formatted_output)
            
        except Exception as e:
            logger.warning(f"Failed to scrape webpage: {e}")
            return f"Error scraping webpage '{url}': {e}"
    
    def map_website(self, 
                    url: str, 
                    limit: int = 100, 
                    include_subdomains: bool = False) -> str:
        """
        Discover URLs from a starting point on a website.
        
        Args:
            url (str): Starting URL for URL discovery.
            limit (int, optional): Maximum number of URLs to return.
            include_subdomains (bool, optional): Include URLs from subdomains in results.
            
        Returns:
            str: Formatted list of discovered URLs as Markdown.
        """
        logger.info(f"Mapping website: {url}")
        
        try:
            # Map the website
            result = self.client.map(
                url=url,
                limit=limit,
                includeSubdomains=include_subdomains
            )
            
            logger.info(f"Successfully mapped {url}, found {len(result)} URLs")
            
            # Format as Markdown
            formatted_output = [
                f"# Website Map: {url}\n",
                f"Found {len(result)} URLs\n",
                "## Discovered URLs:\n"
            ]
            
            for i, discovered_url in enumerate(result, 1):
                formatted_output.append(f"{i}. {discovered_url}")
            
            return "\n".join(formatted_output)
            
        except Exception as e:
            logger.warning(f"Failed to map website: {e}")
            return f"Error mapping website '{url}': {e}"


# Example usage with Agno Agent
if __name__ == "__main__":
    # Set your API key in environment variable before running
    # os.environ["FIRECRAWL_API_KEY"] = "your-api-key-here"
    
    # For demonstration purposes, you can also set the API key directly
    # api_key = "your-api-key-here"
    # firecrawl_tools = FirecrawlTools(api_key=api_key)
    
    # Or use the environment variable (recommended)
    firecrawl_tools = FirecrawlTools(api_key="api_key")
    
    # Create an Agno agent with the FireCrawl toolkit
    agent = Agent(
        tools=[firecrawl_tools],
        show_tool_calls=True,
        markdown=True,
    )
    
    # Example query
    agent.print_response("Research the current trends in artificial intelligence and summarize the key developments.") 