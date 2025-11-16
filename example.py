#!/usr/bin/env python3
"""
Example usage of the URL Shortener

This script demonstrates basic usage of the URL shortener module.
"""

from url_shortener import URLShortener


def main():
    """Demonstrate URL shortener usage with examples."""
    
    # Create a URL shortener instance
    print("Creating URL Shortener instance...\n")
    shortener = URLShortener(base_url="http://short.ly/")
    
    # Example 1: Shorten a single URL
    print("Example 1: Shorten a single URL")
    print("-" * 50)
    long_url = "https://www.example.com/very/long/url/path?param1=value1&param2=value2"
    short_url = shortener.shorten(long_url)
    print(f"Long URL:  {long_url}")
    print(f"Short URL: {short_url}\n")
    
    # Example 2: Expand the shortened URL
    print("Example 2: Expand a shortened URL")
    print("-" * 50)
    expanded_url = shortener.expand(short_url)
    print(f"Short URL:    {short_url}")
    print(f"Expanded URL: {expanded_url}\n")
    
    # Example 3: Shorten multiple URLs
    print("Example 3: Shorten multiple URLs")
    print("-" * 50)
    urls_to_shorten = [
        "https://github.com/user/repository/blob/main/README.md",
        "https://stackoverflow.com/questions/123456/long-question-title",
        "https://www.amazon.com/product/with/very/long/path/and/many/parameters"
    ]
    
    for url in urls_to_shorten:
        short = shortener.shorten(url)
        print(f"{url[:50]}... -> {short}")
    print()
    
    # Example 4: Test idempotency (same URL returns same short code)
    print("Example 4: Test idempotency")
    print("-" * 50)
    test_url = "https://www.python.org/doc/essay/"
    short1 = shortener.shorten(test_url)
    short2 = shortener.shorten(test_url)
    print(f"First call:  {short1}")
    print(f"Second call: {short2}")
    print(f"Same result: {short1 == short2}\n")
    
    # Example 5: Show statistics
    print("Example 5: Statistics")
    print("-" * 50)
    stats = shortener.get_stats()
    print(f"Total shortened URLs: {stats['total_urls']}")
    print(f"Unique URLs: {stats['unique_urls']}\n")
    
    # Example 6: Custom base URL
    print("Example 6: Custom base URL")
    print("-" * 50)
    custom_shortener = URLShortener(base_url="https://myurl.co/")
    custom_short = custom_shortener.shorten("https://www.example.com/page")
    print(f"Custom short URL: {custom_short}\n")


if __name__ == "__main__":
    main()
