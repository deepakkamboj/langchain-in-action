"""
File: ch01_04_testing_framework.py
Purpose: Comprehensive testing framework for LangChain agents
Chapter: Chapter 1 - Building Your First LangChain Agent
Requirements: pytest, langchain
"""

from ch01_03_openai_agent import create_openai_agent
from ch01_02_production_agent import create_production_agent, Context
from ch01_01_basic_agent import create_basic_agent
from shared.logging_utils import AgentLogger
from shared.test_helpers import AgentTestSuite, TestCase
from shared.config import config
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))


# Import our agent implementations


def create_comprehensive_test_cases():
    """Create comprehensive test cases for agent evaluation."""

    return [
        TestCase(
            name="Basic Weather Query",
            input="What's the weather in San Francisco?",
            expected_contains=["sunny", "San Francisco"],
            max_execution_time=10.0,
            metadata={"category": "weather", "complexity": "basic"}
        ),
        TestCase(
            name="Simple Math Calculation",
            input="What is 25 * 4?",
            expected_contains=["100"],
            should_use_tools=["simple_calculator"],
            max_execution_time=5.0,
            metadata={"category": "calculation", "complexity": "basic"}
        ),
        TestCase(
            name="Text Analysis",
            input="How many words are in 'LangChain is amazing'?",
            expected_contains=["3", "words"],
            should_use_tools=["get_word_count"],
            max_execution_time=5.0,
            metadata={"category": "text_analysis", "complexity": "basic"}
        ),
        TestCase(
            name="Multi-step Query",
            input="Calculate 15 * 8 and tell me how many words are in 'Hello World'",
            expected_contains=["120", "2", "words"],
            should_use_tools=["simple_calculator", "get_word_count"],
            max_execution_time=15.0,
            metadata={"category": "multi_step", "complexity": "medium"}
        ),
        TestCase(
            name="Contextual Weather Query",
            input="What's the weather where I am?",
            expected_contains=["weather"],
            max_execution_time=10.0,
            metadata={"category": "weather", "complexity": "contextual"}
        ),
        TestCase(
            name="Complex Mathematical Expression",
            input="What is (100 + 50) / 3?",
            expected_contains=["50"],
            should_use_tools=["simple_calculator"],
            max_execution_time=8.0,
            metadata={"category": "calculation", "complexity": "medium"}
        ),
        TestCase(
            name="Current Time Query",
            input="What time is it now?",
            expected_contains=["time", "current"],
            should_use_tools=["get_current_timestamp"],
            max_execution_time=5.0,
            metadata={"category": "utility", "complexity": "basic"}
        )
    ]


def test_basic_agent():
    """Test the basic LangChain agent implementation."""

    print("🧪 Testing Basic LangChain Agent")
    print("=" * 40)

    # Create agent
    agent = create_basic_agent()
    if not agent:
        print("❌ Failed to create basic agent - skipping tests")
        return None

    # Create test suite with simplified test cases for basic agent
    basic_test_cases = [
        TestCase(
            name="Simple Weather Query",
            input="what is the weather in sf",
            expected_contains=["sunny", "sf"],
            max_execution_time=15.0
        ),
        TestCase(
            name="Different City Weather",
            input="How's the weather in New York?",
            expected_contains=["sunny", "New York"],
            max_execution_time=15.0
        ),
        TestCase(
            name="Generic Weather Query",
            input="Tell me about the weather",
            expected_contains=["weather"],
            max_execution_time=15.0
        )
    ]

    # Wrap agent to match expected interface
    class BasicAgentWrapper:
        def __init__(self, agent):
            self.agent = agent

        def invoke(self, inputs):
            response = self.agent.invoke({
                "messages": [{"role": "user", "content": inputs["input"]}]
            })
            # Extract response content
            if isinstance(response, dict) and 'messages' in response:
                output = response['messages'][-1]['content']
            else:
                output = str(response)
            return {"output": output}

    wrapped_agent = BasicAgentWrapper(agent)
    test_suite = AgentTestSuite(wrapped_agent, "Basic Agent Tests")

    return test_suite.run_test_suite(basic_test_cases)


