"""
File: ch01_03_openai_agent.py
Purpose: Alternative agent implementation using OpenAI for comparison
Chapter: Chapter 1 - Building Your First LangChain Agent
Requirements: langchain, langchain-openai
"""

from shared.logging_utils import AgentLogger, monitor_performance
from shared.config import config
import time
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.agents import tool, create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))


@tool
def simple_calculator(expression: str) -> str:
    """Evaluate basic mathematical expressions.

    Args:
        expression: Mathematical expression like '25 * 4 + 10' or '100 / 5'

    Returns:
        String containing the calculation result
    """
    try:
        # Safe evaluation for basic math (replace ^ with ** for exponents)
        safe_expression = expression.replace('^', '**')
        result = eval(safe_expression)
        return f"The result is: {result}"
    except Exception as e:
        return f"Error calculating '{expression}': {str(e)}"


@tool
def get_word_count(text: str) -> str:
    """Count words in a text string.

    Args:
        text: The text string to analyze

    Returns:
        String containing word count information
    """
    if not text.strip():
        return "The text is empty - 0 words."

    word_count = len(text.split())
    char_count = len(text)
    return f"The text '{text}' contains {word_count} words and {char_count} characters."


@tool
def get_current_timestamp() -> str:
    """Get the current timestamp.

    Returns:
        String containing current date and time
    """
    from datetime import datetime
    now = datetime.now()
    return f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}"


def create_openai_agent(with_memory: bool = False):
    """Create an OpenAI-based agent with optional memory."""

    # Validate OpenAI configuration
    try:
        config.validate_openai()
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("Please set OPENAI_API_KEY environment variable")
        return None

    # Create OpenAI LLM
    model_config = config.get_model_config("gpt-4")
    llm = ChatOpenAI(
        model=model_config["model"],
        temperature=model_config["temperature"],
        max_tokens=model_config["max_tokens"],
        request_timeout=model_config["timeout"]
    )

    # Define available tools
    tools = [simple_calculator, get_word_count, get_current_timestamp]

    # Create ReAct prompt template
    if with_memory:
        template = """Answer questions using available tools when needed.

Previous conversation:
{chat_history}

Tools available:
{tools}

Use this format:
Question: the input question
Thought: think about what to do
Action: choose from [{tool_names}]
Action Input: tool input
Observation: tool result
... (repeat Thought/Action/Observation as needed)
Thought: I know the final answer
Final Answer: complete answer

Question: {input}
Thought: {agent_scratchpad}"""
    else:
        template = """Answer questions using available tools when needed.

Tools available:
{tools}

Use this format:
Question: the input question
Thought: think about what to do
Action: choose from [{tool_names}]
Action Input: tool input
Observation: tool result
... (repeat Thought/Action/Observation as needed)
Thought: I know the final answer
Final Answer: complete answer

Question: {input}
Thought: {agent_scratchpad}"""

    prompt = PromptTemplate.from_template(template)

    # Create ReAct agent
    agent = create_react_agent(llm, tools, prompt)

    # Create agent executor with optional memory
    if with_memory:
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            memory=memory,
            verbose=True,
            max_iterations=5,
            handle_parsing_errors=True
        )
    else:
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            max_iterations=5,
            handle_parsing_errors=True
        )

    return agent_executor


@monitor_performance("agent_query_processing")
def process_agent_query(agent, query: str, logger: AgentLogger) -> dict:
    """Process a single agent query with monitoring."""

    logger.log_agent_step("USER_QUERY", query)

    start_time = time.time()
    response = agent.invoke({"input": query})
    duration = time.time() - start_time

    logger.log_llm_interaction(query, response['output'], duration)

    return response


