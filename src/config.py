"""Shared paths and settings used across notebooks."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"
FIGURES_DIR = ROOT / "reports" / "figures"

PG19_BASE_URL = "https://storage.googleapis.com/deepmind-gutenberg"
METADATA_PATH = RAW_DIR / "metadata.csv"

# Single seed for every split, sample and model so results are reproducible.
RANDOM_STATE = 42
TEST_SIZE = 0.2
CV_FOLDS = 5
