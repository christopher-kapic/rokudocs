#!/usr/bin/env python3
"""
Roku Documentation Scraper

Scrapes documentation from https://developer.roku.com/ using Selenium
to handle JavaScript-rendered content. Extracts all documentation pages
and saves them according to the existing directory structure.
"""

import re
import time
import logging
from pathlib import Path
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Tuple, Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

BASE_URL = "https://developer.roku.com"
REFERENCE_START_URL = f"{BASE_URL}/docs/references/references-overview.md"
DEVELOPER_START_URL = f"{BASE_URL}/docs/developer-program/getting-started/roku-dev-prog.md"
SPECS_START_URL = f"{BASE_URL}/docs/specs/specs-overview.md"
FEATURES_START_URL = f"{BASE_URL}/docs/features/features-overview.md"

# URL to directory mapping
URL_TO_DIR_MAP = {
    'brightscript/components': 'BrightScript/Components',
    'brightscript/interfaces': 'BrightScript/Interfaces',
    'brightscript/language': 'BrightScript/Language',
    'brightscript/events': 'BrightScript/Events',
    'scenegraph': 'SceneGraph',
}

# Special directory mappings for SceneGraph subdirectories
SCENEGRAPH_SUBDIR_MAP = {
    'component-functions': 'Component functions',
    'xml-elements': 'XML Events',
    'abstract-nodes': 'Abstract Nodes',
    'renderable-nodes': 'Renderable Nodes',
    'label-nodes': 'Label Nodes',
    'animation-nodes': 'Animation Nodes',
    'typographic-nodes': 'Typographic Nodes',
    'control-nodes': 'Control Nodes',
    'layout-group-nodes': 'Layout-Group Nodes',
    'dynamic-voice-keyboard-nodes': 'Voice Keyboard Nodes',
    'standard-dialog-framework-nodes': 'StandardDialog Nodes',
    'dialog-nodes': 'Dialog Nodes',
    'widget-nodes': 'Widget Nodes',
    'list-and-grid-nodes': 'Lists and grid Nodes',
    'sliding-panels-nodes': 'Sliding Panel Nodes',
    'media-playback-nodes': 'Media Playback Nodes',
}


