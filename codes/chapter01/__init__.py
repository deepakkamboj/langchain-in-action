"""
Chapter 1 Code Examples - LangChain Agent Development

This package contains all code examples for Chapter 1:
- ch01_01_basic_agent.py: Basic LangChain agent following official quickstart
- ch01_02_production_agent.py: Production-ready agent with advanced features
- ch01_03_openai_agent.py: OpenAI-based implementation for comparison
- ch01_04_testing_framework.py: Comprehensive testing and evaluation framework

Usage:
    python ch01_01_basic_agent.py          # Run basic agent demo
    python ch01_02_production_agent.py     # Run production agent demo  
    python ch01_03_openai_agent.py         # Run OpenAI agent comparison
    python ch01_04_testing_framework.py    # Run comprehensive testing

Requirements:
    pip install langchain langchain-openai langchain-anthropic langgraph python-dotenv

Environment Variables:
    OPENAI_API_KEY=your_openai_key          # For OpenAI models
    ANTHROPIC_API_KEY=your_anthropic_key    # For Claude models
    LANGCHAIN_API_KEY=your_langsmith_key    # For observability (optional)
    LANGCHAIN_TRACING_V2=true               # Enable tracing (optional)
"""

__version__ = "1.0.0"
__author__ = "LangChain in Action"
