import pandas as pd
from pathlib import Path


def load_careers():
    """Load career information from the careers CSV file."""

    project_root = Path(__file__).resolve().parent.parent
    file_path = project_root / "data" / "careers.csv"

    careers = pd.read_csv(file_path)

    return careers

if __name__ == "__main__":
    careers = load_careers()

    print("Total careers:", len(careers))
    print("\nFirst 5 careers:")
    print(careers[["career", "domain"]].head())