class RokuDocScraper:
    def __init__(self, base_dir: str = ".", headless: bool = True, skip_existing: bool = False):
        self.base_dir = Path(base_dir)
        self.headless = headless
        self.skip_existing = skip_existing
        self.driver = None
        self.visited_urls = set()
        self.failed_urls = []
        self.skipped_files = []
        
    def setup_driver(self):
        """Initialize Chrome WebDriver with appropriate options."""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)
        logger.info("WebDriver initialized successfully")
        
    def close_driver(self):
        """Close the WebDriver."""
        if self.driver:
            self.driver.quit()
            logger.info("WebDriver closed")
            
    def wait_for_element(self, by: By, value: str, timeout: int = 30):
        """Wait for an element to be present."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            logger.warning(f"Timeout waiting for element: {value}")
            return None
            
    def extract_navigation_links(self, mode: str = 'references') -> List[Dict[str, str]]:
        """
        Extract all documentation links from the navigation menu.
        Args:
            mode: 'references' to extract reference docs, 'developer' to extract developer docs,
                  'specs' to extract specifications docs, 'features' to extract features docs
        Returns a list of dictionaries with 'url' and 'title' keys.
        """
        logger.info(f"Extracting navigation links for mode: {mode}...")
        links = []
        
        # Determine which URL pattern to look for
        if mode == 'developer':
            url_pattern = '/docs/developer-program/'
        elif mode == 'specs':
            url_pattern = '/docs/specs/'
        elif mode == 'features':
            url_pattern = '/docs/features/'
        else:
            url_pattern = '/docs/references/'
        
        try:
            # Wait for navigation menu to load
            nav_container = self.wait_for_element(
                By.CSS_SELECTOR, 
                "#document-nav-menu > nav > div.doc-nav > div",
                timeout=30
            )
            
            if not nav_container:
                logger.error("Could not find navigation container")
                return links
                
            # Wait a bit more for JavaScript to fully render
            time.sleep(5)
            
            # Try to wait for at least one link to be visible and have an href
            try:
                WebDriverWait(self.driver, 15).until(
                    lambda d: len([el for el in d.find_elements(By.CSS_SELECTOR, "a.doc-nav-subcategory-link") 
                                  if el.get_attribute('href') and url_pattern in el.get_attribute('href')]) > 0
                )
            except TimeoutException:
                logger.warning("Timeout waiting for links with valid hrefs")
            
            # Try to expand all collapsed sections by clicking on group headers
            try:
                group_headers = nav_container.find_elements(
                    By.CSS_SELECTOR,
                    ".doc-nav-group > .doc-nav-title"
                )
                for header in group_headers:
                    try:
                        # Check if the subcategory is hidden
                        parent = header.find_element(By.XPATH, "./..")
                        subcategory = parent.find_element(By.CSS_SELECTOR, ".doc-nav-subcategory")
                        if "hidden" in subcategory.get_attribute("class"):
                            # Click to expand
                            self.driver.execute_script("arguments[0].click();", header)
                            time.sleep(0.2)
                    except:
                        pass
            except Exception as e:
                logger.debug(f"Could not expand all sections: {e}")
            
            # Also try to expand nested groups
            try:
                nested_groups = nav_container.find_elements(
                    By.CSS_SELECTOR,
                    ".doc-nav-group .doc-nav-group > .doc-nav-title"
                )
                for header in nested_groups:
                    try:
                        parent = header.find_element(By.XPATH, "./..")
                        subcategory = parent.find_element(By.CSS_SELECTOR, ".doc-nav-subcategory")
                        if "hidden" in subcategory.get_attribute("class"):
                            self.driver.execute_script("arguments[0].click();", header)
                            time.sleep(0.2)
                    except:
                        pass
            except Exception as e:
                logger.debug(f"Could not expand nested sections: {e}")
            
            # Wait a moment for expansion animations
            time.sleep(2)
            
            # Scroll to make sure all links are in view (helps with lazy loading)
            try:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", nav_container)
                time.sleep(0.5)
            except:
                pass
            
            # Wait for links to be visible and loaded
            try:
                WebDriverWait(nav_container, 10).until(
                    lambda d: len(d.find_elements(By.CSS_SELECTOR, "a.doc-nav-subcategory-link")) > 0
                )
            except:
                pass
            
            # Find all documentation links (including those in previously hidden sections)
            # Try multiple selectors to catch all links
            link_elements = nav_container.find_elements(
                By.CSS_SELECTOR, 
                "a.doc-nav-subcategory-link"
            )
            
            # If we didn't find enough, try alternative selector
            if len(link_elements) < 10:
                logger.debug("Trying alternative selector for links")
                link_elements = nav_container.find_elements(
                    By.CSS_SELECTOR,
                    f"a[href*='{url_pattern}']"
                )
            
            logger.info(f"Found {len(link_elements)} documentation links")
            
            # Debug: Check first few links to see what we're getting
            if link_elements:
                logger.info(f"Sample link hrefs (first 10):")
                valid_count = 0
                for i, link_elem in enumerate(link_elements[:10]):
                    try:
                        href = link_elem.get_attribute('href')
                        title = link_elem.text.strip()[:50] if link_elem.text else 'NO TEXT'
                        is_valid = href and url_pattern in href
                        if is_valid:
                            valid_count += 1
                        logger.info(f"  Link {i+1}: href='{href}', title='{title}', valid={is_valid}")
                    except Exception as e:
                        logger.debug(f"  Link {i+1}: Error - {e}")
                logger.info(f"Found {valid_count} valid links out of {min(10, len(link_elements))} checked")
            
            seen_urls = set()
            for link_elem in link_elements:
                try:
                    # Try multiple methods to get the href
                    href = link_elem.get_attribute('href')
                    if not href or href == 'None':
                        # Try getting it via JavaScript
                        href = self.driver.execute_script("return arguments[0].getAttribute('href');", link_elem)
                    if not href or href == 'None':
                        # Try getting the property
                        href = link_elem.get_property('href')
                    if not href or href == 'None':
                        # Try getting from outerHTML
                        outer_html = link_elem.get_attribute('outerHTML')
                        if outer_html and 'href=' in outer_html:
                            import re
                            match = re.search(r'href=["\']([^"\']+)["\']', outer_html)
                            if match:
                                href = match.group(1)
                    
                    title = link_elem.get_attribute('title') or link_elem.text.strip()
                    
                    if not href or href.strip() == '' or href == 'None':
                        logger.debug(f"Link with title '{title}' has no valid href attribute")
                        continue
                    
                    # Clean up the href
                    href = href.strip()
                    
                    # Check if this is a documentation link matching our mode
                    if url_pattern not in href:
                        # Log first few non-matching links for debugging
                        if len(seen_urls) < 3:
                            logger.debug(f"Link '{title}' href doesn't contain '{url_pattern}': {href}")
                        continue
                    
                    # Extract the path part (handle both relative and absolute URLs)
                    idx = href.find(url_pattern)
                    path = href[idx:]
                    
                    # Remove query params and fragments
                    if '?' in path:
                        path = path.split('?')[0]
                    if '#' in path:
                        path = path.split('#')[0]
                    
                    # Ensure path starts with /
                    if not path.startswith('/'):
                        path = '/' + path
                    
                    # Build full URL
                    full_url = urljoin(BASE_URL, path)
                    
                    # Double-check it's a valid documentation URL
                    if url_pattern not in full_url:
                        logger.debug(f"Constructed URL doesn't contain '{url_pattern}': {full_url}")
                        continue
                    
                    # Avoid duplicates
                    if full_url not in seen_urls:
                        seen_urls.add(full_url)
                        links.append({
                            'url': full_url,
                            'title': title,
                            'path': path
                        })
                except Exception as e:
                    logger.warning(f"Error extracting link: {e}", exc_info=True)
                    continue
                    
        except Exception as e:
            logger.error(f"Error extracting navigation links: {e}", exc_info=True)
            
        logger.info(f"Extracted {len(links)} unique documentation links")
        return links
        
    def url_to_filepath(self, url: str) -> Tuple[Path, str]:
        """
        Convert a documentation URL to a file path matching the existing structure.
        Returns (directory_path, filename)
        """
        parsed = urlparse(url)
        path_parts = [p for p in parsed.path.strip('/').split('/') if p]
        
        # Check if this is a specs URL
        if 'docs' in path_parts and 'specs' in path_parts:
            specs_idx = path_parts.index('specs')
            relevant_parts = path_parts[specs_idx + 1:]
            if not relevant_parts:
                logger.warning(f"Could not parse specs URL: {url}")
                return None, None
            filename = relevant_parts[-1]
            if not filename.endswith('.md'):
                filename += '.md'
            dir_parts = [self.base_dir, 'Specifications']
            if len(relevant_parts) > 1:
                for subdir in relevant_parts[:-1]:
                    dir_name = subdir.replace('-', ' ').title()
                    dir_parts.append(dir_name)
            if filename.endswith('.MD') or filename.endswith('.Md') or filename.endswith('.mD'):
                filename = filename.rsplit('.', 1)[0] + '.md'
            elif not filename.endswith('.md'):
                filename = filename + '.md'
            directory = Path(*dir_parts)
            return directory, filename
        
        # Check if this is a features URL
        if 'docs' in path_parts and 'features' in path_parts:
            features_idx = path_parts.index('features')
            relevant_parts = path_parts[features_idx + 1:]
            if not relevant_parts:
                logger.warning(f"Could not parse features URL: {url}")
                return None, None
            filename = relevant_parts[-1]
            if not filename.endswith('.md'):
                filename += '.md'
            dir_parts = [self.base_dir, 'Features']
            if len(relevant_parts) > 1:
                for subdir in relevant_parts[:-1]:
                    dir_name = subdir.replace('-', ' ').title()
                    dir_parts.append(dir_name)
            if filename.endswith('.MD') or filename.endswith('.Md') or filename.endswith('.mD'):
                filename = filename.rsplit('.', 1)[0] + '.md'
            elif not filename.endswith('.md'):
                filename = filename + '.md'
            directory = Path(*dir_parts)
            return directory, filename
        
        # Check if this is a developer-program URL
        if 'docs' in path_parts and 'developer-program' in path_parts:
            # Handle developer-program URLs (flattened structure)
            dev_idx = path_parts.index('developer-program')
            relevant_parts = path_parts[dev_idx + 1:]  # Skip 'developer-program'
            
            if not relevant_parts:
                logger.warning(f"Could not parse developer-program URL: {url}")
                return None, None
            
            # Get the filename (last part, should end with .md)
            filename = relevant_parts[-1]
            if not filename.endswith('.md'):
                filename += '.md'
            
            # Build directory path: Developer/[subdirs...]
            dir_parts = [self.base_dir, 'Developer']
            
            # Add subdirectories (everything except the filename)
            if len(relevant_parts) > 1:
                for subdir in relevant_parts[:-1]:
                    # Convert kebab-case to title case for directory names
                    dir_name = subdir.replace('-', ' ').title()
                    dir_parts.append(dir_name)
            
            # Ensure filename always has lowercase .md extension
            if filename.endswith('.MD') or filename.endswith('.Md') or filename.endswith('.mD'):
                filename = filename.rsplit('.', 1)[0] + '.md'
            elif not filename.endswith('.md'):
                filename = filename + '.md'
            
            directory = Path(*dir_parts)
            return directory, filename
        
        # Handle references URLs (BrightScript and SceneGraph)
        # Extract the relevant parts (skip 'docs' and 'references')
        if 'docs' in path_parts and 'references' in path_parts:
            ref_idx = path_parts.index('references')
            relevant_parts = path_parts[ref_idx + 1:]
        else:
            relevant_parts = path_parts
            
        if not relevant_parts:
            logger.warning(f"Could not parse URL: {url}")
            return None, None
            
        # Get the filename (last part, should end with .md)
        filename = relevant_parts[-1]
        if not filename.endswith('.md'):
            filename += '.md'
            
        # Remove .md extension for processing
        base_filename = filename[:-3] if filename.endswith('.md') else filename
        
        # Determine base directory
        if 'brightscript' in relevant_parts[0].lower():
            base_dir_name = 'BrightScript'
            category = relevant_parts[1] if len(relevant_parts) > 1 else None
        elif 'scenegraph' in relevant_parts[0].lower():
            base_dir_name = 'SceneGraph'
            category = None
        else:
            # Unknown category, save to root
            logger.warning(f"Unknown category in URL: {url}")
            return self.base_dir, filename
            
        # Build directory path - prepend 'Reference' for reference docs
        dir_parts = [self.base_dir, 'Reference', base_dir_name]
        
        if base_dir_name == 'BrightScript':
            if category:
                # Map category to directory name
                category_map = {
                    'components': 'Components',
                    'interfaces': 'Interfaces',
                    'language': 'Language',
                    'events': 'Events',
                }
                mapped_category = category_map.get(category, category.title())
                dir_parts.append(mapped_category)
                
        elif base_dir_name == 'SceneGraph':
            # Handle SceneGraph subdirectories
            # Structure: scenegraph/[subdir]/filename.md
            # If len(relevant_parts) == 2, it's a root-level file (scenegraph/filename.md)
            # If len(relevant_parts) > 2, it's in a subdirectory (scenegraph/subdir/filename.md)
            if len(relevant_parts) > 2:
                # Has subdirectory: scenegraph/subdir/filename.md
                subdir = relevant_parts[1]
                # Map subdirectory name
                mapped_subdir = SCENEGRAPH_SUBDIR_MAP.get(subdir, subdir.replace('-', ' ').title())
                dir_parts.append(mapped_subdir)
            # If len(relevant_parts) == 2, it's a root-level file, no subdirectory to add
                
        # Handle special cases for XML elements
        if 'xml-elements' in relevant_parts:
            # XML elements need special handling for <component>, <interface>, etc.
            if base_filename == 'component':
                filename = '<component>.md'
            elif base_filename == 'interface':
                filename = '<interface>.md'
            elif base_filename == 'script':
                filename = '<script>.md'
            elif base_filename == 'children':
                filename = '<children>.md'
                
        # Handle component functions
        elif 'component-functions' in relevant_parts:
            if base_filename == 'init':
                filename = 'init().md'
            elif base_filename == 'onkeyevent':
                filename = 'onKeyEvent().md'
                
        # Handle special naming for SceneGraph files
        # Convert camelCase to PascalCase for consistency
        if base_dir_name == 'SceneGraph' and not filename.startswith('<'):
            # Capitalize first letter if needed
            if base_filename and base_filename[0].islower():
                filename = base_filename[0].upper() + base_filename[1:] + '.md'
            else:
                filename = base_filename + '.md'
        
        # Ensure filename always has lowercase .md extension
        if filename.endswith('.MD') or filename.endswith('.Md') or filename.endswith('.mD'):
            filename = filename.rsplit('.', 1)[0] + '.md'
        elif not filename.endswith('.md'):
            filename = filename + '.md'
        
        # On case-insensitive filesystems, check if file already exists with different case
        # and use that case instead
        directory = Path(*dir_parts)
        if directory.exists():
            try:
                # Check if a file with similar name already exists
                for existing_file in directory.iterdir():
                    if existing_file.is_file() and existing_file.name.lower() == filename.lower():
                        # Use the existing file's case
                        filename = existing_file.name
                        logger.debug(f"Using existing file case: {filename}")
                        break
            except Exception:
                pass  # If we can't check, just use the generated filename
                
        return directory, filename
        
    def process_element(self, element, content_parts: list, in_list: bool = False):
        """
        Recursively process HTML elements and convert to simplified markdown.
        Matches the existing file format (plain text, minimal formatting).
        """
        # Handle None elements
        if element is None:
            return
            
        if not hasattr(element, 'name') or element.name is None:
            # Text node or element without name
            text = str(element).strip()
            if text:
                content_parts.append(text)
            return
            
        tag_name = element.name.lower()
        
        if tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            text = self.extract_text_with_formatting(element)
            if text:
                # Just the text, no markdown heading syntax (matching existing format)
                content_parts.append(f"{text}\n")
                    
        elif tag_name == 'p':
            text = self.extract_text_with_formatting(element)
            if text:
                content_parts.append(f"{text}\n")
                
        elif tag_name in ['ul', 'ol']:
            items = element.find_all('li', recursive=False)
            for item in items:
                item_text = self.extract_text_with_formatting(item)
                if item_text:
                    # Just the text, no bullet prefix (matching existing format for simple lists)
                    content_parts.append(f"{item_text}\n")
            if items:
                content_parts.append('\n')
                
        elif tag_name == 'li':
            text = self.extract_text_with_formatting(element)
            if text:
                content_parts.append(f"{text}\n")
                
        elif tag_name == 'pre':
            # Check if it contains a code element
            code_elem = element.find('code')
            if code_elem:
                code_text = code_elem.get_text()
                # Preserve the entire code block including metadata like "brush: vb;"
                content_parts.append(f"{code_text}\n")
            else:
                code_text = element.get_text()
                content_parts.append(f"{code_text}\n")
            content_parts.append('\n')
            
        elif tag_name == 'code':
            # Only process if not inside a pre tag (handled above)
            if element.parent and hasattr(element.parent, 'name') and element.parent.name and element.parent.name.lower() != 'pre':
                code_text = element.get_text()
                content_parts.append(code_text)
            # Inside pre, just get text (will be handled by pre)
                
        elif tag_name == 'table':
            # Extract table content - preserve as tab-separated or simple format
            rows = element.find_all('tr')
            if rows:
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if cells:
                        # Use tab separation to preserve table structure
                        row_text = '\t'.join([self.extract_text_with_formatting(c) for c in cells])
                        content_parts.append(f"{row_text}\n")
                content_parts.append('\n')
                
        elif tag_name == 'br':
            content_parts.append('\n')
            
        else:
            # For other elements, recursively process children
            for child in element.children:
                if child is not None:
                    self.process_element(child, content_parts, in_list)
                
    def extract_text_with_formatting(self, element) -> str:
        """
        Extract text from an element, preserving inline formatting (bold, links, etc.)
        Returns plain text matching the existing file format.
        """
        # Handle None elements
        if element is None:
            return ''
            
        if not hasattr(element, 'name') or element.name is None:
            return str(element).strip()
            
        parts = []
        
        for child in element.children:
            # Skip None children
            if child is None:
                continue
                
            # Check if it's an element with a name attribute
            if hasattr(child, 'name') and child.name is not None:
                tag_name = child.name.lower()
                
                if tag_name == 'strong' or tag_name == 'b':
                    text = child.get_text().strip()
                    if text:
                        parts.append(text)  # Just text, no markdown bold (matching existing format)
                elif tag_name == 'em' or tag_name == 'i':
                    text = child.get_text().strip()
                    if text:
                        parts.append(text)  # Just text, no markdown italic
                elif tag_name == 'a':
                    text = child.get_text().strip()
                    if text:
                        # Just use the link text, not the URL (matching existing format)
                        parts.append(text)
                elif tag_name == 'code':
                    code_text = child.get_text()
                    parts.append(code_text)
                elif tag_name in ['br']:
                    parts.append('\n')
                else:
                    # Recursively process other elements
                    child_text = self.extract_text_with_formatting(child)
                    if child_text:
                        parts.append(child_text)
            else:
                # Text node
                text = str(child).strip()
                if text:
                    parts.append(text)
                    
        # Join parts with spaces, but handle newlines specially
        result_parts = []
        for i, part in enumerate(parts):
            if part == '\n':
                result_parts.append('\n')
            else:
                if result_parts and result_parts[-1] != '\n' and not result_parts[-1].endswith('\n'):
                    # Add space between text parts
                    result_parts.append(' ')
                result_parts.append(part)
        
        result = ''.join(result_parts).strip()
        # Normalize multiple spaces but preserve intentional line breaks
        result = re.sub(r'[ \t]+', ' ', result)
        # Normalize multiple newlines (max 2 consecutive)
        result = re.sub(r'\n{3,}', '\n\n', result)
        return result
        
    def html_to_markdown(self, soup: BeautifulSoup) -> str:
        """
        Convert HTML content to markdown, preserving structure.
        Matches the simplified format of existing files.
        """
        content_parts = []
        
        # Process all top-level children
        for element in soup.children:
            if element is not None:
                self.process_element(element, content_parts)
            
        return ''.join(content_parts)
        
    def extract_page_content(self, url: str) -> Optional[str]:
        """
        Navigate to a page and extract the main content.
        Returns the markdown content as a string.
        """
        if url in self.visited_urls:
            logger.debug(f"Skipping already visited URL: {url}")
            return None
            
        logger.info(f"Extracting content from: {url}")
        
        try:
            self.driver.get(url)
            self.visited_urls.add(url)
            
            # Wait for content to load
            content_element = self.wait_for_element(
                By.CSS_SELECTOR,
                ".markdown-body.developer-content-body",
                timeout=30
            )
            
            if not content_element:
                logger.warning(f"Content not found for {url}")
                return None
                
            # Wait a bit more for any dynamic content
            time.sleep(1)
            
            # Get the HTML content
            html_content = content_element.get_attribute('outerHTML')
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "noscript"]):
                script.decompose()
                
            # Convert HTML to markdown
            markdown_content = self.html_to_markdown(soup)
            
            # Clean up excessive blank lines
            markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
            
            # Clean up trailing whitespace on lines
            lines = [line.rstrip() for line in markdown_content.split('\n')]
            markdown_content = '\n'.join(lines)
            
            return markdown_content.strip()
            
        except TimeoutException:
            logger.error(f"Timeout loading page: {url}")
            self.failed_urls.append(url)
            return None
        except Exception as e:
            logger.error(f"Error extracting content from {url}: {e}", exc_info=True)
            self.failed_urls.append(url)
            return None
            
    def save_content(self, content: str, directory: Path, filename: str) -> bool:
        """
        Save content to a file.
        Returns True if saved, False if skipped.
        """
        # Validate inputs
        if directory is None or filename is None:
            logger.error(f"Cannot save: directory={directory}, filename={filename}")
            return False
            
        # Ensure filename doesn't contain path separators
        filename = Path(filename).name
        
        try:
            directory.mkdir(parents=True, exist_ok=True)
        except FileExistsError as e:
            # On case-insensitive filesystems, this can happen if a file exists with similar name
            logger.warning(f"Directory creation conflict for {directory}: {e}")
            # Check if it's actually a file
            if directory.exists() and directory.is_file():
                logger.error(f"Path {directory} exists as a file, cannot create directory")
                return False
            # If it's already a directory, that's fine
            if not directory.is_dir():
                logger.error(f"Path {directory} exists but is not a directory")
                return False
        
        filepath = directory / filename
        
        # Check if file exists and should be skipped
        if self.skip_existing and filepath.exists():
            logger.info(f"Skipping existing file: {filepath}")
            self.skipped_files.append(str(filepath))
            return False
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Saved: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error saving {filepath}: {e}")
            return False
            
    def scrape_all(self, max_retries: int = 3, delay: float = 2.0, mode: str = 'references'):
        """
        Main scraping method. Extracts all links and scrapes each page.
        Args:
            max_retries: Maximum number of retries for failed pages
            delay: Delay between requests in seconds
            mode: 'references' to scrape reference docs, 'developer' to scrape developer docs,
                  'specs' to scrape specifications docs, 'features' to scrape features docs
        """
        try:
            self.setup_driver()
            
            # Determine start URL based on mode
            if mode == 'developer':
                start_url = DEVELOPER_START_URL
            elif mode == 'specs':
                start_url = SPECS_START_URL
            elif mode == 'features':
                start_url = FEATURES_START_URL
            else:
                start_url = REFERENCE_START_URL
            
            # Navigate to start page
            logger.info(f"Navigating to {start_url}")
            self.driver.get(start_url)
            time.sleep(3)  # Wait for page to fully load
            
            # Extract all navigation links
            links = self.extract_navigation_links(mode=mode)
            
            if not links:
                logger.error("No links found. Exiting.")
                return
                
            logger.info(f"Found {len(links)} pages to scrape")
            
            # Scrape each page
            for i, link_info in enumerate(links, 1):
                url = link_info['url']
                logger.info(f"Processing {i}/{len(links)}: {link_info['title']}")
                
                # Extract content
                content = None
                for attempt in range(max_retries):
                    content = self.extract_page_content(url)
                    if content:
                        break
                    if attempt < max_retries - 1:
                        logger.info(f"Retrying {url} (attempt {attempt + 2}/{max_retries})")
                        time.sleep(delay * (attempt + 1))
                        
                if not content:
                    logger.warning(f"Failed to extract content from {url} after {max_retries} attempts")
                    continue
                    
                # Determine file path
                directory, filename = self.url_to_filepath(url)
                
                if not directory or not filename:
                    logger.warning(f"Could not determine file path for {url}")
                    continue
                    
                # Save content
                self.save_content(content, directory, filename)
                
                # Rate limiting
                time.sleep(delay)
                
            # Print summary
            logger.info("\n" + "="*50)
            logger.info("Scraping Summary")
            logger.info("="*50)
            logger.info(f"Total pages found: {len(links)}")
            logger.info(f"Successfully scraped: {len(links) - len(self.failed_urls) - len(self.skipped_files)}")
            if self.skip_existing:
                logger.info(f"Skipped (existing): {len(self.skipped_files)}")
            logger.info(f"Failed: {len(self.failed_urls)}")
            
            if self.failed_urls:
                logger.info("\nFailed URLs:")
                for url in self.failed_urls:
                    logger.info(f"  - {url}")
                    
        except Exception as e:
            logger.error(f"Fatal error during scraping: {e}", exc_info=True)
        finally:
            self.close_driver()


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Scrape Roku developer documentation')
    parser.add_argument('--base-dir', default='.', help='Base directory for output (default: current directory)')
    parser.add_argument('--no-headless', action='store_true', help='Run browser in visible mode')
    parser.add_argument('--skip-existing', action='store_true', help='Skip files that already exist')
    parser.add_argument('--delay', type=float, default=2.0, help='Delay between requests in seconds (default: 2.0)')
    parser.add_argument('--max-retries', type=int, default=3, help='Maximum retries for failed pages (default: 3)')
    parser.add_argument('--mode', choices=['references', 'developer', 'specs', 'features'], default='references',
                       help='Scraping mode: references (default), developer, specs, or features')
    
    args = parser.parse_args()
    
    scraper = RokuDocScraper(
        base_dir=args.base_dir,
        headless=not args.no_headless,
        skip_existing=args.skip_existing
    )
    
    scraper.scrape_all(
        max_retries=args.max_retries,
        delay=args.delay,
        mode=args.mode
    )


if __name__ == '__main__':
    main()
