"""Preprocessing: encode categoricals, scale numerics, encode labels.

Two non-obvious choices documented inline:
1. Categorical features in the test set may contain values never seen in
   train. We use pandas.get_dummies on the *concatenated* feature space so
   both splits end up with identical columns.
2. We standardise (zero mean, unit variance) rather than min-max scale.
   Standardisation is more robust to the long-tailed byte counts in NSL-KDD.
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

from config import CATEGORICAL_FEATURES, CLASS_LABELS


def _split_xy(df):
    X = df.drop(columns=["label"])
    y = df["label"]
    return X, y


def encode_features(train_df, test_df):
    """One-hot encode categoricals over the *union* of train+test categories.

    Why union? The test set contains rare service strings (e.g. ``aol``,
    ``http_2784``) that don't appear in train. If we encoded each split
    independently, the resulting matrices would have different columns and the
    model couldn't be applied to the test set.
    """
    X_train, y_train = _split_xy(train_df)
    X_test, y_test = _split_xy(test_df)

    combined = pd.concat([X_train, X_test], keys=["train", "test"])
    combined_encoded = pd.get_dummies(
        combined,
        columns=CATEGORICAL_FEATURES,
        drop_first=False,
    ).astype(np.float32)

    X_train_enc = combined_encoded.loc["train"].reset_index(drop=True)
    X_test_enc = combined_encoded.loc["test"].reset_index(drop=True)
    return X_train_enc, y_train, X_test_enc, y_test


def scale_features(X_train, X_test):
    """Standardise numeric columns. Fit only on training data — never the test
    set — so we don't leak information about the test distribution.
    """
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, scaler


def encode_labels(y_train, y_test):
    """Map string class labels -> integers in a fixed order.

    Fixing the label order (Normal=0, DoS=1, Probe=2, R2L=3, U2R=4) makes
    confusion-matrix and per-class metric output comparable across runs.
    """
    encoder = LabelEncoder()
    encoder.classes_ = np.array(CLASS_LABELS)
    y_train_enc = np.array([list(CLASS_LABELS).index(y) for y in y_train])
    y_test_enc = np.array([list(CLASS_LABELS).index(y) for y in y_test])
    return y_train_enc, y_test_enc, encoder


def full_pipeline(train_df, test_df):
    """Run the full preprocessing pipeline. Returns:
        X_train, y_train, X_test, y_test, feature_names, label_encoder
    """
    X_train_enc, y_train, X_test_enc, y_test = encode_features(train_df, test_df)
    feature_names = list(X_train_enc.columns)
    X_train_scaled, X_test_scaled, _ = scale_features(X_train_enc, X_test_enc)
    y_train_enc, y_test_enc, label_encoder = encode_labels(y_train, y_test)
    return (
        X_train_scaled,
        y_train_enc,
        X_test_scaled,
        y_test_enc,
        feature_names,
        label_encoder,
    )


if __name__ == "__main__":
    from data_loader import load_nsl_kdd

    train_df, test_df = load_nsl_kdd()
    X_tr, y_tr, X_te, y_te, names, _ = full_pipeline(train_df, test_df)
    print(f"X_train: {X_tr.shape}, y_train: {y_tr.shape}")
    print(f"X_test:  {X_te.shape}, y_test:  {y_te.shape}")
    print(f"# features after one-hot encoding: {len(names)}")
