# URL-Shortening

URL shortening is the process of taking a long complex link and converting it into a short, easy-to-share link. When someone clicks the short link, the URL shortening service instantly redirects them to the original, long link.

## Features

- **Simple and Easy to Use**: Clean Python implementation using only standard library
- **Hash-Based Short Codes**: Uses MD5 hashing and base62 encoding for generating short codes
- **Collision Handling**: Automatically handles hash collisions
- **Idempotent**: Same URL always returns the same short code
- **In-Memory Storage**: Fast lookups with dictionary-based storage
- **CLI Interface**: Interactive command-line interface for easy usage
- **Statistics**: Track the number of shortened URLs

## Installation

This project requires Python 3.6 or higher and uses only the Python standard library.

```bash
# Clone the repository
git clone https://github.com/harshmishra2701/URL-Shortening.git
cd URL-Shortening

# No additional dependencies needed!
```

## Usage

### 1. Command-Line Interface (CLI)

Run the interactive CLI:

```bash
python3 cli.py
```

Available commands:
- `shorten <url>` - Shorten a long URL
- `expand <url>` - Expand a shortened URL to get the original
- `list` - List all shortened URLs
- `stats` - Show statistics
- `help` - Show help message
- `quit` or `exit` - Exit the program

Example session:
```
url-shortener> shorten https://www.example.com/very/long/url/path
✓ Shortened URL: http://short.ly/kJ8xYz

url-shortener> expand http://short.ly/kJ8xYz
✓ Original URL: https://www.example.com/very/long/url/path

url-shortener> stats
Statistics:
Total shortened URLs: 1
Unique URLs: 1
```

### 2. As a Python Module

Import and use in your Python code:

```python
from url_shortener import URLShortener

# Create a shortener instance
shortener = URLShortener(base_url="http://short.ly/")

# Shorten a URL
long_url = "https://www.example.com/very/long/url"
short_url = shortener.shorten(long_url)
print(f"Short URL: {short_url}")

# Expand a shortened URL
original_url = shortener.expand(short_url)
print(f"Original URL: {original_url}")

# Get statistics
stats = shortener.get_stats()
print(f"Total URLs: {stats['total_urls']}")
```

### 3. Run Example Script

See the URL shortener in action:

```bash
python3 example.py
```

### 4. Run Demo

Run the built-in demo from the main module:

```bash
python3 url_shortener.py
```

## How It Works

1. **URL Shortening**: When you provide a long URL, the system:
   - Generates an MD5 hash of the URL
   - Converts the hash to a base62 encoded string (using A-Z, a-z, 0-9)
   - Creates a short code of 6 characters
   - Stores the mapping between short code and original URL

2. **URL Expansion**: When you provide a short URL:
   - Extracts the short code from the URL
   - Looks up the original URL in the mapping
   - Returns the original URL

3. **Collision Handling**: If two different URLs generate the same short code (rare but possible):
   - The system uses a counter-based approach
   - Generates a unique short code for the new URL

## Project Structure

```
URL-Shortening/
├── url_shortener.py   # Core URL shortener module
├── cli.py             # Interactive command-line interface
├── example.py         # Example usage script
├── requirements.txt   # Dependencies (none required for core functionality)
└── README.md          # This file
```

## API Reference

### URLShortener Class

#### `__init__(base_url: str = "http://short.ly/")`
Initialize the URL shortener with a custom base URL.

#### `shorten(long_url: str) -> str`
Shorten a long URL and return the shortened URL.

#### `expand(short_url: str) -> Optional[str]`
Expand a shortened URL and return the original URL, or None if not found.

#### `get_stats() -> Dict[str, int]`
Get statistics about the URL shortener (total URLs, unique URLs).

## Examples

### Example 1: Basic Usage
```python
from url_shortener import URLShortener

shortener = URLShortener()
short = shortener.shorten("https://www.example.com/long/url")
print(short)  # Output: http://short.ly/kJ8xYz
```

### Example 2: Custom Base URL
```python
shortener = URLShortener(base_url="https://mysite.co/")
short = shortener.shorten("https://www.example.com")
print(short)  # Output: https://mysite.co/kJ8xYz
```

### Example 3: Batch Shortening
```python
urls = [
    "https://www.github.com/user/repo",
    "https://www.stackoverflow.com/questions/123",
    "https://www.amazon.com/product/page"
]

shortener = URLShortener()
for url in urls:
    print(f"{url} -> {shortener.shorten(url)}")
```

## Limitations

- **In-Memory Storage**: URLs are stored in memory and will be lost when the program exits. For production use, consider adding persistent storage (database, file, etc.)
- **No Validation**: The current implementation doesn't validate if URLs are actually accessible
- **Single Instance**: Each URLShortener instance maintains its own separate storage
- **No Analytics**: Doesn't track click counts or access times

## Future Enhancements

Potential improvements for the future:
- Add persistent storage (SQLite, PostgreSQL, Redis)
- Implement custom short codes (vanity URLs)
- Add URL validation and checking
- Track analytics (click counts, timestamps, referrers)
- Add expiration dates for shortened URLs
- Implement rate limiting
- Add web interface (Flask/FastAPI)
- Support for QR code generation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Author

Created by Harsh Mishra
