import pandas as pd
import sys
from pathlib import Path
import os
import json
from rich import print

def main():
    # read in argument
    filename = sys.argv[1]
    path = Path(filename)
    assert os.path.exists(path), "File not found."
    assert filename.endswith('.json'), "File must be a json file."
    
    csv_filename = filename[:-4] + 'csv'
    csv_path = Path(csv_filename)
    df = pd.read_json(path)
    df.to_csv(csv_path, index=False)

if __name__ == "__main__":
    main()
