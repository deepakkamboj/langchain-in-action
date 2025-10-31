"""
File: test_helpers.py
Purpose: Testing utilities and helpers for LangChain agent development
Chapter: Shared utilities across all chapters
Requirements: pytest, unittest, langchain
"""

import pytest
import time
import json
from typing import List, Dict, Any, Optional
from unittest.mock import Mock, patch
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TestCase:
    """Structure for agent test cases."""
    name: str
    input: str
    expected_contains: Optional[List[str]] = None
    expected_exact: Optional[str] = None
    should_use_tools: Optional[List[str]] = None
    max_execution_time: float = 30.0
    metadata: Optional[Dict[str, Any]] = None


class AgentTestSuite:
    """Comprehensive testing suite for LangChain agents."""

    def __init__(self, agent_executor, test_name: str = "AgentTest"):
        self.agent = agent_executor
        self.test_name = test_name
        self.test_results = []
        self.performance_metrics = {}

    def run_single_test(self, test_case: TestCase) -> Dict[str, Any]:
        """Run a single test case and return comprehensive results."""
        start_time = time.time()
        result = {
            "test_name": test_case.name,
            "input": test_case.input,
            "status": "UNKNOWN",
            "error": None,
            "execution_time": 0,
            "agent_response": None,
            "tools_used": [],
            "validation_results": {}
        }

        try:
            # Execute the agent
            response = self.agent.invoke({"input": test_case.input})
            execution_time = time.time() - start_time

            result.update({
                "execution_time": execution_time,
                "agent_response": response.get("output", response),
                "status": "EXECUTED"
            })

            # Extract tools used if available
            if hasattr(response, 'intermediate_steps'):
                result["tools_used"] = [
                    step[0].tool for step in response.intermediate_steps
                ]

            # Validate response
            validation_results = self._validate_response(test_case, result)
            result["validation_results"] = validation_results

            # Determine overall status
            if all(validation_results.values()):
                result["status"] = "PASSED"
            else:
                result["status"] = "FAILED"
                failed_validations = [
                    k for k, v in validation_results.items() if not v]
                result["error"] = f"Validation failed: {', '.join(failed_validations)}"

        except Exception as e:
            result.update({
                "status": "ERROR",
                "error": str(e),
                "execution_time": time.time() - start_time
            })

        self.test_results.append(result)
        return result

    def _validate_response(self, test_case: TestCase, result: Dict[str, Any]) -> Dict[str, bool]:
        """Validate agent response against test case expectations."""
        validations = {}
        response = str(result["agent_response"]).lower()

        # Check execution time
        validations["execution_time_ok"] = result["execution_time"] <= test_case.max_execution_time

        # Check expected content
        if test_case.expected_contains:
            validations["contains_expected"] = all(
                expected.lower() in response
                for expected in test_case.expected_contains
            )

        # Check exact match
        if test_case.expected_exact:
            validations["exact_match"] = response.strip(
            ) == test_case.expected_exact.lower().strip()

        # Check tool usage
        if test_case.should_use_tools:
            tools_used = set(result["tools_used"])
            expected_tools = set(test_case.should_use_tools)
            validations["correct_tools_used"] = expected_tools.issubset(
                tools_used)

        # Response is not empty
        validations["non_empty_response"] = len(response.strip()) > 0

        return validations

    def run_test_suite(self, test_cases: List[TestCase]) -> Dict[str, Any]:
        """Run complete test suite and return comprehensive summary."""
        print(f"🧪 Running {self.test_name} Test Suite...")
        print(f"   Total test cases: {len(test_cases)}")
        print("-" * 50)

        for i, test_case in enumerate(test_cases, 1):
            print(f"Running test {i}/{len(test_cases)}: {test_case.name}")
            result = self.run_single_test(test_case)

            # Display result
            status_emoji = {
                "PASSED": "✅",
                "FAILED": "❌",
                "ERROR": "⚠️"
            }.get(result["status"], "❓")

            print(f"{status_emoji} {result['test_name']}: {result['status']} "
                  f"({result['execution_time']:.2f}s)")

            if result["error"]:
                print(f"   Error: {result['error']}")

        # Generate comprehensive summary
        summary = self._generate_summary(test_cases)
        self._print_summary(summary)

        return summary

    def _generate_summary(self, test_cases: List[TestCase]) -> Dict[str, Any]:
        """Generate comprehensive test summary."""
        passed = [r for r in self.test_results if r["status"] == "PASSED"]
        failed = [r for r in self.test_results if r["status"] == "FAILED"]
        errors = [r for r in self.test_results if r["status"] == "ERROR"]

        total_execution_time = sum(r["execution_time"]
                                   for r in self.test_results)
        avg_execution_time = total_execution_time / \
            len(self.test_results) if self.test_results else 0

        # Analyze tool usage
        all_tools_used = set()
        for result in self.test_results:
            all_tools_used.update(result["tools_used"])

        # Analyze validation failures
        validation_failures = {}
        for result in failed:
            for validation, passed in result["validation_results"].items():
                if not passed:
                    validation_failures[validation] = validation_failures.get(
                        validation, 0) + 1

        return {
            "test_suite_name": self.test_name,
            "total_tests": len(test_cases),
            "passed": len(passed),
            "failed": len(failed),
            "errors": len(errors),
            "success_rate": len(passed) / len(test_cases) * 100 if test_cases else 0,
            "total_execution_time": total_execution_time,
            "average_execution_time": avg_execution_time,
            "tools_used": list(all_tools_used),
            "validation_failures": validation_failures,
            "detailed_results": self.test_results
        }

    def _print_summary(self, summary: Dict[str, Any]):
        """Print formatted test summary."""
        print("\n" + "="*60)
        print(f"📊 {summary['test_suite_name']} - Test Summary")
        print("="*60)
        print(f"Total Tests: {summary['total_tests']}")
        print(
            f"✅ Passed: {summary['passed']} ({summary['success_rate']:.1f}%)")
        print(f"❌ Failed: {summary['failed']}")
        print(f"⚠️  Errors: {summary['errors']}")
        print(f"⏱️  Total Time: {summary['total_execution_time']:.2f}s")
        print(f"📈 Avg Time: {summary['average_execution_time']:.2f}s")

        if summary['tools_used']:
            print(f"🔧 Tools Used: {', '.join(summary['tools_used'])}")

        if summary['validation_failures']:
            print("\n❌ Most Common Validation Failures:")
            for failure, count in summary['validation_failures'].items():
                print(f"   - {failure}: {count} occurrences")

    def save_results(self, filepath: str):
        """Save test results to JSON file."""
        summary = self._generate_summary([])

        with open(filepath, 'w') as f:
            json.dump(summary, f, indent=2, default=str)

        print(f"💾 Test results saved to: {filepath}")

    def clear_results(self):
        """Clear test results for fresh run."""
        self.test_results.clear()
        self.performance_metrics.clear()


