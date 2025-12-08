"""
Unit tests for BookStack Connector.

Run with: pytest tests/test_bookstack_connector.py -v
Or standalone: python tests/test_bookstack_connector.py
"""

import sys
from pathlib import Path

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.connectors.bookstack_connector import BookStackConnector


class TestBookStackConnectorUnit:
    """Unit tests for BookStackConnector class."""

    def test_init_with_credentials(self):
        """Test initialization with credentials."""
        connector = BookStackConnector(
            base_url="https://example.com",
            token_id="test_id",
            token_secret="test_secret",
        )
        assert connector.base_url == "https://example.com"
        assert connector.token_id == "test_id"
        assert connector.token_secret == "test_secret"

    def test_init_strips_trailing_slash(self):
        """Test that trailing slash is stripped from base_url."""
        connector = BookStackConnector(
            base_url="https://example.com/",
            token_id="test_id",
            token_secret="test_secret",
        )
        assert connector.base_url == "https://example.com"

    def test_init_without_credentials(self):
        """Test initialization without credentials."""
        connector = BookStackConnector()
        assert connector.base_url is None
        assert connector.token_id is None
        assert connector.token_secret is None

    def test_set_credentials(self):
        """Test setting credentials after initialization."""
        connector = BookStackConnector()
        connector.set_credentials(
            base_url="https://example.com",
            token_id="test_id",
            token_secret="test_secret",
        )
        assert connector.base_url == "https://example.com"
        assert connector.token_id == "test_id"
        assert connector.token_secret == "test_secret"

    def test_get_headers(self):
        """Test header generation."""
        connector = BookStackConnector(
            base_url="https://example.com",
            token_id="test_id",
            token_secret="test_secret",
        )
        headers = connector.get_headers()
        assert headers["Authorization"] == "Token test_id:test_secret"
        assert headers["Content-Type"] == "application/json"
        assert headers["Accept"] == "application/json"

    def test_get_headers_without_credentials(self):
        """Test that get_headers raises error without credentials."""
        connector = BookStackConnector()
        with pytest.raises(ValueError) as exc_info:
            connector.get_headers()
        assert "credentials not initialized" in str(exc_info.value)

    def test_make_api_request_without_credentials(self):
        """Test that API request raises error without credentials."""
        connector = BookStackConnector()
        with pytest.raises(ValueError) as exc_info:
            connector.make_api_request("pages")
        assert "credentials not initialized" in str(exc_info.value)


class TestBookStackConnectorIntegration:
    """Integration tests for BookStack connector with demo instance.
    
    These tests require network access and valid credentials.
    Skip if credentials are not available.
    """

    # Demo instance credentials - get from https://demo.bookstackapp.com
    # Login: admin@example.com / password -> Edit Profile -> API Tokens
    BASE_URL = "https://demo.bookstackapp.com"
    TOKEN_ID = "YOUR_TOKEN_ID"  # Replace for integration tests
    TOKEN_SECRET = "YOUR_TOKEN_SECRET"  # Replace for integration tests

    @pytest.fixture
    def connector(self):
        """Create a connector with demo credentials."""
        return BookStackConnector(
            base_url=self.BASE_URL,
            token_id=self.TOKEN_ID,
            token_secret=self.TOKEN_SECRET,
        )

    @pytest.mark.integration
    def test_get_all_pages(self, connector):
        """Test fetching all pages from demo instance."""
        pages = connector.get_all_pages(count=10)
        assert isinstance(pages, list)
        assert len(pages) > 0
        # Check page structure
        if pages:
            page = pages[0]
            assert "id" in page
            assert "name" in page

    @pytest.mark.integration
    def test_get_page_detail(self, connector):
        """Test fetching page detail."""
        # First get a page ID
        pages = connector.get_all_pages(count=1)
        assert len(pages) > 0
        page_id = pages[0]["id"]

        # Get detail
        detail = connector.get_page_detail(page_id)
        assert "id" in detail
        assert "name" in detail
        assert "html" in detail

    @pytest.mark.integration
    def test_export_page_markdown(self, connector):
        """Test exporting page as markdown."""
        pages = connector.get_all_pages(count=1)
        assert len(pages) > 0
        page_id = pages[0]["id"]

        markdown = connector.export_page_markdown(page_id)
        assert isinstance(markdown, str)
        assert len(markdown) > 0

    @pytest.mark.integration
    def test_get_pages_by_date_range(self, connector):
        """Test fetching pages by date range."""
        pages, error = connector.get_pages_by_date_range(
            start_date="2020-01-01",
            end_date="2025-12-31",
        )
        # May or may not have pages, but should not error
        assert error is None or "No pages found" in error
        assert isinstance(pages, list)

    @pytest.mark.integration
    def test_get_page_with_content(self, connector):
        """Test fetching page with content."""
        pages = connector.get_all_pages(count=1)
        assert len(pages) > 0
        page_id = pages[0]["id"]

        detail, content = connector.get_page_with_content(page_id, use_markdown=True)
        assert "id" in detail
        assert isinstance(content, str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
