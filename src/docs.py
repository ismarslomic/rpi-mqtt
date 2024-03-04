#!/usr/bin/env python3
"""Auto generate documentation"""

from settings.settings import write_model_to_json, write_model_to_mkd


def main():
    """Generate documentation to the docs folder"""

    print("Generating Settings model as JSON schema and Markdown file in docs folder")
    write_model_to_json()
    write_model_to_mkd()


if __name__ == "__main__":
    main()
