# Agent Guidelines for RokuDocs

This repository contains scraped Roku developer documentation for AI agents to reference. The scraper uses Python with Selenium to extract content from https://developer.roku.com/.

## Setup

```bash
# Activate virtual environment
source env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Scraper

```bash
python scrape_roku_docs.py [options]
```

Options:
- `--base-dir DIR`: Base directory for output (default: current directory)
- `--no-headless`: Run browser in visible mode
- `--skip-existing`: Skip files that already exist
- `--delay SECONDS`: Delay between requests (default: 2.0)
- `--max-retries N`: Maximum retries for failed pages (default: 3)
- `--mode MODE`: Scraping mode: `references` (default), `developer`, `specs`, or `features`

Example:
```bash
python scrape_roku_docs.py --skip-existing --delay 1.5
python scrape_roku_docs.py --mode specs
python scrape_roku_docs.py --mode features
```

## Code Style Guidelines

### Python Code Style
- Use **snake_case** for variables, functions, and method names
- Use **PascalCase** for class names (e.g., `RokuDocScraper`)
- Use **UPPER_CASE** for constants (e.g., `BASE_URL`, `START_URL`)

### Imports
- Import standard library modules first, then third-party, then local
- Group imports logically with blank lines between groups:
  ```python
  import re
  import time
  from pathlib import Path
  
  from selenium import webdriver
  from bs4 import BeautifulSoup
  ```

### Type Hints
- Use type hints for function parameters and return values:
  ```python
  from typing import List, Dict, Optional
  
  def extract_navigation_links(self) -> List[Dict[str, str]]:
      ...
  
  def save_content(self, content: str, directory: Path, filename: str) -> bool:
      ...
  ```

### Docstrings
- Use triple-quoted docstrings for classes and methods
- Docstrings should be concise and describe purpose, parameters, and return types

### Error Handling
- Use specific exception catching (e.g., `TimeoutException`, `NoSuchElementException`)
- Log errors with appropriate log levels (`logger.error`, `logger.warning`)
- Use try/except blocks for Selenium operations that may fail

### Logging
- Configure logging at module level with format:
  ```python
  logging.basicConfig(
      level=logging.INFO,
      format='%(asctime)s - %(levelname)s - %(message)s',
      handlers=[logging.FileHandler(...), logging.StreamHandler()]
  )
  logger = logging.getLogger(__name__)
  ```
- Use `logger.info()`, `logger.warning()`, `logger.error()`, `logger.debug()` appropriately

### File I/O
- Use `pathlib.Path` for file operations
- Always use `utf-8` encoding: `open(filepath, 'w', encoding='utf-8')`
- Handle `FileExistsError` for directory creation on case-insensitive filesystems

### Web Scraping
- Use Selenium WebDriver with explicit waits (`WebDriverWait`, `EC.presence_of_element_located`)
- Always use `time.sleep()` after page loads to allow dynamic content to render
- Handle multiple selectors when elements may not be found with the first approach
- Clean URLs by removing query params and fragments
- Use `urljoin()` for URL construction

### Constants and Configuration
- Define constants at module level (BASE_URL, mappings, etc.)
- Use dictionaries for URL-to-directory mappings or transformations

## Project Structure

```
/
├── Developer/        # Developer program docs (--mode developer)
├── Reference/        # API reference docs (--mode references)
│   ├── BrightScript/
│   └── SceneGraph/
├── Specifications/   # Specs docs (--mode specs)
├── Features/         # Features docs (--mode features)
├── scrape_roku_docs.py
├── requirements.txt
└── env/
```

## Important Notes

- No formal test suite exists - run the scraper directly to verify changes
- No lint/typecheck configuration - write clear, readable code
- Documentation is scraped as plain text markdown (minimal formatting)
- The scraper handles JavaScript-rendered content via headless Chrome
- File naming preserves special characters like `<>` (e.g., `<component>.md`)
- Special naming rules exist for SceneGraph files (camelCase → PascalCase)