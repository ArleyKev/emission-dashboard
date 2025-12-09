import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA_DIR = BASE / "data"
CSV_PATH = DATA_DIR / "emissions_fake.csv"

def load_csv_to_df(path: str | Path = None) -> pd.DataFrame:
    p = Path(path) if path else CSV_PATH
    df = pd.read_csv(p)
    df['year'] = df['year'].astype(int)
    df['emissions_tCO2e'] = pd.to_numeric(df['emissions_tCO2e'], errors='coerce').fillna(0)
    return df

_df = None
def get_data():
    global _df
    if _df is None:
        _df = load_csv_to_df()
    return _df
