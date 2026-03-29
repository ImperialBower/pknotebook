"""
Tests for the CLI interface.
"""

import unittest
import tempfile
import os
from click.testing import CliRunner
from yaml2markdown.cli import cli, convert, validate, preview


class TestCLI(unittest.TestCase):
    """Test cases for CLI interface."""
    
    def setUp(self):
        """Set up test cases."""
        self.runner = CliRunner()
    
    def test_convert_command(self):
        """Test the convert command."""
        yaml_content = """
title: "CLI Test"
description: "Testing CLI conversion"
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp_file:
            temp_file.write(yaml_content)
            temp_file.flush()
            
            try:
                result = self.runner.invoke(convert, [temp_file.name])
                
                self.assertEqual(result.exit_code, 0)
                self.assertIn("Successfully converted", result.output)
                
                # Check if output file was created
                output_file = temp_file.name.replace('.yaml', '.md')
                self.assertTrue(os.path.exists(output_file))
                
                # Clean up output file
                if os.path.exists(output_file):
                    os.unlink(output_file)
                    
            finally:
                os.unlink(temp_file.name)
    
    def test_convert_with_custom_output(self):
        """Test convert command with custom output file."""
        yaml_content = """
title: "Custom Output Test"
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp_yaml:
            temp_yaml.write(yaml_content)
            temp_yaml.flush()
            
            with tempfile.NamedTemporaryFile(suffix='.md', delete=False) as temp_md:
                try:
                    result = self.runner.invoke(convert, [
                        temp_yaml.name, 
                        '-o', temp_md.name
                    ])
                    
                    self.assertEqual(result.exit_code, 0)
                    self.assertIn("Successfully converted", result.output)
                    self.assertTrue(os.path.exists(temp_md.name))
                    
                finally:
                    os.unlink(temp_yaml.name)
                    os.unlink(temp_md.name)
    
    def test_validate_command(self):
        """Test the validate command."""
        # Test valid YAML
        valid_yaml = """
title: "Valid YAML"
description: "This is valid"
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp_file:
            temp_file.write(valid_yaml)
            temp_file.flush()
            
            try:
                result = self.runner.invoke(validate, [temp_file.name])
                
                self.assertEqual(result.exit_code, 0)
                self.assertIn("is valid YAML", result.output)
                
            finally:
                os.unlink(temp_file.name)
    
    def test_validate_invalid_yaml(self):
        """Test validate command with invalid YAML."""
        invalid_yaml = """
title: [unclosed
invalid: yaml
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp_file:
            temp_file.write(invalid_yaml)
            temp_file.flush()
            
            try:
                result = self.runner.invoke(validate, [temp_file.name])
                
                self.assertEqual(result.exit_code, 1)
                self.assertIn("is not valid YAML", result.output)
                
            finally:
                os.unlink(temp_file.name)
    
    def test_preview_command(self):
        """Test the preview command."""
        yaml_content = """
title: "Preview Test"
description: "Testing preview functionality"
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp_file:
            temp_file.write(yaml_content)
            temp_file.flush()
            
            try:
                result = self.runner.invoke(preview, ['-f', temp_file.name])
                
                self.assertEqual(result.exit_code, 0)
                self.assertIn("MARKDOWN PREVIEW", result.output)
                self.assertIn("# Title", result.output)
                self.assertIn("Preview Test", result.output)
                
            finally:
                os.unlink(temp_file.name)
    
    def test_preview_with_width(self):
        """Test preview command with custom width."""
        yaml_content = """
image:
  src: "https://example.com/test.jpg"
  alt: "Test Image"
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp_file:
            temp_file.write(yaml_content)
            temp_file.flush()
            
            try:
                result = self.runner.invoke(preview, ['-f', temp_file.name, '-w', '500'])
                
                self.assertEqual(result.exit_code, 0)
                self.assertIn('width="500"', result.output)
                
            finally:
                os.unlink(temp_file.name)
    
    def test_convert_with_options(self):
        """Test convert command with various options."""
        yaml_content = """
title: "Options Test"
link: "https://example.com"
items:
  - name: "A"
    value: 1
  - name: "B"
    value: 2
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp_yaml:
            temp_yaml.write(yaml_content)
            temp_yaml.flush()
            
            try:
                # Test with disabled auto-linking and tables
                result = self.runner.invoke(convert, [
                    temp_yaml.name,
                    '--no-auto-link',
                    '--no-table',
                    '-v'  # verbose
                ])
                
                self.assertEqual(result.exit_code, 0)
                self.assertIn("Successfully converted", result.output)
                self.assertIn("Converting YAML to Markdown", result.output)
                
                # Check the output file content
                output_file = temp_yaml.name.replace('.yaml', '.md')
                with open(output_file, 'r') as f:
                    content = f.read()
                
                # Should not have auto-linked the URL
                self.assertNotIn("[https://example.com]", content)
                # Should not have table format
                self.assertNotIn("| name | value |", content)
                
                # Clean up
                os.unlink(output_file)
                
            finally:
                os.unlink(temp_yaml.name)
    
    def test_nonexistent_file(self):
        """Test with nonexistent file."""
        result = self.runner.invoke(convert, ['nonexistent.yaml'])
        
        self.assertEqual(result.exit_code, 2)  # Click error code for file not found
    
    def test_help_command(self):
        """Test help output."""
        result = self.runner.invoke(cli, ['--help'])
        
        self.assertEqual(result.exit_code, 0)
        self.assertIn("YAML to Markdown Converter", result.output)
        self.assertIn("convert", result.output)
        self.assertIn("validate", result.output)
        self.assertIn("preview", result.output)


if __name__ == '__main__':
    unittest.main()