class MockLLMResponse:
    """Mock LLM response for testing."""

    def __init__(self, content: str, tool_calls: List[Dict] = None):
        self.content = content
        self.tool_calls = tool_calls or []


def create_test_cases_from_json(filepath: str) -> List[TestCase]:
    """Load test cases from JSON file."""
    with open(filepath, 'r') as f:
        data = json.load(f)

    test_cases = []
    for case_data in data.get('test_cases', []):
        test_case = TestCase(
            name=case_data['name'],
            input=case_data['input'],
            expected_contains=case_data.get('expected_contains'),
            expected_exact=case_data.get('expected_exact'),
            should_use_tools=case_data.get('should_use_tools'),
            max_execution_time=case_data.get('max_execution_time', 30.0),
            metadata=case_data.get('metadata')
        )
        test_cases.append(test_case)

    return test_cases


def mock_openai_response(response_text: str, tool_calls: List[Dict] = None):
    """Create mock OpenAI response for testing."""
    return Mock(
        choices=[Mock(
            message=Mock(
                content=response_text,
                tool_calls=tool_calls or []
            )
        )]
    )


def mock_anthropic_response(response_text: str):
    """Create mock Anthropic response for testing."""
    return Mock(content=response_text)


# Pytest fixtures for common testing scenarios
@pytest.fixture
def sample_test_cases():
    """Provide sample test cases for agent testing."""
    return [
        TestCase(
            name="Basic Calculation",
            input="What is 15 * 24?",
            expected_contains=["360"],
            should_use_tools=["calculator"]
        ),
        TestCase(
            name="Weather Query",
            input="What's the weather like today?",
            expected_contains=["weather", "today"],
            should_use_tools=["get_weather"]
        ),
        TestCase(
            name="String Length",
            input="How many characters are in 'LangChain'?",
            expected_contains=["9", "characters"],
            should_use_tools=["get_word_length"]
        )
    ]


@pytest.fixture
def mock_agent():
    """Provide mock agent for testing."""
    agent = Mock()
    agent.invoke.return_value = {
        "output": "Mock response from agent",
        "intermediate_steps": []
    }
    return agent