def test_production_agent():
    """Test the production-ready agent implementation."""

    print("🧪 Testing Production LangChain Agent")
    print("=" * 40)

    # Create agent
    agent, checkpointer = create_production_agent()
    if not agent:
        print("❌ Failed to create production agent - skipping tests")
        return None

    # Create test cases for production agent
    production_test_cases = [
        TestCase(
            name="Contextual Weather Query",
            input="what is the weather outside?",
            expected_contains=["weather"],
            max_execution_time=20.0
        ),
        TestCase(
            name="Specific Location Weather",
            input="How's the weather in Paris?",
            expected_contains=["sunny", "Paris"],
            max_execution_time=15.0
        ),
        TestCase(
            name="Conversational Follow-up",
            input="thank you!",
            expected_contains=["welcome"],
            max_execution_time=10.0
        )
    ]

    # Wrap production agent to match expected interface
    class ProductionAgentWrapper:
        def __init__(self, agent):
            self.agent = agent

        def invoke(self, inputs):
            config_dict = {"configurable": {"thread_id": "test_thread"}}
            user_context = Context(user_id="1")

            response = self.agent.invoke(
                {"messages": [{"role": "user", "content": inputs["input"]}]},
                config=config_dict,
                context=user_context
            )

            # Extract response
            if 'structured_response' in response:
                output = response['structured_response'].punny_response
            else:
                output = str(response)

            return {"output": output}

    wrapped_agent = ProductionAgentWrapper(agent)
    test_suite = AgentTestSuite(wrapped_agent, "Production Agent Tests")

    return test_suite.run_test_suite(production_test_cases)


def test_openai_agent():
    """Test the OpenAI-based agent implementation."""

    print("🧪 Testing OpenAI LangChain Agent")
    print("=" * 40)

    # Create agent
    agent = create_openai_agent(with_memory=False)
    if not agent:
        print("❌ Failed to create OpenAI agent - skipping tests")
        return None

    # Use comprehensive test cases for OpenAI agent
    test_cases = create_comprehensive_test_cases()

    test_suite = AgentTestSuite(agent, "OpenAI Agent Tests")
    return test_suite.run_test_suite(test_cases)


def run_performance_comparison():
    """Compare performance across different agent implementations."""

    print("\n📊 Agent Performance Comparison")
    print("=" * 50)

    results = {}

    # Test each agent type
    test_functions = [
        ("Basic Agent", test_basic_agent),
        ("Production Agent", test_production_agent),
        ("OpenAI Agent", test_openai_agent)
    ]

    for agent_name, test_func in test_functions:
        try:
            result = test_func()
            if result:
                results[agent_name] = result
        except Exception as e:
            print(f"❌ Failed to test {agent_name}: {e}")
            results[agent_name] = None

    # Display comparison
    print("\n🏆 Performance Summary:")
    print(f"{'Agent Type':<18} {'Success Rate':<12} {'Avg Time':<10} {'Total Tests':<12}")
    print("-" * 55)

    for agent_name, result in results.items():
        if result:
            success_rate = f"{result['success_rate']:.1f}%"
            avg_time = f"{result['average_execution_time']:.2f}s"
            total_tests = str(result['total_tests'])
        else:
            success_rate = "N/A"
            avg_time = "N/A"
            total_tests = "N/A"

        print(f"{agent_name:<18} {success_rate:<12} {avg_time:<10} {total_tests:<12}")

    return results


def run_agent_stress_test():
    """Run stress tests to evaluate agent reliability under load."""

    print("\n🔥 Agent Stress Test")
    print("=" * 30)

    # Create OpenAI agent for stress testing
    agent = create_openai_agent(with_memory=False)
    if not agent:
        print("❌ No agent available for stress testing")
        return

    # Create repeated test cases
    stress_test_cases = []
    base_queries = [
        "What is 10 + 10?",
        "How many words in 'test'?",
        "What time is it?",
        "Calculate 5 * 5"
    ]

    # Create 20 test cases (5 of each query)
    for i in range(5):
        for j, query in enumerate(base_queries):
            stress_test_cases.append(TestCase(
                name=f"Stress_Test_{i}_{j}",
                input=query,
                max_execution_time=30.0,
                metadata={"stress_test": True, "iteration": i}
            ))

    # Run stress test
    test_suite = AgentTestSuite(agent, "Agent Stress Test")

    print(f"Running {len(stress_test_cases)} stress test cases...")
    start_time = time.time()

    results = test_suite.run_test_suite(stress_test_cases)

    total_time = time.time() - start_time

    print(f"\n🎯 Stress Test Results:")
    print(f"   Total time: {total_time:.2f}s")
    print(f"   Tests per second: {len(stress_test_cases)/total_time:.2f}")
    print(f"   Success rate: {results['success_rate']:.1f}%")

    return results


if __name__ == "__main__":
    import time

    print("🧪 LangChain Agent Testing Framework")
    print("=" * 60)

    # Enable tracing if configured
    if config.langchain_tracing_v2:
        config.enable_tracing()
        print("🔍 LangSmith tracing enabled")

    # Run performance comparison
    comparison_results = run_performance_comparison()

    # Run stress test
    stress_results = run_agent_stress_test()

    # Save results
    if comparison_results:
        print(f"\n💾 Test results available for analysis")
        print(
            f"   Performance comparison: {len(comparison_results)} agent types tested")
        if stress_results:
            print(
                f"   Stress test: {stress_results['total_tests']} cases completed")

    print("\n✅ Testing framework demonstration complete!")
