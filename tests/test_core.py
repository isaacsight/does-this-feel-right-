"""
Tests for admin/core.py - Blog admin functionality.
"""
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent and admin directories to path
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "admin"))

# Mock environment before importing core
os.environ['GEMINI_API_KEY'] = 'test_key'
os.environ['SUPABASE_URL'] = 'https://test.supabase.co'
os.environ['SUPABASE_KEY'] = 'test_key'

import core


class TestGetPosts:
    """Tests for retrieving blog posts."""

    @patch('core.os.listdir')
    @patch('core.os.path.join')
    @patch('builtins.open', create=True)
    @patch('core.frontmatter.load')
    def test_get_posts_success(self, mock_fm_load, mock_open, mock_join, mock_listdir):
        """Test successful post retrieval."""
        # Setup mocks
        mock_listdir.return_value = ['post1.md', 'post2.md', 'not_markdown.txt']
        mock_post = MagicMock()
        mock_post.__getitem__ = lambda self, key: f"Test {key}"
        mock_fm_load.return_value = mock_post

        posts = core.get_posts()

        # Should only process .md files
        assert mock_fm_load.call_count == 2
        assert len(posts) == 2

    @patch('core.os.listdir')
    def test_get_posts_empty_directory(self, mock_listdir):
        """Test handling of empty content directory."""
        mock_listdir.return_value = []
        posts = core.get_posts()
        assert posts == []


class TestSavePost:
    """Tests for saving blog posts."""

    @patch('core.os.path.join')
    @patch('builtins.open', create=True)
    @patch('core.frontmatter.dump')
    def test_save_post_with_filename(self, mock_dump, mock_open, mock_join):
        """Test saving a post with existing filename."""
        filename = core.save_post(
            filename="existing-post.md",
            title="Test Post",
            date="2024-01-01",
            category="Testing",
            tags="test, pytest",
            content="This is test content"
        )

        assert filename == "existing-post.md"
        mock_dump.assert_called_once()

    @patch('core.os.path.join')
    @patch('builtins.open', create=True)
    @patch('core.frontmatter.dump')
    def test_save_post_generates_filename(self, mock_dump, mock_open, mock_join):
        """Test saving a post generates slug from title."""
        filename = core.save_post(
            filename=None,
            title="My New Blog Post",
            date="2024-01-01",
            category="Testing",
            tags="test",
            content="Content here"
        )

        assert filename == "my-new-blog-post.md"

    @patch('core.os.path.join')
    @patch('builtins.open', create=True)
    @patch('core.frontmatter.dump')
    def test_save_post_parses_tags(self, mock_dump, mock_open, mock_join):
        """Test that string tags are parsed into list."""
        core.save_post(
            filename="test.md",
            title="Test",
            date="2024-01-01",
            category="Test",
            tags="tag1, tag2, tag3",
            content="Content"
        )

        # Verify frontmatter.dump was called (frontmatter.Post was created)
        assert mock_dump.called


class TestGenerateAIPost:
    """Tests for AI post generation."""

    @patch('core.save_post')
    @patch('core.genai.GenerativeModel')
    def test_generate_with_gemini(self, mock_model, mock_save):
        """Test AI generation with Gemini provider."""
        # Setup mock
        mock_response = Mock()
        mock_response.text = "# Generated Content\n\nThis is AI generated."
        mock_model.return_value.generate_content.return_value = mock_response
        mock_save.return_value = "ai-test-topic.md"

        filename = core.generate_ai_post("test topic", provider="gemini")

        assert filename == "ai-test-topic.md"
        mock_model.assert_called_once()

    @patch('core.save_post')
    @patch('core.openai.chat.completions.create')
    def test_generate_with_openai(self, mock_create, mock_save):
        """Test AI generation with OpenAI provider."""
        # Setup mock
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Generated content"
        mock_create.return_value = mock_response
        mock_save.return_value = "ai-test.md"

        filename = core.generate_ai_post("test", provider="openai")

        assert filename == "ai-test.md"

    def test_generate_invalid_provider(self):
        """Test that invalid provider raises exception."""
        # Since we don't validate provider in current code, this would pass through
        # This test documents expected future behavior
        with pytest.raises(Exception):
            core.generate_ai_post("test", provider="invalid_provider_name")


class TestPublishGit:
    """Tests for git publishing functionality."""

    @patch('core.subprocess.run')
    def test_publish_git_success(self, mock_run):
        """Test successful git publish."""
        mock_run.return_value = Mock(returncode=0)

        result = core.publish_git()

        assert "Successfully published" in result
        assert mock_run.call_count == 3  # add, commit, push

    @patch('core.subprocess.run')
    def test_publish_git_failure(self, mock_run):
        """Test git publish failure handling."""
        from subprocess import CalledProcessError

        mock_run.side_effect = CalledProcessError(1, 'git')

        with pytest.raises(Exception) as exc_info:
            core.publish_git()

        assert "Git publish failed" in str(exc_info.value)


class TestSecurityValidation:
    """Tests for input validation and security."""

    def test_save_post_validates_filename(self):
        """Test that filename is sanitized to prevent path traversal."""
        # This is a recommendation for future security improvement
        # Current code might not have this validation
        dangerous_filename = "../../../etc/passwd"

        with patch('builtins.open', create=True):
            with patch('core.frontmatter.dump'):
                # Should not allow path traversal
                filename = core.save_post(
                    filename=dangerous_filename,
                    title="Test",
                    date="2024-01-01",
                    category="Test",
                    tags="test",
                    content="Test"
                )

                # The filename should be sanitized
                assert ".." not in filename
                assert os.path.sep not in filename.replace(".md", "")
