"""
URL Shortener Module

This module provides functionality to shorten long URLs into short, easy-to-share links.
It uses base62 encoding to generate short codes from URL hashes.
"""

import hashlib
import string
from typing import Dict, Optional


class URLShortener:
    """A simple URL shortening service."""
    
    def __init__(self, base_url: str = "http://short.ly/"):
        """
        Initialize the URL shortener.
        
        Args:
            base_url: The base URL for shortened links (default: http://short.ly/)
        """
        self.base_url = base_url.rstrip('/') + '/'
        self.url_mapping: Dict[str, str] = {}  # Maps short code to original URL
        self.reverse_mapping: Dict[str, str] = {}  # Maps original URL to short code
        self.counter = 0
        
        # Base62 characters for encoding
        self.base62_chars = string.ascii_letters + string.digits
    
    def _generate_short_code(self, url: str, length: int = 6) -> str:
        """
        Generate a short code for the given URL.
        
        Args:
            url: The URL to shorten
            length: The length of the short code (default: 6)
        
        Returns:
            A short code string
        """
        # Use MD5 hash of the URL
        hash_object = hashlib.md5(url.encode())
        hash_hex = hash_object.hexdigest()
        
        # Convert hex to integer
        hash_int = int(hash_hex, 16)
        
        # Convert to base62
        short_code = ""
        for _ in range(length):
            short_code = self.base62_chars[hash_int % 62] + short_code
            hash_int //= 62
        
        # Handle collision by incrementing counter
        if short_code in self.url_mapping and self.url_mapping[short_code] != url:
            self.counter += 1
            short_code = self._encode_base62(self.counter, length)
        
        return short_code
    
    def _encode_base62(self, num: int, length: int = 6) -> str:
        """
        Encode a number to base62.
        
        Args:
            num: The number to encode
            length: Minimum length of the result
        
        Returns:
            Base62 encoded string
        """
        if num == 0:
            return self.base62_chars[0] * length
        
        result = ""
        while num > 0:
            result = self.base62_chars[num % 62] + result
            num //= 62
        
        # Pad with leading characters if needed
        return result.rjust(length, self.base62_chars[0])
    
    def shorten(self, long_url: str) -> str:
        """
        Shorten a long URL.
        
        Args:
            long_url: The long URL to shorten
        
        Returns:
            The shortened URL
        """
        # Check if URL already shortened
        if long_url in self.reverse_mapping:
            short_code = self.reverse_mapping[long_url]
            return self.base_url + short_code
        
        # Generate short code
        short_code = self._generate_short_code(long_url)
        
        # Store mappings
        self.url_mapping[short_code] = long_url
        self.reverse_mapping[long_url] = short_code
        
        return self.base_url + short_code
    
    def expand(self, short_url: str) -> Optional[str]:
        """
        Expand a shortened URL to get the original URL.
        
        Args:
            short_url: The shortened URL
        
        Returns:
            The original long URL, or None if not found
        """
        # Extract short code from URL
        if short_url.startswith(self.base_url):
            short_code = short_url[len(self.base_url):]
        else:
            short_code = short_url
        
        return self.url_mapping.get(short_code)
    
    def get_stats(self) -> Dict[str, int]:
        """
        Get statistics about the URL shortener.
        
        Returns:
            Dictionary with statistics
        """
        return {
            "total_urls": len(self.url_mapping),
            "unique_urls": len(self.reverse_mapping)
        }


def main():
    """Main function demonstrating URL shortener usage."""
    # Create URL shortener instance
    shortener = URLShortener()
    
    # Example URLs to shorten
    test_urls = [
        "https://www.example.com/very/long/url/with/many/segments/and/parameters?id=12345&session=abcdefghijklmnop",
        "https://github.com/some-user/some-repository/blob/main/src/components/LongFileName.tsx",
        "https://stackoverflow.com/questions/12345678/how-to-implement-url-shortening-service-in-python"
    ]
    
    print("=" * 70)
    print("URL Shortening Service Demo")
    print("=" * 70)
    print()
    
    # Shorten URLs
    for url in test_urls:
        short_url = shortener.shorten(url)
        print(f"Original: {url}")
        print(f"Shortened: {short_url}")
        print()
    
    # Demonstrate expansion
    print("-" * 70)
    print("URL Expansion Demo")
    print("-" * 70)
    print()
    
    short_url = shortener.shorten(test_urls[0])
    expanded = shortener.expand(short_url)
    print(f"Short URL: {short_url}")
    print(f"Expanded: {expanded}")
    print()
    
    # Show statistics
    stats = shortener.get_stats()
    print("-" * 70)
    print("Statistics")
    print("-" * 70)
    print(f"Total shortened URLs: {stats['total_urls']}")
    print(f"Unique URLs: {stats['unique_urls']}")
    print()


if __name__ == "__main__":
    main()
