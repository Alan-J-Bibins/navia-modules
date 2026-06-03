import pandas as pd
import json
from pathlib import Path
from activities.social_story.model import SocialStoryScoreResponse
from activities.social_story.judge import judge_social_story

CSV_PATH = Path(__file__).parent / "social_story_dataset.csv"
CHECKPOINT_PATH = Path(__file__).parent / "scoring_checkpoint.json"
OUTPUT_PATH = Path(__file__).parent / "social_story_scored.csv"
df = pd.read_csv(CSV_PATH)
# --- Load checkpoint if it exists ---
scores_0, remarks_0 = [], []
scores_1, remarks_1 = [], []
start_idx = 0
if CHECKPOINT_PATH.exists():
    with open(CHECKPOINT_PATH, "r") as f:
        ckpt = json.load(f)
    scores_0 = ckpt.get("scores_0", [])
    remarks_0 = ckpt.get("remarks_0", [])
    scores_1 = ckpt.get("scores_1", [])
    remarks_1 = ckpt.get("remarks_1", [])
    start_idx = ckpt.get("last_idx", -1) + 1
    print(
        f"Resuming from row index {start_idx} (already processed {len(scores_0)} rows)"
    )
# --- Scoring loop ---
for idx, row in df.iloc[start_idx:].iterrows():
    title = row["title"]
    content = row["content"]
    min_age = int(row["min_age"])
    result0 = judge_social_story(
        story_schema=f"{title}\n{content}", age=min_age, judge=0
    )
    result1 = judge_social_story(
        story_schema=f"{title}\n{content}", age=min_age, judge=2
    )
    scores_0.append(
        result0.score if isinstance(result0, SocialStoryScoreResponse) else -1
    )
    remarks_0.append(
        result0.remarks if isinstance(result0, SocialStoryScoreResponse) else ""
    )
    scores_1.append(
        result1.score if isinstance(result1, SocialStoryScoreResponse) else -1
    )
    remarks_1.append(
        result1.remarks if isinstance(result1, SocialStoryScoreResponse) else ""
    )
    # --- Save checkpoint after every row ---
    ckpt = {
        "last_idx": int(idx),
        "scores_0": scores_0,
        "remarks_0": remarks_0,
        "scores_1": scores_1,
        "remarks_1": remarks_1,
    }
    with open(CHECKPOINT_PATH, "w") as f:
        json.dump(ckpt, f)
    print(f"Processed row {idx} ({len(scores_0)} total done)")
# --- Final write ---
df["judge_score_0"] = scores_0
df["judge_remarks_0"] = remarks_0
df["judge_score_1"] = scores_1
df["judge_remarks_1"] = remarks_1
df.to_csv(OUTPUT_PATH, index=False)
print(f"Done! Scored CSV saved to {OUTPUT_PATH}")
# Clean up checkpoint after successful completion
CHECKPOINT_PATH.unlink(missing_ok=True)
