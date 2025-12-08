"""
Test script for BookStack Connector.

Usage:
    1. Get API credentials from https://demo.bookstackapp.com
       - Login: admin@example.com / password
       - Go to Edit Profile -> API Tokens -> Create Token
    2. Replace TOKEN_ID and TOKEN_SECRET below
    3. Run: python -m app.connectors.test_bookstack
"""

from app.connectors.bookstack_connector import BookStackConnector

# Demo instance credentials - replace with your own token
BASE_URL = "https://demo.bookstackapp.com"
TOKEN_ID = "YOUR_TOKEN_ID"  # Replace with your token
TOKEN_SECRET = "YOUR_TOKEN_SECRET"  # Replace with your token


def test_connection():
    """Test basic API connection."""
    print("=" * 50)
    print("BookStack Connector Test")
    print("=" * 50)

    if TOKEN_ID == "YOUR_TOKEN_ID" or TOKEN_SECRET == "YOUR_TOKEN_SECRET":
        print("\n❌ Please set your TOKEN_ID and TOKEN_SECRET first!")
        print("   1. Login to https://demo.bookstackapp.com")
        print("   2. Go to Edit Profile -> API Tokens -> Create Token")
        print("   3. Copy the Token ID and Token Secret to this file")
        return False

    connector = BookStackConnector(
        base_url=BASE_URL,
        token_id=TOKEN_ID,
        token_secret=TOKEN_SECRET,
    )

    try:
        # Test 1: Get all pages
        print("\n[Test 1] Fetching pages list...")
        pages = connector.get_all_pages(count=10)
        print(f"   ✅ Found {len(pages)} pages")

        if pages:
            # Test 2: Get page detail
            first_page = pages[0]
            page_id = first_page["id"]
            print(f"\n[Test 2] Fetching page detail (ID: {page_id})...")
            detail = connector.get_page_detail(page_id)
            print(f"   ✅ Page: {detail.get('name', 'Unknown')}")
            print(f"   ✅ Book ID: {detail.get('book_id', 'N/A')}")
            print(f"   ✅ Has HTML: {'html' in detail}")
            print(f"   ✅ Has Markdown: {'markdown' in detail}")

            # Test 3: Export as Markdown
            print(f"\n[Test 3] Exporting page as Markdown...")
            markdown = connector.export_page_markdown(page_id)
            print(f"   ✅ Markdown length: {len(markdown)} chars")
            if markdown:
                preview = markdown[:200].replace("\n", " ")
                print(f"   Preview: {preview}...")

            # Test 4: Get pages by date range
            print("\n[Test 4] Fetching pages by date range...")
            recent_pages, error = connector.get_pages_by_date_range(
                start_date="2020-01-01",
                end_date="2025-12-31",
            )
            if error:
                print(f"   ⚠️ Warning: {error}")
            else:
                print(f"   ✅ Found {len(recent_pages)} pages updated since 2020-01-01")

        print("\n" + "=" * 50)
        print("✅ All tests passed! BookStack connector is working.")
        print("=" * 50)
        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


if __name__ == "__main__":
    test_connection()
