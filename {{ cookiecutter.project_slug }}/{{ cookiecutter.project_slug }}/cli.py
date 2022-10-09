"""Entry point of CLI."""
{% if cookiecutter.project_category == "Command-Line" -%}
import argparse


def main() -> int:
    """Entry point of CLI."""
    parser = argparse.ArgumentParser()
    parser.parse_args()
    print("Please implement {{ cookiecutter.project_slug }}.cli.main")
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
{%- endif %}
