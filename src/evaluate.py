"""Evaluation utilities: metrics, confusion matrix, ROC-AUC, feature importance.

We compute metrics in one place so the experiment script stays short and so
results are reported consistently across all three models.
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.preprocessing import label_binarize

from config import CLASS_LABELS, FIGURES_DIR, RESULTS_DIR


def overall_metrics(y_true, y_pred, y_proba=None):
    """Return a dict of single-number metrics suitable for the comparison table."""
    metrics = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision_weighted": float(
            precision_score(y_true, y_pred, average="weighted", zero_division=0)
        ),
        "recall_weighted": float(
            recall_score(y_true, y_pred, average="weighted", zero_division=0)
        ),
        "f1_weighted": float(
            f1_score(y_true, y_pred, average="weighted", zero_division=0)
        ),
        "f1_macro": float(
            f1_score(y_true, y_pred, average="macro", zero_division=0)
        ),
    }
    if y_proba is not None:
        try:
            y_true_bin = label_binarize(y_true, classes=list(range(len(CLASS_LABELS))))
            metrics["roc_auc_ovr"] = float(
                roc_auc_score(y_true_bin, y_proba, average="weighted", multi_class="ovr")
            )
        except ValueError:
            metrics["roc_auc_ovr"] = None
    return metrics


def per_class_table(y_true, y_pred):
    """Return a DataFrame of per-class precision / recall / F1 / support."""
    report = classification_report(
        y_true,
        y_pred,
        target_names=CLASS_LABELS,
        output_dict=True,
        zero_division=0,
    )
    rows = {cls: report[cls] for cls in CLASS_LABELS}
    return pd.DataFrame(rows).T[["precision", "recall", "f1-score", "support"]]


def plot_confusion_matrix(y_true, y_pred, model_name, save_path):
    cm = confusion_matrix(y_true, y_pred, labels=list(range(len(CLASS_LABELS))))
    cm_norm = cm.astype(float) / cm.sum(axis=1, keepdims=True).clip(min=1)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=CLASS_LABELS,
        yticklabels=CLASS_LABELS,
        ax=axes[0],
        cbar=False,
    )
    axes[0].set_title(f"{model_name} — counts")
    axes[0].set_xlabel("Predicted")
    axes[0].set_ylabel("Actual")
    sns.heatmap(
        cm_norm,
        annot=True,
        fmt=".2f",
        cmap="Blues",
        xticklabels=CLASS_LABELS,
        yticklabels=CLASS_LABELS,
        ax=axes[1],
        cbar=False,
    )
    axes[1].set_title(f"{model_name} — row-normalised (recall per class)")
    axes[1].set_xlabel("Predicted")
    axes[1].set_ylabel("Actual")
    fig.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_feature_importance(feature_names, importances, model_name, save_path, top_k=15):
    order = np.argsort(importances)[::-1][:top_k]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(
        [feature_names[i] for i in order][::-1],
        [importances[i] for i in order][::-1],
        color="steelblue",
    )
    ax.set_title(f"Top {top_k} feature importances — {model_name}")
    ax.set_xlabel("importance")
    fig.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def save_results(model_name, overall, per_class, predictions=None):
    """Persist per-model results so we can rebuild tables without re-running."""
    safe = model_name.lower().replace(" ", "_")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(RESULTS_DIR / f"{safe}_overall.json", "w") as f:
        json.dump(overall, f, indent=2)
    per_class.to_csv(RESULTS_DIR / f"{safe}_per_class.csv")
    if predictions is not None:
        np.save(RESULTS_DIR / f"{safe}_predictions.npy", predictions)


def write_comparison_table(rows):
    """Write the master comparison CSV (one row per model)."""
    df = pd.DataFrame(rows)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(RESULTS_DIR / "comparison.csv", index=False)
    return df
