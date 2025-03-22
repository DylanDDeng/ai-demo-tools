# AI Agent & LLM Demo Tools 🤖🔍💡

This repository contains a series of demos I write about **Agent**, **RAG** and **LLMs**. There maybe some errors in this repository, because I learn this all by myself. So, if you find any bugs, or errors, please make an issue to tell me. 

I hope this repository can also help you if you get any idea from this. 

Thanks to Shubham for his [awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps)

## Repository Structure

The repository consists of three main modules, each focused on different aspects of AI applications:

### 01-media-generator 🎨
Tools for creating and processing multimedia content using generative AI.

- **Functionality**: Image generation and processing using Gemini API and Replicate
- **Technology**: Streamlit interface, multimodal generation, text-to-image conversion
- **Files**:
  - `01-workflow.py` - Main workflow and interface
  - `README.md` - Module description and dependencies

### 02-Mistral-Small 👁️
A multimodal chatbot based on Mistral AI, focusing on image analysis and understanding.

- **Functionality**: Upload and analyze images, support for image-based Q&A
- **Technology**: Mistral AI models, multimodal understanding, context-aware conversation
- **Files**:
  - `mistral_image_chatbot.py` - Main Streamlit application
  - `test_mistral_small.py` - Mistral API test script
  - `requirements.txt` - Dependency package list

### 03-financial-agent 📊
A cryptocurrency research and analysis system based on multi-agent collaboration, demonstrating the capabilities of agent teams.

- **Functionality**: Conduct in-depth research on cryptocurrencies and provide investment advice
- **Technology**: Agno framework, multi-agent collaboration, web retrieval, content generation
- **Files**:
  - `crypto_financial_agent.py` - Main application
  - `firecrawl_tool.py` - Web crawling and research tools
  - `perplexity_tool.py` - Information retrieval tool based on Perplexity

## Technical Highlights

This repository showcases several key AI technology concepts and practices that I've been learning:

- **Multi-Agent Systems** - Demonstrates how AI agents with different specialties can work together to solve complex problems
- **Tool Usage** - Shows how LLMs can use external tools (such as search engines, web scraping tools) to enhance their capabilities
- **RAG Implementation** - Implements Retrieval-Augmented Generation through Perplexity and FireCrawl tools
- **Multimodal Understanding** - Utilizes Mistral and Gemini models to process images and text
- **Structured Output** - Generates structured data through clear formatting requirements

## Installation Guide

### Global Dependencies

```bash
pip install openai agno streamlit replicate
```

### Module-Specific Dependencies

#### Media Generator
```bash
pip install streamlit replicate
```

#### Mistral Chatbot
```bash
pip install -r 02-Mistral-Small/requirements.txt
```

#### Financial Analysis Agent
```bash
pip install agno openai
```

## Usage

### Media Generator
```bash
cd 01-media-generator
streamlit run 01-workflow.py
```

### Mistral Image Chatbot
```bash
cd 02-Mistral-Small
streamlit run mistral_image_chatbot.py
```

### Cryptocurrency Analysis Agent
```bash
python 03-financial-agent/crypto_financial_agent.py --crypto bitcoin --google-api-key <YOUR_API_KEY> --firecrawl-api-key <YOUR_API_KEY> --perplexity-api-key <YOUR_API_KEY>
```

## API Key Requirements

To run these projects, you need to obtain the following API keys:

- **Gemini API Key** - Google's Gemini model API
- **Mistral API Key** - Mistral AI platform
- **FireCrawl API Key** - Web scraping and content analysis
- **Perplexity API Key** - Information retrieval and question answering
- **Replicate API Key** - For image generation

## Learning Resources

These demos represent my learning journey through the following concepts:

- **Agent Frameworks** - How to build and organize AI agent systems
- **RAG Architecture** - Practical implementation of retrieval-augmented generation
- **LLM Prompt Engineering** - Examples of effective prompting in different scenarios
- **Multimodal Applications** - Comprehensive applications handling text and images
- **Tool-Enhanced LLMs** - Extending model capabilities using external tools

## Future Improvements

I'm always looking to improve this repository. Some ideas I'm considering:

- Add more agent examples for specialized domains
- Implement RAG systems with local knowledge bases
- Add support for multiple languages
- Create more user-friendly UI interfaces
- Integrate more data sources and tools

---

Contributions and feedback are highly appreciated! This repository documents my learning journey with AI Agent and LLM technologies - I hope it can be useful for your learning as well.