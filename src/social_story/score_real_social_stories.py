import pandas as pd
from pathlib import Path

CSV_PATH = Path(__file__).parent / "social_story_dataset.csv"
df = pd.read_csv(CSV_PATH)

for i,row in df.iterrows:
