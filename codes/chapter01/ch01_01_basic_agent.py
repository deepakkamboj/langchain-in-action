"""
File: ch01_01_basic_agent.py
Purpose: Basic LangChain agent following official quickstart example
Chapter: Chapter 1 - Building Your First LangChain Agent
Requirements: langchain, langchain-anthropic
"""

from shared.logging_utils import AgentLogger
from shared.config import config
from langchain.agents import create_agent
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


def create_basic_agent():
    """Create the basic agent from LangChain quickstart."""

    # Validate Anthropic configuration
    try:
        config.validate_anthropic()
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("Please set ANTHROPIC_API_KEY environment variable")
        return None

    # Create agent with Claude Sonnet 4.5 (as recommended in docs)
    agent = create_agent(
        model="anthropic:claude-sonnet-4-5",
        tools=[get_weather],
        system_prompt="You are a helpful assistant",
    )

    return agent


def run_basic_agent_demo():
    """Demonstrate basic agent capabilities."""

    print("🤖 Creating Basic LangChain Agent")
    print("=" * 50)

    # Create the agent
    agent = create_basic_agent()
    if not agent:
        return

    # Set up logging
    logger = AgentLogger("basic_agent")

    # Test queries
    test_queries = [
        "what is the weather in sf",
        "How's the weather in New York?",
        "Tell me about the weather in London"
    ]

    print(f"Testing {len(test_queries)} queries...\n")

    for i, query in enumerate(test_queries, 1):
        print(f"Query {i}: {query}")
        print("-" * 30)

        try:
            # Log the interaction
            logger.log_agent_step("USER_QUERY", query)

            # Run the agent
            response = agent.invoke({
                "messages": [{"role": "user", "content": query}]
            })

            # Extract and display response
            if isinstance(response, dict) and 'messages' in response:
                # Handle new format
                agent_response = response['messages'][-1]['content']
            else:
                # Handle other formats
                agent_response = str(response)

            print(f"🤖 Agent Response: {agent_response}")
            logger.log_agent_step("AGENT_RESPONSE", agent_response)

        except Exception as e:
            print(f"❌ Error: {e}")
            logger.log_agent_step("ERROR", str(e))

        print("\n" + "="*50 + "\n")

    # Print summary
    summary = logger.get_conversation_summary()
    print("📊 Session Summary:")
    print(f"   Total steps: {summary['total_steps']}")
    print(
        f"   Successful interactions: {len([log for log in summary['conversation_log'] if log['step_type'] == 'AGENT_RESPONSE'])}")


if __name__ == "__main__":
    # Enable tracing if configured
    if config.langchain_tracing_v2:
        config.enable_tracing()
        print("🔍 LangSmith tracing enabled")

    run_basic_agent_demo()
