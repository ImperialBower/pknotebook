# YAML to Markdown Converter

A Python tool that converts YAML files to beautifully formatted Markdown documents with support for links, images, tables, code blocks, and rich formatting.

## Features

- ✅ **Smart YAML Processing**: Converts any YAML structure to readable Markdown
- 🖼️ **Image Support**: Automatic image embedding with customizable dimensions
- 🔗 **Link Formatting**: Automatic URL detection and link formatting
- 📊 **Table Generation**: Converts arrays of objects to Markdown tables
- 💻 **Code Blocks**: Syntax highlighting for code snippets
- 💬 **Quotes & Blockquotes**: Beautiful formatting for testimonials and quotes
- 🎨 **Rich Formatting**: Headers, lists, and structured content
- 🖥️ **CLI Interface**: Easy-to-use command-line tool
- 🔧 **Programmatic API**: Use in your Python projects

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/devplaybooks/spark4.git

# Navigate to the project
cd spark4/yaml2markdown

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Using pip (when published)

```bash
pip install yaml2markdown
```

## Quick Start

### Command Line Usage

```bash
# Basic conversion
yaml2markdown input.yaml -o output.md

# With custom image width
yaml2markdown input.yaml -o output.md --width 500

# Preview conversion without saving
yaml2markdown preview -f input.yaml

# Validate YAML file
yaml2markdown validate input.yaml
```

### Python API Usage

```python
from yaml2markdown import YamlToMarkdownConverter

# Create converter instance
converter = YamlToMarkdownConverter(
    image_width=400,
    auto_link_detection=True,
    table_format=True
)

# Convert YAML string
yaml_content = """
title: "My Document"
description: "A sample document"
image:
  src: "https://example.com/image.jpg"
  alt: "Sample Image"
  width: 300
"""

markdown = converter.convert(yaml_content)
print(markdown)

# Convert file
markdown = converter.convert_file('input.yaml', 'output.md')
```

## YAML Features and Formatting

### Images

YAML input:

```yaml
image:
  src: "https://example.com/photo.jpg"
  alt: "Description"
  title: "Photo Title"
  width: 400
  caption: "Photo caption"
```

Markdown output:

```markdown
<img src="https://example.com/photo.jpg" alt="Description" title="Photo Title" width="400">

*Photo caption*
```

### Links

YAML input:

```yaml
link:
  text: "Visit GitHub"
  url: "https://github.com"
  title: "GitHub Homepage"
```

Markdown output:

```markdown
[Visit GitHub](https://github.com "GitHub Homepage")
```

### Code Blocks

YAML input:

```yaml
code:
  code: |
    def hello_world():
        print("Hello, World!")
  language: "python"
```

Markdown output:

````markdown
```python
def hello_world():
    print("Hello, World!")
```
````

### Tables

YAML input:

```yaml
products:
  - name: "Product A"
    price: "$10"
    rating: 4.5
  - name: "Product B"
    price: "$15"
    rating: 4.8
```

Markdown output:

```markdown
| name | price | rating |
| --- | --- | --- |
| Product A | $10 | 4.5 |
| Product B | $15 | 4.8 |
```

### Quotes

YAML input:

```yaml
quote:
  quote: "This tool is amazing!"
  author: "Happy User"
```

Markdown output:

```markdown
> This tool is amazing!
>
> — Happy User
```

## CLI Options

```
Usage: yaml2markdown [OPTIONS] INPUT_FILE

Options:
  -o, --output TEXT       Output Markdown file (default: input_file.md)
  -w, --width INTEGER     Default width for images in pixels
  --no-auto-link         Disable automatic URL to link conversion
  --no-table             Disable table formatting for arrays
  -v, --verbose          Enable verbose output
  --help                 Show this message and exit.

Commands:
  convert    Convert YAML file to Markdown (default)
  preview    Preview YAML to Markdown conversion
  validate   Validate a YAML file
```

## Examples

The `examples/` directory contains sample YAML files demonstrating various features:

- **`comprehensive_example.yaml`**: Full-featured documentation example
- **`blog_post.yaml`**: Blog post with images and links
- **`product_catalog.yaml`**: Product catalog with tables and media

Try them out:

```bash
yaml2markdown examples/comprehensive_example.yaml
yaml2markdown examples/blog_post.yaml -w 600
yaml2markdown preview -f examples/product_catalog.yaml
```

## Configuration

The converter supports several configuration options:

```python
converter = YamlToMarkdownConverter(
    image_width=400,           # Default image width in pixels
    auto_link_detection=True,  # Auto-convert URLs to links
    table_format=True          # Format object arrays as tables
)
```

## API Reference

### `YamlToMarkdownConverter`

Main converter class with the following methods:

- **`convert(yaml_content: str) -> str`**: Convert YAML string to Markdown
- **`convert_file(yaml_file: str, output_file: str = None) -> str`**: Convert YAML file

### Utility Functions

- **`validate_yaml(content: str) -> bool`**: Validate YAML syntax
- **`is_url(text: str) -> bool`**: Check if text is a valid URL
- **`is_image_file(url: str) -> bool`**: Check if URL points to an image
- **`format_markdown(text: str) -> str`**: Format and clean Markdown text

## Requirements

- Python 3.8+
- PyYAML >= 6.0
- Click >= 8.0
- Pillow >= 9.0 (for image processing)
- Requests >= 2.28 (for URL handling)

## Development

### Setup Development Environment

```bash
# Clone and setup
git clone https://github.com/devplaybooks/spark4.git
cd spark4/yaml2markdown

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest

# Run tests with coverage
pytest --cov=yaml2markdown
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### v0.1.0 (2025-12-01)

- Initial release
- Basic YAML to Markdown conversion
- Support for images, links, tables, and code blocks
- CLI interface
- Auto-link detection

## Support

- 📖 [Documentation](https://docs.example.com/yaml2markdown)
- 🐛 [Issue Tracker](https://github.com/devplaybooks/spark4/issues)
- 💬 [Discussions](https://github.com/devplaybooks/spark4/discussions)

---

Made with ❤️ by [Christopher Baker](https://github.com/christopher-baker)
