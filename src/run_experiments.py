"""End-to-end experiment runner.

Pipeline:
    1. Load NSL-KDD train/test.
    2. Encode categoricals + scale features.
    3. For each of {LR, RF, XGBoost}:
         a. Stratified k-fold CV on the training set with SMOTE applied to
            each fold's training side only (never the validation side).
         b. Final fit on the full SMOTE-resampled training set.
         c. Evaluate on the held-out KDDTest+ split.
    4. Save metrics, confusion matrices, feature-importance plots,
       comparison.csv and a class-distribution figure.
"""
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from imblearn.over_sampling import SMOTE
from sklearn.base import clone
from sklearn.model_selection import StratifiedKFold

from config import CLASS_LABELS, CV_FOLDS, FIGURES_DIR, RANDOM_SEED, RESULTS_DIR
from data_loader import class_distribution, load_nsl_kdd
from evaluate import (
    overall_metrics,
    per_class_table,
    plot_confusion_matrix,
    plot_feature_importance,
    save_results,
    write_comparison_table,
)
from models import build_models
from preprocess import full_pipeline


def cv_with_smote(model, X, y, cv_folds=CV_FOLDS):
    """Run stratified k-fold CV with SMOTE applied per fold.

    SMOTE must run *inside* the CV loop, on the training side only, otherwise
    synthetic minority samples leak into validation and inflate scores.
    """
    skf = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=RANDOM_SEED)
    fold_scores = []
    for fold_idx, (tr_idx, va_idx) in enumerate(skf.split(X, y), start=1):
        X_tr, X_va = X[tr_idx], X[va_idx]
        y_tr, y_va = y[tr_idx], y[va_idx]

        # SMOTE k_neighbors must be <= (smallest class count - 1). U2R has
        # only ~52 samples in train, so 5 neighbours is a safe default but we
        # still clamp defensively.
        min_count = pd.Series(y_tr).value_counts().min()
        k = max(1, min(5, min_count - 1))
        sm = SMOTE(random_state=RANDOM_SEED, k_neighbors=k)
        X_tr_res, y_tr_res = sm.fit_resample(X_tr, y_tr)

        m = clone(model)
        m.fit(X_tr_res, y_tr_res)
        y_pred = m.predict(X_va)
        from sklearn.metrics import f1_score
        fold_scores.append(
            f1_score(y_va, y_pred, average="weighted", zero_division=0)
        )
        print(f"    fold {fold_idx}/{cv_folds}: weighted F1 = {fold_scores[-1]:.4f}")
    return float(np.mean(fold_scores)), float(np.std(fold_scores))


def plot_class_distribution(train_df, test_df, save_path):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    for ax, df, title in zip(axes, [train_df, test_df], ["KDDTrain+", "KDDTest+"]):
        counts = df["label"].value_counts().reindex(CLASS_LABELS)
        ax.bar(counts.index, counts.values, color="steelblue")
        ax.set_title(title)
        ax.set_yscale("log")
        for i, v in enumerate(counts.values):
            ax.text(i, v, f"{int(v):,}", ha="center", va="bottom", fontsize=9)
    fig.suptitle("Class distribution (log scale)", fontsize=12)
    fig.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    print("[1/4] Loading NSL-KDD...")
    train_df, test_df = load_nsl_kdd()
    print(class_distribution(train_df, "train"))
    print(class_distribution(test_df, "test"))
    plot_class_distribution(train_df, test_df, FIGURES_DIR / "class_distribution.png")

    print("\n[2/4] Preprocessing...")
    X_train, y_train, X_test, y_test, feature_names, _ = full_pipeline(
        train_df, test_df
    )
    print(f"Feature matrix: train {X_train.shape}, test {X_test.shape}")

    print("\n[3/4] Pre-resampling training set with SMOTE for the final fit...")
    sm = SMOTE(random_state=RANDOM_SEED, k_neighbors=5)
    X_train_smote, y_train_smote = sm.fit_resample(X_train, y_train)
    print(
        f"After SMOTE: {X_train_smote.shape[0]:,} rows "
        f"(class counts: {dict(pd.Series(y_train_smote).value_counts().sort_index())})"
    )

    print("\n[4/4] Training and evaluating models...")
    models = build_models()
    comparison_rows = []

    for name, model in models.items():
        print(f"\n--- {name} ---")
        t0 = time.time()
        print(f"  Cross-validating ({CV_FOLDS}-fold, SMOTE per fold)...")
        cv_mean, cv_std = cv_with_smote(model, X_train, y_train, cv_folds=CV_FOLDS)
        print(f"  CV weighted F1: {cv_mean:.4f} ± {cv_std:.4f}")

        print("  Fitting on full SMOTE-resampled train set...")
        model.fit(X_train_smote, y_train_smote)

        print("  Predicting on KDDTest+...")
        y_pred = model.predict(X_test)
        try:
            y_proba = model.predict_proba(X_test)
        except AttributeError:
            y_proba = None

        overall = overall_metrics(y_test, y_pred, y_proba)
        per_class = per_class_table(y_test, y_pred)
        train_seconds = time.time() - t0
        overall.update(
            {
                "model": name,
                "cv_f1_weighted_mean": cv_mean,
                "cv_f1_weighted_std": cv_std,
                "wall_time_seconds": round(train_seconds, 1),
            }
        )

        save_results(name, overall, per_class, predictions=y_pred)
        plot_confusion_matrix(
            y_test, y_pred, name,
            FIGURES_DIR / f"cm_{name.lower().replace(' ', '_')}.png",
        )

        if hasattr(model, "feature_importances_"):
            plot_feature_importance(
                feature_names,
                model.feature_importances_,
                name,
                FIGURES_DIR / f"fi_{name.lower().replace(' ', '_')}.png",
            )
        elif hasattr(model, "coef_"):
            plot_feature_importance(
                feature_names,
                np.abs(model.coef_).mean(axis=0),
                name,
                FIGURES_DIR / f"fi_{name.lower().replace(' ', '_')}.png",
            )

        comparison_rows.append(overall)
        print(
            f"  Test accuracy: {overall['accuracy']:.4f}  |  "
            f"weighted F1: {overall['f1_weighted']:.4f}  |  "
            f"macro F1: {overall['f1_macro']:.4f}  |  "
            f"time: {train_seconds:.1f}s"
        )
        print("  Per-class:")
        print(per_class.round(4).to_string())

    print("\n=== FINAL COMPARISON ===")
    df = write_comparison_table(comparison_rows)
    cols = ["model", "accuracy", "precision_weighted", "recall_weighted",
            "f1_weighted", "f1_macro", "roc_auc_ovr", "wall_time_seconds"]
    print(df[cols].round(4).to_string(index=False))
    print(f"\nResults saved to: {RESULTS_DIR}")
    print(f"Figures saved to: {FIGURES_DIR}")


if __name__ == "__main__":
    main()
