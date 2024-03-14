import argparse
from pathlib import Path

import pandas as pd
from rich.console import Console
from rich.progress import Progress


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Convert JSON to CSV")
    parser.add_argument("filename", type=str, help="Path to the JSON file")
    return parser.parse_args()


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean column names."""
    return (
        df.columns.str.lower()
        .str.replace(' ', '_')
        .str.replace(':', '')
        .str.replace('.', '')
    )


def create_csv_filepath(json_filepath: Path) -> Path:
    """Create the output CSV filepath."""
    return json_filepath.with_suffix('.csv')


def main():
    """Convert JSON to CSV."""

    # Argument parsing
    args = parse_args()

    # File existence check
    file_path = Path(args.filename)
    assert file_path.exists(), f"Error: File not found at {file_path}"

    # File extension check
    assert file_path.suffix.lower() == '.json',(
        "Error: File must be a JSON file."
    )

    # Read JSON file to DataFrame
    df = pd.read_json(file_path)
    df = clean_data(df)

    # Save DataFrame to CSV
    csv_path = create_csv_filepath(file_path)

    with Progress() as progress:
        task = progress.add_task("[cyan]Converting to CSV...", total=1)
        df.to_csv(csv_path, index=False)  # Save DataFrame to CSV
        progress.update(task, advance=1)

    console = Console()
    console.print(f"[green]Conversion successful. CSV saved at: {csv_path}")


if __name__ == "__main__":
    main()
