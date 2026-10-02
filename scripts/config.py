from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_DIR = BASE_DIR / "dataset"
OUTPUT_DIR = BASE_DIR / "output"

INPUT_FILE = DATASET_DIR / "FraudLens_30000.csv"

OUTPUT_DIR.mkdir(exist_ok=True)