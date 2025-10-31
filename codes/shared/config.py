"""
File: config.py
Purpose: Centralized configuration management for LangChain applications
Chapter: Shared utilities across all chapters
Requirements: python-dotenv, langchain
"""

import os
import logging
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class LangChainConfig:
    """Production-ready configuration for LangChain applications."""

    # API Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")

    # Model Configuration
    default_model: str = "gpt-4"
    temperature: float = 0.1
    max_tokens: int = 4096
    timeout: int = 30

    # LangSmith Configuration (Observability)
    langchain_api_key: str = os.getenv("LANGCHAIN_API_KEY", "")
    langchain_tracing_v2: bool = os.getenv(
        "LANGCHAIN_TRACING_V2", "false").lower() == "true"
    langchain_project: str = os.getenv(
        "LANGCHAIN_PROJECT", "langchain-development")

    # Development Configuration
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    verbose_logging: bool = os.getenv(
        "VERBOSE_LOGGING", "false").lower() == "true"

    def __post_init__(self):
        """Validate configuration after initialization."""
        self._setup_logging()
        self._validate_required_keys()

    def _setup_logging(self) -> None:
        """Configure logging based on debug settings."""
        log_level = logging.DEBUG if self.debug else logging.INFO
        if self.verbose_logging:
            log_level = logging.DEBUG

        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('langchain_app.log')
            ]
        )

    def _validate_required_keys(self) -> None:
        """Validate that at least one API key is available."""
        if not self.openai_api_key and not self.anthropic_api_key:
            logging.warning(
                "No API keys configured. Set OPENAI_API_KEY or ANTHROPIC_API_KEY "
                "environment variables to use language models."
            )

    def get_model_config(self, model_name: Optional[str] = None) -> Dict[str, Any]:
        """Get model configuration for LangChain initialization."""
        return {
            "model": model_name or self.default_model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "timeout": self.timeout
        }

    def validate_openai(self) -> None:
        """Validate OpenAI configuration."""
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

    def validate_anthropic(self) -> None:
        """Validate Anthropic configuration."""
        if not self.anthropic_api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable is required")

    def enable_tracing(self) -> None:
        """Enable LangSmith tracing for observability."""
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_PROJECT"] = self.langchain_project
        if self.langchain_api_key:
            os.environ["LANGCHAIN_API_KEY"] = self.langchain_api_key


# Global configuration instance
config = LangChainConfig()
