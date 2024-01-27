import pandas as pd
import argparse
from pathlib import Path
from rich.console import Console
from rich.progress import Progress

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="Convert JSON to CSV")
    parser.add_argument("filename", type=str, help="Path to the JSON file")
    args = parser.parse_args()

    # File existence check
    file_path = Path(args.filename)
    assert file_path.exists(), f"Error: File not found at {file_path}"

    # File extension check
    assert file_path.suffix.lower() == '.json', "Error: File must be a JSON file."

    # Read JSON file to DataFrame
    df = pd.read_json(file_path)

    # Clean column names
    df.columns = (
        df.columns.str.lower()
        .str.replace(' ', '_')
        .str.replace(':', '')
        .str.replace('.', '')
    )

    # Save DataFrame to CSV
    csv_filename = file_path.stem + '.csv'
    csv_path = file_path.with_name(csv_filename)
    
    with Progress() as progress:
        task = progress.add_task("[cyan]Converting to CSV...", total=1)
        df.to_csv(csv_path, index=False)
        progress.update(task, advance=1)

    console = Console()
    console.print(f"[green]Conversion successful. CSV saved at: {csv_path}")

if __name__ == "__main__":
    main()