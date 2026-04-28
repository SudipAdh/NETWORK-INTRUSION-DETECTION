"""Define the three classifiers under comparison.

Hyperparameters are deliberately conservative — we are studying *baseline*
behaviour rather than chasing leaderboard scores. Heavy tuning would muddle
the comparison because each algorithm would benefit unequally.
"""
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier

from config import RANDOM_SEED


def build_models():
    """Return a dict of name -> sklearn-compatible estimator."""
    return {
        "Logistic Regression": LogisticRegression(
            max_iter=1000,
            solver="lbfgs",
            n_jobs=-1,
            random_state=RANDOM_SEED,
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=100,
            max_depth=None,
            n_jobs=-1,
            random_state=RANDOM_SEED,
            class_weight="balanced",
        ),
        "XGBoost": XGBClassifier(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            objective="multi:softprob",
            num_class=5,
            tree_method="hist",
            n_jobs=-1,
            random_state=RANDOM_SEED,
            eval_metric="mlogloss",
        ),
    }
