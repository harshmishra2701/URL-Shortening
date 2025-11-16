#!/usr/bin/env python3
"""
Command-line interface for URL Shortener

This script provides an interactive CLI for shortening and expanding URLs.
"""

import sys
from url_shortener import URLShortener


def print_banner():
    """Print a welcome banner."""
    print("\n" + "=" * 70)
    print(" " * 20 + "URL SHORTENER CLI")
    print("=" * 70)
    print()


def print_help():
    """Print help information."""
    print("Commands:")
    print("  shorten <url>  - Shorten a long URL")
    print("  expand <url>   - Expand a shortened URL")
    print("  list           - List all shortened URLs")
    print("  stats          - Show statistics")
    print("  help           - Show this help message")
    print("  quit/exit      - Exit the program")
    print()


def main():
    """Main CLI function."""
    shortener = URLShortener()
    
    print_banner()
    print("Welcome to URL Shortener!")
    print("Type 'help' for available commands.\n")
    
    while True:
        try:
            user_input = input("url-shortener> ").strip()
            
            if not user_input:
                continue
            
            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()
            
            if command in ['quit', 'exit']:
                print("\nGoodbye!")
                break
            
            elif command == 'help':
                print_help()
            
            elif command == 'shorten':
                if len(parts) < 2:
                    print("Error: Please provide a URL to shorten.")
                    print("Usage: shorten <url>")
                else:
                    long_url = parts[1]
                    short_url = shortener.shorten(long_url)
                    print(f"\n✓ Shortened URL: {short_url}\n")
            
            elif command == 'expand':
                if len(parts) < 2:
                    print("Error: Please provide a shortened URL to expand.")
                    print("Usage: expand <url>")
                else:
                    short_url = parts[1]
                    original_url = shortener.expand(short_url)
                    if original_url:
                        print(f"\n✓ Original URL: {original_url}\n")
                    else:
                        print("\n✗ Short URL not found in database.\n")
            
            elif command == 'list':
                if not shortener.url_mapping:
                    print("\nNo URLs have been shortened yet.\n")
                else:
                    print("\nShortened URLs:")
                    print("-" * 70)
                    for short_code, long_url in shortener.url_mapping.items():
                        short_url = shortener.base_url + short_code
                        display_url = long_url if len(long_url) <= 50 else long_url[:47] + "..."
                        print(f"{short_url} -> {display_url}")
                    print()
            
            elif command == 'stats':
                stats = shortener.get_stats()
                print("\nStatistics:")
                print("-" * 70)
                print(f"Total shortened URLs: {stats['total_urls']}")
                print(f"Unique URLs: {stats['unique_urls']}")
                print()
            
            else:
                print(f"Unknown command: {command}")
                print("Type 'help' for available commands.\n")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()
