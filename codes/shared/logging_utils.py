"""
File: logging_utils.py
Purpose: Logging utilities for LangChain agent development and debugging
Chapter: Shared utilities across all chapters
Requirements: logging, datetime
"""

import logging
import time
import functools
from typing import Any, Dict, List, Callable
from datetime import datetime
from contextlib import contextmanager


class AgentLogger:
    """Enhanced logger for agent development and debugging."""

    def __init__(self, name: str, log_level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.conversation_log = []
        self.performance_metrics = {}

        # Configure logger if not already configured
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(getattr(logging, log_level.upper()))

    def log_agent_step(self, step_type: str, content: Any, metadata: Dict = None):
        """Log individual agent steps with context."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "step_type": step_type,
            "content": str(content),
            "metadata": metadata or {}
        }

        self.conversation_log.append(log_entry)
        self.logger.info(f"[{step_type}] {content}")

        # Add metadata details if available
        if metadata:
            for key, value in metadata.items():
                self.logger.debug(f"  {key}: {value}")

    def log_tool_execution(self, tool_name: str, input_data: Any,
                           output: Any, duration: float, success: bool = True):
        """Log tool execution with performance metrics."""
        status = "SUCCESS" if success else "FAILED"

        self.log_agent_step(
            "TOOL_EXECUTION",
            f"Tool: {tool_name} - {status}",
            {
                "tool_name": tool_name,
                "input": str(input_data)[:200] + "..." if len(str(input_data)) > 200 else str(input_data),
                "output": str(output)[:200] + "..." if len(str(output)) > 200 else str(output),
                "duration_ms": round(duration * 1000, 2),
                "success": success
            }
        )

        # Track performance metrics
        if tool_name not in self.performance_metrics:
            self.performance_metrics[tool_name] = {
                "total_calls": 0,
                "total_duration": 0,
                "successes": 0,
                "failures": 0
            }

        metrics = self.performance_metrics[tool_name]
        metrics["total_calls"] += 1
        metrics["total_duration"] += duration
        metrics["successes" if success else "failures"] += 1

    def log_llm_interaction(self, prompt: str, response: str,
                            duration: float, token_usage: Dict = None):
        """Log LLM interactions with token usage tracking."""
        self.log_agent_step(
            "LLM_INTERACTION",
            f"LLM Response Generated",
            {
                "prompt_preview": prompt[:100] + "..." if len(prompt) > 100 else prompt,
                "response_preview": response[:100] + "..." if len(response) > 100 else response,
                "duration_ms": round(duration * 1000, 2),
                "token_usage": token_usage or {}
            }
        )

    def get_performance_summary(self) -> Dict:
        """Get performance summary for all tools."""
        summary = {}
        for tool_name, metrics in self.performance_metrics.items():
            avg_duration = metrics["total_duration"] / \
                metrics["total_calls"] if metrics["total_calls"] > 0 else 0
            success_rate = metrics["successes"] / \
                metrics["total_calls"] if metrics["total_calls"] > 0 else 0

            summary[tool_name] = {
                "total_calls": metrics["total_calls"],
                "success_rate": round(success_rate * 100, 1),
                "average_duration_ms": round(avg_duration * 1000, 2),
                "total_duration_ms": round(metrics["total_duration"] * 1000, 2)
            }

        return summary

    def get_conversation_summary(self) -> Dict:
        """Get comprehensive conversation summary for analysis."""
        tool_executions = [entry for entry in self.conversation_log
                           if entry["step_type"] == "TOOL_EXECUTION"]

        llm_interactions = [entry for entry in self.conversation_log
                            if entry["step_type"] == "LLM_INTERACTION"]

        return {
            "total_steps": len(self.conversation_log),
            "tool_executions": len(tool_executions),
            "llm_interactions": len(llm_interactions),
            "tools_used": list(set(
                entry["metadata"].get("tool_name")
                for entry in tool_executions
                if entry["metadata"].get("tool_name")
            )),
            "total_duration_ms": sum(
                entry["metadata"].get("duration_ms", 0)
                for entry in self.conversation_log
            ),
            "performance_metrics": self.get_performance_summary(),
            "conversation_log": self.conversation_log
        }

    def clear_logs(self):
        """Clear conversation logs and reset metrics."""
        self.conversation_log.clear()
        self.performance_metrics.clear()


def monitor_performance(operation_name: str, logger: AgentLogger = None,
                        log_threshold_seconds: float = 1.0) -> Callable:
    """
    Decorator to monitor function performance and log slow operations.

    Args:
        operation_name: Human-readable name for the operation
        logger: AgentLogger instance (optional)
        log_threshold_seconds: Log warning if execution exceeds this time

    Returns:
        Decorated function with performance monitoring
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            error_occurred = False
            result = None

            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                error_occurred = True
                raise
            finally:
                execution_time = time.time() - start_time

                if logger:
                    logger.log_agent_step(
                        "PERFORMANCE_MONITOR",
                        f"Operation: {operation_name}",
                        {
                            "operation": operation_name,
                            "duration_ms": round(execution_time * 1000, 2),
                            "success": not error_occurred,
                            "threshold_exceeded": execution_time > log_threshold_seconds
                        }
                    )
                elif execution_time > log_threshold_seconds:
                    logging.warning(
                        f"Slow operation detected: {operation_name} "
                        f"took {execution_time:.2f} seconds"
                    )
        return wrapper
    return decorator


@contextmanager
def error_handling_context(operation_name: str, logger: AgentLogger = None):
    """Context manager for consistent error handling and logging."""
    start_time = time.time()

    try:
        if logger:
            logger.log_agent_step(
                "OPERATION_START", f"Starting: {operation_name}")
        else:
            logging.info(f"Starting operation: {operation_name}")

        yield

        duration = time.time() - start_time
        if logger:
            logger.log_agent_step(
                "OPERATION_COMPLETE",
                f"Completed: {operation_name}",
                {"duration_ms": round(duration * 1000, 2)}
            )
        else:
            logging.info(
                f"Completed operation: {operation_name} in {duration:.2f}s")

    except Exception as e:
        duration = time.time() - start_time
        error_msg = f"Operation {operation_name} failed after {duration:.2f}s: {e}"

        if logger:
            logger.log_agent_step(
                "OPERATION_ERROR",
                error_msg,
                {
                    "operation": operation_name,
                    "duration_ms": round(duration * 1000, 2),
                    "error_type": type(e).__name__,
                    "error_message": str(e)
                }
            )
        else:
            logging.error(error_msg)

        raise


def setup_production_logging(log_level: str = "INFO",
                             log_file: str = None,
                             structured: bool = True) -> logging.Logger:
    """
    Configure production-ready logging for LangChain applications.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for log output
        structured: Whether to use structured logging format

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("langchain_agent")
    logger.setLevel(getattr(logging, log_level.upper()))

    # Clear existing handlers
    logger.handlers.clear()

    # Configure formatter
    if structured:
        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
            '"module": "%(name)s", "message": "%(message)s", '
            '"line": %(lineno)d}'
        )
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
