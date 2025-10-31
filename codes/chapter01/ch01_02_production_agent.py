"""
File: ch01_02_production_agent.py
Purpose: Production-ready LangChain agent following real-world example from docs
Chapter: Chapter 1 - Building Your First LangChain Agent
Requirements: langchain, langchain-anthropic, langgraph
"""

from shared.logging_utils import AgentLogger, error_handling_context
from shared.config import config
from typing import Any
from dataclasses import dataclass
from langgraph.checkpoint.memory import InMemorySaver
from langchain.chat_models import init_chat_model
from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))


# System prompt defines agent behavior (keep it specific and actionable)
SYSTEM_PROMPT = """You are an expert weather forecaster, who speaks in puns.

You have access to two tools:

- get_weather_for_location: use this to get the weather for a specific location
- get_user_location: use this to get the user's location

If a user asks you for the weather, make sure you know the location. If you can tell from the question that they mean wherever they are, use the get_user_location tool to find their location."""


@tool
def get_weather_for_location(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


@dataclass
class Context:
    """Custom runtime context schema."""
    user_id: str


@tool
def get_user_location(runtime: ToolRuntime[Context, Any]) -> str:
    """Retrieve user information based on user ID."""
    user_id = runtime.context.user_id
    return "Florida" if user_id == "1" else "SF"


@dataclass
class ResponseFormat:
    """Response schema for the agent."""
    # A punny response (always required)
    punny_response: str
    # Any interesting information about the weather if available
    weather_conditions: str | None = None


def create_production_agent():
    """Create a production-ready agent with all advanced features."""

    # Validate Anthropic configuration
    try:
        config.validate_anthropic()
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("Please set ANTHROPIC_API_KEY environment variable")
        return None, None

    # Set up language model with the right parameters for your use case
    model = init_chat_model(
        "anthropic:claude-sonnet-4-5",
        temperature=0.5,     # Balanced creativity vs consistency
        timeout=10,          # Request timeout in seconds
        max_tokens=1000      # Limit response length
    )

    # Add memory to maintain state across interactions
    checkpointer = InMemorySaver()

    # Assemble the complete production agent
    agent = create_agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=[get_user_location, get_weather_for_location],
        context_schema=Context,
        response_format=ResponseFormat,
        checkpointer=checkpointer
    )

    return agent, checkpointer


def run_production_agent_demo():
    """Demonstrate production agent capabilities with advanced features."""

    print("🚀 Creating Production-Ready LangChain Agent")
    print("=" * 60)

    # Create the agent
    agent, checkpointer = create_production_agent()
    if not agent:
        return

    # Set up logging
    logger = AgentLogger("production_agent")

    # Configure conversation thread
    config_dict = {"configurable": {"thread_id": "demo_thread_1"}}
    user_context = Context(user_id="1")

    # Test scenarios demonstrating production features
    test_scenarios = [
        {
            "name": "Weather Query with Context",
            "query": "what is the weather outside?",
            "description": "Tests tool usage and context integration"
        },
        {
            "name": "Follow-up Conversation",
            "query": "thank you!",
            "description": "Tests memory and conversation continuity"
        },
        {
            "name": "Specific Location Query",
            "query": "How's the weather in Paris?",
            "description": "Tests direct location handling"
        },
        {
            "name": "Conversation Context",
            "query": "What was my first question?",
            "description": "Tests memory recall across interactions"
        }
    ]

    print(f"Running {len(test_scenarios)} production scenarios...\n")

    for i, scenario in enumerate(test_scenarios, 1):
        print(f"Scenario {i}: {scenario['name']}")
        print(f"Description: {scenario['description']}")
        print(f"Query: {scenario['query']}")
        print("-" * 50)

        try:
            with error_handling_context(f"Scenario_{i}", logger):
                # Log the interaction
                logger.log_agent_step("USER_QUERY", scenario['query'], {
                    "scenario": scenario['name'],
                    "thread_id": config_dict["configurable"]["thread_id"],
                    "user_id": user_context.user_id
                })

                # Run the agent with context
                response = agent.invoke(
                    {"messages": [
                        {"role": "user", "content": scenario['query']}]},
                    config=config_dict,
                    context=user_context
                )

                # Extract structured response
                if 'structured_response' in response:
                    structured_resp = response['structured_response']

                    print(
                        f"🎭 Punny Response: {structured_resp.punny_response}")
                    if structured_resp.weather_conditions:
                        print(
                            f"🌤️  Weather: {structured_resp.weather_conditions}")

                    logger.log_agent_step("STRUCTURED_RESPONSE", "Response generated", {
                        "punny_response": structured_resp.punny_response,
                        "weather_conditions": structured_resp.weather_conditions
                    })
                else:
                    print(f"🤖 Response: {response}")
                    logger.log_agent_step("AGENT_RESPONSE", str(response))

        except Exception as e:
            print(f"❌ Error in scenario {i}: {e}")
            logger.log_agent_step("ERROR", str(
                e), {"scenario": scenario['name']})

        print("\n" + "="*60 + "\n")

    # Print comprehensive summary
    summary = logger.get_conversation_summary()
    print("📊 Production Agent Session Summary:")
    print(f"   Total steps: {summary['total_steps']}")
    print(f"   Tool executions: {summary['tool_executions']}")
    print(f"   LLM interactions: {summary['llm_interactions']}")
    if summary['tools_used']:
        print(f"   Tools used: {', '.join(summary['tools_used'])}")

    # Display performance metrics
    performance = logger.get_performance_summary()
    if performance:
        print("\n🔧 Tool Performance:")
        for tool_name, metrics in performance.items():
            print(f"   {tool_name}: {metrics['total_calls']} calls, "
                  f"{metrics['success_rate']}% success rate, "
                  f"{metrics['average_duration_ms']}ms avg")


def demonstrate_memory_persistence():
    """Demonstrate conversation memory across multiple sessions."""

    print("\n🧠 Testing Memory Persistence")
    print("=" * 40)

    agent, _ = create_production_agent()
    if not agent:
        return

    # Use the same thread ID to maintain conversation history
    thread_id = "persistent_memory_demo"
    config_dict = {"configurable": {"thread_id": thread_id}}
    user_context = Context(user_id="2")  # Different user

    # First conversation
    print("Session 1:")
    response1 = agent.invoke(
        {"messages": [
            {"role": "user", "content": "I live in Seattle, what's the weather?"}]},
        config=config_dict,
        context=user_context
    )
    print(f"Agent: {response1.get('structured_response', response1)}")

    # Second conversation - should remember context
    print("\nSession 2 (same thread):")
    response2 = agent.invoke(
        {"messages": [
            {"role": "user", "content": "Is it usually this nice here?"}]},
        config=config_dict,
        context=user_context
    )
    print(f"Agent: {response2.get('structured_response', response2)}")


if __name__ == "__main__":
    # Enable tracing if configured
    if config.langchain_tracing_v2:
        config.enable_tracing()
        print("🔍 LangSmith tracing enabled")

    # Run main demo
    run_production_agent_demo()

    # Demonstrate memory persistence
    demonstrate_memory_persistence()
