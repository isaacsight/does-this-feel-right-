"""
PyTest configuration and shared fixtures for tests.
"""
import os
import tempfile
from pathlib import Path
from typing import Generator
import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_frontmatter() -> str:
    """Sample frontmatter content for testing."""
    return """---
title: Test Post
date: 2024-01-01
category: Testing
tags: test, sample
excerpt: This is a test post
---

This is the body content."""


@pytest.fixture
def sample_markdown() -> str:
    """Sample markdown content for testing."""
    return """# Header 1

This is a paragraph with **bold** and *italic* text.

## Header 2

* List item 1
* List item 2

```python
def hello():
    print("world")
```

> This is a quote
"""


@pytest.fixture
def mock_env(monkeypatch) -> None:
    """Mock environment variables for testing."""
    monkeypatch.setenv("GEMINI_API_KEY", "test_gemini_key")
    monkeypatch.setenv("OPENAI_API_KEY", "test_openai_key")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test_anthropic_key")
    monkeypatch.setenv("SUPABASE_URL", "https://test.supabase.co")
    monkeypatch.setenv("SUPABASE_KEY", "test_supabase_key")


@pytest.fixture
def sample_post_data() -> dict:
    """Sample post metadata for testing."""
    return {
        "title": "Test Post",
        "date": "2024-01-01",
        "category": "Testing",
        "tags": "test, sample, pytest",
        "excerpt": "This is a test post for the test suite",
        "slug": "test-post",
        "read_time": "5 min read",
    }
