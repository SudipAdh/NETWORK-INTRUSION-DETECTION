"""Load and label-map the NSL-KDD dataset.

The raw .txt files are headerless CSVs. We attach proper column names, drop
the difficulty score (we're not doing difficulty-stratified analysis), and
collapse the 22 specific attack names into 5 high-level categories.
"""
import pandas as pd

from config import (
    ATTACK_TO_CATEGORY,
    NSL_KDD_COLUMNS,
    TEST_FILE,
    TRAIN_FILE,
)


def _load_split(path):
    df = pd.read_csv(path, header=None, names=NSL_KDD_COLUMNS)
    # Drop difficulty — useful for some studies, irrelevant for ours.
    df = df.drop(columns=["difficulty"])
    # Map raw attack name -> 5-class category. Unknown attacks default to R2L
    # because the U2R/R2L families are where unseen NSL-KDD test attacks fall.
    df["label"] = df["label"].map(lambda x: ATTACK_TO_CATEGORY.get(x, "R2L"))
    return df


def load_nsl_kdd():
    """Return (train_df, test_df) with 5-class labels."""
    train_df = _load_split(TRAIN_FILE)
    test_df = _load_split(TEST_FILE)
    return train_df, test_df


def class_distribution(df, name=""):
    """Return a small summary table of class counts and percentages."""
    counts = df["label"].value_counts()
    total = counts.sum()
    summary = pd.DataFrame(
        {
            "samples": counts,
            "percent": (counts / total * 100).round(2),
        }
    )
    summary.index.name = f"class ({name})" if name else "class"
    return summary


if __name__ == "__main__":
    train_df, test_df = load_nsl_kdd()
    print(f"Train shape: {train_df.shape}")
    print(f"Test shape:  {test_df.shape}")
    print()
    print("Train class distribution:")
    print(class_distribution(train_df, "train"))
    print()
    print("Test class distribution:")
    print(class_distribution(test_df, "test"))
