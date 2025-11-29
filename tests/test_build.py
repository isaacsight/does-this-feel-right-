"""
Tests for build.py - Static site generation functions.
"""
import pytest
from pathlib import Path
import sys

# Add parent directory to path to import build module
sys.path.insert(0, str(Path(__file__).parent.parent))

import build


class TestParseFrontmatter:
    """Tests for frontmatter parsing."""

    def test_parse_valid_frontmatter(self, sample_frontmatter):
        """Test parsing valid frontmatter."""
        metadata, body = build.parse_frontmatter(sample_frontmatter)

        assert metadata['title'] == 'Test Post'
        assert metadata['date'] == '2024-01-01'
        assert metadata['category'] == 'Testing'
        assert metadata['tags'] == 'test, sample'
        assert 'This is the body content.' in body

    def test_parse_no_frontmatter(self):
        """Test parsing content without frontmatter."""
        content = "Just plain content without frontmatter"
        metadata, body = build.parse_frontmatter(content)

        assert metadata == {}
        assert body == content

    def test_parse_empty_frontmatter(self):
        """Test parsing empty frontmatter section."""
        content = "---\n---\nBody content"
        metadata, body = build.parse_frontmatter(content)

        assert metadata == {}
        assert "Body content" in body


class TestMarkdownToHtml:
    """Tests for markdown to HTML conversion."""

    def test_headers(self):
        """Test header conversion."""
        md = "# Header 1\n## Header 2\n### Header 3"
        html = build.markdown_to_html(md)

        assert '<h1>Header 1</h1>' in html
        assert '<h2>Header 2</h2>' in html
        assert '<h3>Header 3</h3>' in html

    def test_paragraphs(self):
        """Test paragraph conversion."""
        md = "First paragraph\n\nSecond paragraph"
        html = build.markdown_to_html(md)

        assert '<p>First paragraph</p>' in html
        assert '<p>Second paragraph</p>' in html

    def test_lists(self):
        """Test list conversion."""
        md = "* Item 1\n* Item 2\n* Item 3"
        html = build.markdown_to_html(md)

        assert '<ul>' in html
        assert '</ul>' in html
        assert '<li>Item 1</li>' in html
        assert '<li>Item 2</li>' in html

    def test_bold_and_italic(self):
        """Test inline formatting."""
        md = "This is **bold** and this is *italic*"
        html = build.markdown_to_html(md)

        assert '<strong>bold</strong>' in html or '<b>bold</b>' in html
        assert '<em>italic</em>' in html or '<i>italic</i>' in html

    def test_links(self):
        """Test link conversion."""
        md = "[Link Text](https://example.com)"
        html = build.markdown_to_html(md)

        assert '<a href="https://example.com">Link Text</a>' in html

    def test_code_blocks(self):
        """Test code block conversion."""
        md = "```\ncode here\n```"
        html = build.markdown_to_html(md)

        assert '<pre><code>' in html
        assert '</code></pre>' in html
        assert 'code here' in html

    def test_blockquotes(self):
        """Test blockquote conversion."""
        md = "> This is a quote"
        html = build.markdown_to_html(md)

        assert '<blockquote>' in html
        assert 'This is a quote' in html


class TestCalculateSimilarity:
    """Tests for text similarity calculation."""

    def test_identical_texts(self):
        """Test similarity of identical texts."""
        text1 = "The quick brown fox jumps over the lazy dog"
        text2 = "The quick brown fox jumps over the lazy dog"

        similarity = build.calculate_similarity(text1, text2)
        assert similarity == pytest.approx(1.0, rel=0.1)

    def test_completely_different(self):
        """Test similarity of completely different texts."""
        text1 = "Python programming language"
        text2 = "Cooking delicious recipes"

        similarity = build.calculate_similarity(text1, text2)
        assert similarity < 0.3

    def test_partial_overlap(self):
        """Test texts with some common words."""
        text1 = "Python is a great programming language for web development"
        text2 = "Python programming enables rapid web application development"

        similarity = build.calculate_similarity(text1, text2)
        assert 0.3 < similarity < 0.8

    def test_empty_texts(self):
        """Test similarity with empty texts."""
        similarity = build.calculate_similarity("", "text")
        assert similarity == 0.0

        similarity = build.calculate_similarity("text", "")
        assert similarity == 0.0


class TestFileOperations:
    """Tests for file I/O operations."""

    def test_read_write_file(self, temp_dir):
        """Test reading and writing files."""
        test_file = temp_dir / "test.txt"
        content = "Test content for file operations"

        # Write
        build.write_file(str(test_file), content)
        assert test_file.exists()

        # Read
        read_content = build.read_file(str(test_file))
        assert read_content == content

    def test_write_creates_directories(self, temp_dir):
        """Test that write_file creates parent directories."""
        nested_file = temp_dir / "nested" / "path" / "file.txt"
        content = "Testing nested directory creation"

        build.write_file(str(nested_file), content)
        assert nested_file.exists()
        assert build.read_file(str(nested_file)) == content