def run_openai_agent_demo():
    """Demonstrate OpenAI agent capabilities."""

    print("🔗 Creating OpenAI-Based LangChain Agent")
    print("=" * 50)

    # Create agent without memory first
    agent = create_openai_agent(with_memory=False)
    if not agent:
        return

    # Set up logging
    logger = AgentLogger("openai_agent")

    # Test queries demonstrating different tool usage
    test_queries = [
        "What is 15 * 24?",
        "How many words are in 'LangChain is awesome for building agents'?",
        "What time is it now?",
        "Calculate (100 + 50) / 3 and tell me how many words are in 'Hello World'",
        "What is the square root of 144? Use 144 ** 0.5"
    ]

    print(f"Testing {len(test_queries)} queries...\n")

    for i, query in enumerate(test_queries, 1):
        print(f"Query {i}: {query}")
        print("-" * 40)

        try:
            response = process_agent_query(agent, query, logger)
            print(f"🤖 Final Answer: {response['output']}")

        except Exception as e:
            print(f"❌ Error: {e}")
            logger.log_agent_step("ERROR", str(e))

        print("\n" + "="*50 + "\n")

    # Print summary
    summary = logger.get_conversation_summary()
    performance = logger.get_performance_summary()

    print("📊 OpenAI Agent Session Summary:")
    print(f"   Total steps: {summary['total_steps']}")
    print(f"   Tool executions: {summary['tool_executions']}")
    print(
        f"   Average response time: {summary['total_duration_ms']/summary['total_steps']:.0f}ms")

    if performance:
        print("\n🔧 Tool Performance:")
        for tool_name, metrics in performance.items():
            print(f"   {tool_name}: {metrics['total_calls']} calls, "
                  f"{metrics['average_duration_ms']}ms avg")


def run_memory_comparison_demo():
    """Compare agent behavior with and without memory."""

    print("\n🧠 Memory Comparison Demo")
    print("=" * 40)

    # Test without memory
    print("1. Agent WITHOUT Memory:")
    agent_no_memory = create_openai_agent(with_memory=False)
    if agent_no_memory:
        response1 = agent_no_memory.invoke(
            {"input": "My favorite number is 42"})
        print(f"Agent: {response1['output'][:100]}...")

        response2 = agent_no_memory.invoke(
            {"input": "What was my favorite number?"})
        print(f"Agent: {response2['output'][:100]}...")

    print("\n2. Agent WITH Memory:")
    agent_with_memory = create_openai_agent(with_memory=True)
    if agent_with_memory:
        response1 = agent_with_memory.invoke(
            {"input": "My favorite number is 42"})
        print(f"Agent: {response1['output'][:100]}...")

        response2 = agent_with_memory.invoke(
            {"input": "What was my favorite number?"})
        print(f"Agent: {response2['output'][:100]}...")


def compare_agent_approaches():
    """Compare different agent implementation approaches."""

    print("\n⚖️  Agent Implementation Comparison")
    print("=" * 50)

    comparison_data = [
        {
            "Aspect": "Setup Complexity",
            "Basic LangChain": "Very Simple (3 lines)",
            "OpenAI Implementation": "Moderate (15-20 lines)",
            "Production Agent": "Complex (50+ lines)"
        },
        {
            "Aspect": "Memory Support",
            "Basic LangChain": "Built-in with checkpointer",
            "OpenAI Implementation": "Manual implementation",
            "Production Agent": "Advanced with persistence"
        },
        {
            "Aspect": "Structured Output",
            "Basic LangChain": "Native support",
            "OpenAI Implementation": "Requires parsing",
            "Production Agent": "Full schema validation"
        },
        {
            "Aspect": "Observability",
            "Basic LangChain": "Automatic tracing",
            "OpenAI Implementation": "Manual logging",
            "Production Agent": "Complete monitoring"
        },
        {
            "Aspect": "Best Use Case",
            "Basic LangChain": "Quick prototypes",
            "OpenAI Implementation": "Learning & flexibility",
            "Production Agent": "Production systems"
        }
    ]

    # Print comparison table
    print(f"{'Aspect':<20} {'Basic LangChain':<25} {'OpenAI Impl':<20} {'Production Agent':<25}")
    print("-" * 90)

    for row in comparison_data:
        print(f"{row['Aspect']:<20} {row['Basic LangChain']:<25} {row['OpenAI Implementation']:<20} {row['Production Agent']:<25}")


if __name__ == "__main__":
    # Enable tracing if configured
    if config.langchain_tracing_v2:
        config.enable_tracing()
        print("🔍 LangSmith tracing enabled")

    # Run OpenAI agent demo
    run_openai_agent_demo()

    # Demonstrate memory comparison
    run_memory_comparison_demo()

    # Show comparison of approaches
    compare_agent_approaches()
