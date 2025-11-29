"""
Tests for admin/tui.py - Terminal UI application.
"""
import pytest
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "admin"))


class TestPostListItem:
    """Tests for PostListItem widget."""

    def test_post_list_item_creation(self):
        """Test creating a post list item."""
        # Import here to avoid Textual dependency issues in CI
        try:
            from tui import PostListItem

            post_data = {
                'title': 'Test Post',
                'date': '2024-01-01',
                'slug': 'test-post'
            }

            item = PostListItem(post_data)
            assert item.post == post_data
        except ImportError:
            pytest.skip("Textual not available in test environment")


class TestEditorScreen:
    """Tests for EditorScreen."""

    def test_editor_screen_initialization(self):
        """Test editor screen initialization."""
        try:
            from tui import EditorScreen

            post_data = {
                'title': 'Test',
                'date': '2024-01-01',
                'category': 'Test',
                'tags': 'test',
                'content': 'Test content',
                'filename': 'test.md'
            }

            screen = EditorScreen(post_data)
            assert screen.post == post_data
            assert screen.filename == 'test.md'
        except ImportError:
            pytest.skip("Textual not available in test environment")

    def test_editor_screen_new_post(self):
        """Test editor screen for new post (no data)."""
        try:
            from tui import EditorScreen

            screen = EditorScreen()
            assert screen.post == {}
            assert screen.filename is None
        except ImportError:
            pytest.skip("Textual not available in test environment")


class TestBlogTUI:
    """Tests for main BlogTUI application."""

    def test_blogtui_has_bindings(self):
        """Test that BlogTUI defines keyboard bindings."""
        try:
            from tui import BlogTUI

            app = BlogTUI()
            assert hasattr(app, 'BINDINGS')
            assert len(app.BINDINGS) > 0
        except ImportError:
            pytest.skip("Textual not available in test environment")


# Note: Full UI testing would require Textual's AsyncioTestCase
# These are basic smoke tests to ensure classes can be instantiated
# For comprehensive UI testing, consider using Textual's built-in testing tools
