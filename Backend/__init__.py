"""Backend package initializer.

This file makes the Backend folder a Python package so relative imports work when
the app is executed from the repository root or when deployed.
"""

__all__ = ["main", "llm_client", "db"]
