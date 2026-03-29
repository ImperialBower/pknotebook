"""
Command-line interface for yaml2markdown.
"""

import click
import os
import sys
from .converter import YamlToMarkdownConverter
from .utils import validate_yaml


@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-o', '--output', 'output_file', 
              help='Output Markdown file (default: input_file.md)')
@click.option('-w', '--width', type=int, 
              help='Default width for images in pixels')
@click.option('--no-auto-link', is_flag=True, 
              help='Disable automatic URL to link conversion')
@click.option('--no-table', is_flag=True,
              help='Disable table formatting for arrays of objects')
@click.option('-v', '--verbose', is_flag=True,
              help='Enable verbose output')
def convert(input_file, output_file, width, no_auto_link, no_table, verbose):
    """
    Convert YAML file to Markdown with support for links and images.
    
    INPUT_FILE: Path to the YAML file to convert
    """
    try:
        # Validate input file
        if verbose:
            click.echo(f"Reading YAML file: {input_file}")
        
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not validate_yaml(content):
            click.echo("Error: Invalid YAML file", err=True)
            sys.exit(1)
        
        # Determine output file
        if not output_file:
            base_name = os.path.splitext(input_file)[0]
            output_file = f"{base_name}.md"
        
        if verbose:
            click.echo(f"Output file: {output_file}")
        
        # Create converter with options
        converter = YamlToMarkdownConverter(
            image_width=width,
            auto_link_detection=not no_auto_link,
            table_format=not no_table
        )
        
        # Convert
        if verbose:
            click.echo("Converting YAML to Markdown...")
        
        markdown_content = converter.convert(content)
        
        # Write output
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        click.echo(f"✅ Successfully converted {input_file} to {output_file}")
        
        if verbose:
            click.echo(f"Generated {len(markdown_content)} characters of Markdown")
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@click.group()
def cli():
    """YAML to Markdown Converter - Convert YAML files to Markdown with rich formatting."""
    pass


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
def validate(input_file):
    """Validate a YAML file."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if validate_yaml(content):
            click.echo(f"✅ {input_file} is valid YAML")
        else:
            click.echo(f"❌ {input_file} is not valid YAML")
            sys.exit(1)
    
    except Exception as e:
        click.echo(f"Error reading file: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('yaml_content', required=False)
@click.option('-f', '--file', 'yaml_file', type=click.Path(exists=True),
              help='YAML file to preview')
@click.option('-w', '--width', type=int, default=400,
              help='Default width for images in pixels')
def preview(yaml_content, yaml_file, width):
    """Preview YAML to Markdown conversion."""
    try:
        if yaml_file:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                content = f.read()
        elif yaml_content:
            content = yaml_content
        else:
            click.echo("Please provide either YAML content or use --file option")
            sys.exit(1)
        
        converter = YamlToMarkdownConverter(image_width=width)
        markdown = converter.convert(content)
        
        click.echo("=" * 60)
        click.echo("MARKDOWN PREVIEW")
        click.echo("=" * 60)
        click.echo(markdown)
        click.echo("=" * 60)
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


# Add convert as the default command
cli.add_command(convert)


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == '__main__':
    main()