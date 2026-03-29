"""
Tests for the yaml2markdown package.
"""

import unittest
import tempfile
import os
from yaml2markdown import YamlToMarkdownConverter, validate_yaml, format_markdown
from yaml2markdown.utils import is_url, is_image_file, format_markdown_table


class TestYamlToMarkdownConverter(unittest.TestCase):
    """Test cases for YamlToMarkdownConverter class."""
    
    def setUp(self):
        """Set up test cases."""
        self.converter = YamlToMarkdownConverter()
    
    def test_simple_yaml_conversion(self):
        """Test basic YAML to Markdown conversion."""
        yaml_content = """
title: "Test Document"
description: "A test document"
        """
        
        result = self.converter.convert(yaml_content)
        
        self.assertIn("# Title", result)
        self.assertIn("Test Document", result)
        self.assertIn("# Description", result)
        self.assertIn("A test document", result)
    
    def test_image_conversion(self):
        """Test image object conversion."""
        yaml_content = """
header_image:
  src: "https://example.com/image.jpg"
  alt: "Test Image"
  width: 400
  caption: "A test image"
        """
        
        result = self.converter.convert(yaml_content)
        
        self.assertIn('<img src="https://example.com/image.jpg"', result)
        self.assertIn('alt="Test Image"', result)
        self.assertIn('width="400"', result)
        self.assertIn("*A test image*", result)
    
    def test_link_conversion(self):
        """Test link object conversion."""
        yaml_content = """
website:
  text: "Visit GitHub"
  url: "https://github.com"
  title: "GitHub Homepage"
        """
        
        result = self.converter.convert(yaml_content)
        
        self.assertIn('[Visit GitHub](https://github.com "GitHub Homepage")', result)
    
    def test_code_block_conversion(self):
        """Test code block conversion."""
        yaml_content = """
example:
  code: |
    def hello():
        print("Hello World")
  language: "python"
        """
        
        result = self.converter.convert(yaml_content)
        
        self.assertIn("```python", result)
        self.assertIn("def hello():", result)
        self.assertIn('print("Hello World")', result)
    
    def test_quote_conversion(self):
        """Test quote/blockquote conversion."""
        yaml_content = """
testimonial:
  quote: "This is a great tool!"
  author: "Happy User"
        """
        
        result = self.converter.convert(yaml_content)
        
        self.assertIn("> This is a great tool!", result)
        self.assertIn("> — Happy User", result)
    
    def test_list_conversion(self):
        """Test list conversion."""
        yaml_content = """
features:
  - "Easy to use"
  - "Fast conversion"
  - "Rich formatting"
        """
        
        result = self.converter.convert(yaml_content)
        
        self.assertIn("- Easy to use", result)
        self.assertIn("- Fast conversion", result)
        self.assertIn("- Rich formatting", result)
    
    def test_table_conversion(self):
        """Test table conversion from list of objects."""
        yaml_content = """
products:
  - name: "Product A"
    price: "$10"
  - name: "Product B" 
    price: "$20"
        """
        
        result = self.converter.convert(yaml_content)
        
        self.assertIn("| name | price |", result)
        self.assertIn("| Product A | $10 |", result)
        self.assertIn("| Product B | $20 |", result)
    
    def test_auto_link_detection(self):
        """Test automatic link detection."""
        yaml_content = """
description: "Visit https://example.com for more info"
        """
        
        result = self.converter.convert(yaml_content)
        
        self.assertIn("[https://example.com](https://example.com)", result)
    
    def test_auto_image_detection(self):
        """Test automatic image detection from URLs."""
        yaml_content = """
description: "Check out https://example.com/image.jpg"
        """
        
        result = self.converter.convert(yaml_content)
        
        self.assertIn("![Image](https://example.com/image.jpg)", result)
    
    def test_file_conversion(self):
        """Test file-based conversion."""
        yaml_content = """
title: "File Test"
description: "Testing file conversion"
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp_yaml:
            temp_yaml.write(yaml_content)
            temp_yaml.flush()
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as temp_md:
                try:
                    result = self.converter.convert_file(temp_yaml.name, temp_md.name)
                    
                    # Check that file was created and contains expected content
                    self.assertTrue(os.path.exists(temp_md.name))
                    
                    with open(temp_md.name, 'r') as f:
                        content = f.read()
                    
                    self.assertIn("# Title", content)
                    self.assertIn("File Test", content)
                    
                finally:
                    # Clean up
                    os.unlink(temp_yaml.name)
                    os.unlink(temp_md.name)
    
    def test_invalid_yaml(self):
        """Test handling of invalid YAML."""
        invalid_yaml = """
