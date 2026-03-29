"""
Utility functions for YAML to Markdown conversion.
"""

import yaml
import re
from typing import Any, Dict, List
from urllib.parse import urlparse


def validate_yaml(content: str) -> bool:
    """
    Validate if string content is valid YAML.
    
    Args:
        content: String to validate
        
    Returns:
        True if valid YAML, False otherwise
    """
    try:
        yaml.safe_load(content)
        return True
    except yaml.YAMLError:
        return False


def is_url(text: str) -> bool:
    """
    Check if text is a valid URL.
    
    Args:
        text: Text to check
        
    Returns:
        True if valid URL, False otherwise
    """
    try:
        result = urlparse(text)
        return all([result.scheme, result.netloc])
    except:
        return False


def is_image_file(url: str) -> bool:
    """
    Check if URL points to an image file.
    
    Args:
        url: URL to check
        
    Returns:
        True if image URL, False otherwise
    """
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp', '.tiff'}
    
    try:
        parsed = urlparse(url)
        path = parsed.path.lower()
        return any(path.endswith(ext) for ext in image_extensions)
    except:
        return False


def format_markdown_table(data: List[Dict[str, Any]], columns: List[str]) -> str:
    """
    Format list of dictionaries as a Markdown table.
    
    Args:
        data: List of dictionaries
        columns: Column names to include
        
    Returns:
        Markdown table string
    """
    if not data or not columns:
        return ""
    
    # Create header
    header = "| " + " | ".join(columns) + " |"
    separator = "|" + "|".join([" --- " for _ in columns]) + "|"
    
    # Create rows
    rows = []
    for item in data:
        row_values = []
        for col in columns:
            value = item.get(col, "")
            # Escape pipes and newlines for table format
            value_str = str(value).replace("|", "\\|").replace("\n", " ")
            row_values.append(value_str)
        
        row = "| " + " | ".join(row_values) + " |"
        rows.append(row)
    
    # Combine all parts
    table_parts = [header, separator] + rows
    return "\n".join(table_parts)


def clean_markdown(text: str) -> str:
    """
    Clean and format Markdown text.
    
    Args:
        text: Markdown text to clean
        
    Returns:
        Cleaned Markdown text
    """
    # Remove excessive blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Ensure proper spacing around headers
    text = re.sub(r'\n(#{1,6}\s)', r'\n\n\1', text)
    text = re.sub(r'(#{1,6}\s.*)\n([^#\n])', r'\1\n\n\2', text)
    
    return text.strip()


def escape_markdown(text: str) -> str:
    """
    Escape special Markdown characters in text.
    
    Args:
        text: Text to escape
        
    Returns:
        Escaped text
    """
    # Characters that need escaping in Markdown
    escape_chars = r'\\`*_{}[]()#+-.!'
    
    for char in escape_chars:
        text = text.replace(char, f'\\{char}')
    
    return text


def format_markdown(text: str, auto_clean: bool = True) -> str:
    """
    Format and optionally clean Markdown text.
    
    Args:
        text: Markdown text to format
        auto_clean: Whether to automatically clean the text
        
    Returns:
        Formatted Markdown text
    """
    if auto_clean:
        text = clean_markdown(text)
    
    return text