"""
Core converter module for YAML to Markdown conversion.
"""

import yaml
import re
from typing import Any, Dict, List, Union
from urllib.parse import urlparse
import os
from .utils import is_url, is_image_file, format_markdown_table


class YamlToMarkdownConverter:
    """
    Converts YAML content to Markdown with support for links, images, and rich formatting.
    """
    
    def __init__(self, 
                 image_width: int = None, 
                 auto_link_detection: bool = True,
                 table_format: bool = True):
        """
        Initialize the converter.
        
        Args:
            image_width: Default width for images (pixels)
            auto_link_detection: Automatically convert URLs to links
            table_format: Format arrays of objects as tables
        """
        self.image_width = image_width
        self.auto_link_detection = auto_link_detection
        self.table_format = table_format
        
    def convert(self, yaml_content: str) -> str:
        """
        Convert YAML content to Markdown.
        
        Args:
            yaml_content: YAML string to convert
            
        Returns:
            Formatted Markdown string
        """
        try:
            data = yaml.safe_load(yaml_content)
            if data is None:
                return ""
            
            return self._process_value(data)
            
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML content: {e}")
    
    def convert_file(self, yaml_file: str, output_file: str = None) -> str:
        """
        Convert YAML file to Markdown.
        
        Args:
            yaml_file: Path to input YAML file
            output_file: Path to output Markdown file (optional)
            
        Returns:
            Markdown content
        """
        with open(yaml_file, 'r', encoding='utf-8') as f:
            yaml_content = f.read()
        
        markdown_content = self.convert(yaml_content)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
        
        return markdown_content
    
    def _process_value(self, value: Any, level: int = 1) -> str:
        """
        Process a value and convert it to Markdown format.
        
        Args:
            value: Value to process
            level: Heading level for nested structures
            
        Returns:
            Markdown formatted string
        """
        if isinstance(value, dict):
            return self._process_dict(value, level)
        elif isinstance(value, list):
            return self._process_list(value, level)
        else:
            return self._process_scalar(value)
    
    def _process_dict(self, data: Dict[str, Any], level: int = 1) -> str:
        """Process dictionary and convert to Markdown."""
        result = []
        
        for key, value in data.items():
            # Create heading for the key
            heading = "#" * min(level, 6) + " " + self._format_key(key)
            result.append(heading)
            result.append("")
            
            # Process the value
            if isinstance(value, dict):
                # Check if this looks like a special object (link, image, etc.)
                processed = self._process_special_dict(value)
                if processed:
                    result.append(processed)
                else:
                    result.append(self._process_dict(value, level + 1))
            elif isinstance(value, list):
                result.append(self._process_list(value, level + 1))
            else:
                result.append(self._process_scalar(value))
            
            result.append("")
        
        return "\n".join(result).strip()
    
    def _process_list(self, data: List[Any], level: int = 1) -> str:
        """Process list and convert to Markdown."""
        if not data:
            return ""
        
        # Check if this is a list of dictionaries with similar structure (table format)
        if (self.table_format and 
            all(isinstance(item, dict) for item in data) and
            len(data) > 1):
            
            # Get all unique keys from all dictionaries
            all_keys = set()
            for item in data:
                all_keys.update(item.keys())
            
            if all_keys and len(all_keys) <= 10:  # Reasonable table size
                return format_markdown_table(data, list(all_keys))
        
        # Regular list processing
        result = []
        for item in data:
            if isinstance(item, dict):
                # Check for special dict formats
                processed = self._process_special_dict(item)
                if processed:
                    result.append(f"- {processed}")
                else:
                    # Nested dictionary in list
                    nested = self._process_dict(item, level + 1)
                    if nested:
                        result.append(f"- **Item:**")
                        # Indent the nested content
                        indented = "\n".join(f"  {line}" for line in nested.split("\n"))
                        result.append(indented)
            elif isinstance(item, list):
                # Nested list
                nested = self._process_list(item, level + 1)
                result.append(f"- {nested}")
            else:
                result.append(f"- {self._process_scalar(item)}")
        
        return "\n".join(result)
    
    def _process_special_dict(self, data: Dict[str, Any]) -> str:
        """
        Check if dictionary represents a special object (link, image, etc.) and format accordingly.
        
        Args:
            data: Dictionary to check
            
        Returns:
            Formatted string if special object, None otherwise
        """
        # Check for image object
        if 'image' in data or 'img' in data or 'src' in data:
            return self._format_image(data)
        
        # Check for link object
        if 'link' in data or 'url' in data or 'href' in data:
            return self._format_link(data)
        
        # Check for code block
        if 'code' in data:
            return self._format_code(data)
        
        # Check for quote/blockquote
        if 'quote' in data or 'blockquote' in data:
            return self._format_quote(data)
        
        return None
    
    def _format_image(self, data: Dict[str, Any]) -> str:
        """Format image dictionary as Markdown image."""
        # Get image source
        src = data.get('image') or data.get('img') or data.get('src', '')
        
        # Get alt text
        alt = data.get('alt', data.get('title', data.get('description', 'Image')))
        
        # Get title
        title = data.get('title', '')
        
        # Check if width is specified
        width = data.get('width', self.image_width)
        
        # Format the image
        if title:
            img_md = f"![{alt}]({src} \"{title}\")"
        else:
            img_md = f"![{alt}]({src})"
        
        # Add HTML width attribute if specified
        if width:
            img_md = f'<img src="{src}" alt="{alt}" width="{width}">'
            if title:
                img_md = f'<img src="{src}" alt="{alt}" title="{title}" width="{width}">'
        
        # Add caption if provided
        caption = data.get('caption', data.get('description'))
        if caption and caption != alt:
            img_md += f"\n\n*{caption}*"
        
        return img_md
    
    def _format_link(self, data: Dict[str, Any]) -> str:
        """Format link dictionary as Markdown link."""
        # Get URL
        url = data.get('link') or data.get('url') or data.get('href', '')
        
        # Get link text
        text = data.get('text', data.get('title', data.get('name', url)))
        
        # Get title/tooltip
        title = data.get('title', data.get('tooltip'))
        
        # Format the link
        if title and title != text:
            return f"[{text}]({url} \"{title}\")"
        else:
            return f"[{text}]({url})"
    
    def _format_code(self, data: Dict[str, Any]) -> str:
        """Format code dictionary as Markdown code block."""
        code = data.get('code', '')
        language = data.get('language', data.get('lang', ''))
        
        if language:
            return f"```{language}\n{code}\n```"
        else:
            return f"```\n{code}\n```"
    
    def _format_quote(self, data: Dict[str, Any]) -> str:
        """Format quote dictionary as Markdown blockquote."""
        quote = data.get('quote') or data.get('blockquote', '')
        author = data.get('author', data.get('source', ''))
        
        # Format blockquote
        lines = quote.split('\n')
        quote_md = '\n'.join(f"> {line}" for line in lines)
        
        # Add author attribution
        if author:
            quote_md += f"\n>\n> — {author}"
        
        return quote_md
    
    def _process_scalar(self, value: Any) -> str:
        """Process scalar value and apply auto-formatting."""
        if value is None:
            return ""
        
        text = str(value)
        
        # Auto-link detection
        if self.auto_link_detection:
            text = self._auto_link_text(text)
        
        return text
    
    def _auto_link_text(self, text: str) -> str:
        """Automatically convert URLs to links and image URLs to images."""
        # URL pattern
        url_pattern = r'(https?://[^\s\)]+)'
        
        def replace_url(match):
            url = match.group(1)
            
            # Check if it's an image URL
            if is_image_file(url):
                return f"![Image]({url})"
            else:
                return f"[{url}]({url})"
        
        return re.sub(url_pattern, replace_url, text)
    
    def _format_key(self, key: str) -> str:
        """Format dictionary key as a readable title."""
        # Replace underscores and hyphens with spaces
        formatted = key.replace('_', ' ').replace('-', ' ')
        
        # Convert to title case
        formatted = formatted.title()
        
        return formatted