title: "Test
invalid: [unclosed
        """
        
        with self.assertRaises(ValueError):
            self.converter.convert(invalid_yaml)


class TestUtilityFunctions(unittest.TestCase):
    """Test cases for utility functions."""
    
    def test_validate_yaml(self):
        """Test YAML validation."""
        valid_yaml = "title: 'Test'"
        invalid_yaml = "title: [unclosed"
        
        self.assertTrue(validate_yaml(valid_yaml))
        self.assertFalse(validate_yaml(invalid_yaml))
    
    def test_is_url(self):
        """Test URL detection."""
        self.assertTrue(is_url("https://example.com"))
        self.assertTrue(is_url("http://example.com"))
        self.assertFalse(is_url("not-a-url"))
        self.assertFalse(is_url("example.com"))  # No protocol
    
    def test_is_image_file(self):
        """Test image file detection."""
        self.assertTrue(is_image_file("https://example.com/image.jpg"))
        self.assertTrue(is_image_file("https://example.com/image.png"))
        self.assertTrue(is_image_file("https://example.com/image.gif"))
        self.assertFalse(is_image_file("https://example.com/document.pdf"))
        self.assertFalse(is_image_file("https://example.com/"))
    
    def test_format_markdown_table(self):
        """Test Markdown table formatting."""
        data = [
            {"name": "John", "age": 30},
            {"name": "Jane", "age": 25}
        ]
        columns = ["name", "age"]
        
        result = format_markdown_table(data, columns)
        
        self.assertIn("| name | age |", result)
        self.assertIn("| --- | --- |", result)
        self.assertIn("| John | 30 |", result)
        self.assertIn("| Jane | 25 |", result)
    
    def test_format_markdown(self):
        """Test Markdown formatting and cleaning."""
        messy_markdown = """


# Title


Some content



## Subtitle

More content


        """
        
        result = format_markdown(messy_markdown)
        
        # Should remove excessive blank lines
        self.assertNotIn("\n\n\n", result)
        self.assertIn("# Title", result)
        self.assertIn("## Subtitle", result)


class TestConverterOptions(unittest.TestCase):
    """Test cases for converter configuration options."""
    
    def test_disable_auto_link(self):
        """Test disabling auto-link detection."""
        converter = YamlToMarkdownConverter(auto_link_detection=False)
        
        yaml_content = """
description: "Visit https://example.com"
        """
        
        result = converter.convert(yaml_content)
        
        # Should not convert to link
        self.assertNotIn("[https://example.com]", result)
        self.assertIn("https://example.com", result)
    
    def test_disable_table_format(self):
        """Test disabling table formatting."""
        converter = YamlToMarkdownConverter(table_format=False)
        
        yaml_content = """
items:
  - name: "A"
    value: 1
  - name: "B"
    value: 2
        """
        
        result = converter.convert(yaml_content)
        
        # Should not create table
        self.assertNotIn("| name | value |", result)
        # Should create list instead
        self.assertIn("- **Item:**", result)
    
    def test_custom_image_width(self):
        """Test custom image width setting."""
        converter = YamlToMarkdownConverter(image_width=600)
        
        yaml_content = """
photo:
  src: "https://example.com/photo.jpg"
  alt: "Photo"
        """
        
        result = converter.convert(yaml_content)
        
        self.assertIn('width="600"', result)


if __name__ == '__main__':
    unittest.main()