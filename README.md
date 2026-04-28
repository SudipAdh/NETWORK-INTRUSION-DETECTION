# Network Intrusion Detection — A Comparative Study

A reproducible comparative study of three classical machine-learning algorithms — **Logistic Regression**, **Random Forest**, and **XGBoost** — on the **NSL-KDD** benchmark for multi-class network intrusion detection (Normal, DoS, Probe, R2L, U2R).

This is the M.Sc. Machine Learning coursework project for **Sudip Adhikari (250578)**, Softwarica College of IT & E-Commerce (Coventry University).

---

## Headline results (KDDTest+)

| Algorithm           | Accuracy | Weighted F1 | Macro F1 | ROC-AUC | Train time |
|---------------------|---------:|------------:|---------:|--------:|-----------:|
| Logistic Regression |  77.91 % |      0.7631 |   0.5745 |  0.8970 |   330.3 s  |
| Random Forest       |  75.05 % |      0.7112 |   0.5382 |  0.9476 |    53.8 s  |
| **XGBoost**         |**78.66 %**|     0.7582 | **0.6337** | **0.9537** | 90.1 s |

XGBoost wins on three of four held-out metrics and is the only model with credible U2R detection (per-class F1 = 0.4356). The cross-validation weighted F1 scores (0.97 – 0.99) are ~22 percentage points higher than test scores — a property of NSL-KDD deliberately including unseen attack subtypes in its test split, and a number that papers reporting only CV results quietly hide.

Full discussion: see [`assignment_report/assignment_report.pdf`](assignment_report/assignment_report.pdf) and the IEEE-format paper at [`research_paper/paper.pdf`](research_paper/paper.pdf).

---

## Repository layout

```
.
├── src/                       Python source — pipeline, models, evaluation
│   ├── config.py              Paths, random seed, label map, constants
│   ├── data_loader.py         NSL-KDD loader + 22-attack → 5-class mapping
│   ├── preprocess.py          One-hot encode + StandardScaler
│   ├── models.py              LR / RF / XGBoost definitions
│   ├── evaluate.py            Metrics, confusion matrix, feature importance
│   └── run_experiments.py     End-to-end driver
├── figures/                   Class distribution, confusion matrices, feature importance plots
├── results/                   comparison.csv + per-model JSON / CSV / .npy
├── assignment_report/         College submission (LaTeX + PDF, ~18 pages)
├── research_paper/            IEEE-format paper (LaTeX + PDF, 5 pages)
├── docs/                      Slides, proposal, speaker notes
├── requirements.txt
└── README.md
```

The `dataset/` directory is intentionally **not** committed — see below.

---

## Dataset

The NSL-KDD dataset is required to run the pipeline. It is not redistributed here; download it from one of the canonical mirrors:

- Kaggle: <https://www.kaggle.com/datasets/hassan06/nslkdd>
- University of New Brunswick (original): <https://www.unb.ca/cic/datasets/nsl.html>

After download, extract so that the structure looks like:

```
dataset/
└── archive/
    └── nsl-kdd/
        ├── KDDTrain+.txt
        └── KDDTest+.txt
```

The loader reads these two files. The constant `DATASET_DIR` in `src/config.py` controls the path if you place them elsewhere.

---

## Reproducing the experiment

Tested on macOS (Apple Silicon) with **Python 3.13.2**.

```bash
# 1. Clone
git clone https://github.com/SudipAdh/NETWORK-INTRUSION-DETECTION.git
cd NETWORK-INTRUSION-DETECTION

# 2. Place NSL-KDD under dataset/archive/  (see "Dataset" above)

# 3. Set up the environment
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# 4. (macOS only) XGBoost requires OpenMP
brew install libomp

# 5. Run the full pipeline
PYTHONPATH=src .venv/bin/python src/run_experiments.py
```

The driver prints CV scores per fold, fits each model on the SMOTE-resampled training set, evaluates on `KDDTest+`, and writes:

- `results/comparison.csv` — one row per model with overall metrics
- `results/<model>_overall.json` — full metric dict
- `results/<model>_per_class.csv` — per-class precision/recall/F1
- `figures/cm_<model>.png` — confusion matrices (count + row-normalised)
- `figures/fi_<model>.png` — feature importance (top 20)
- `figures/class_distribution.png` — train vs test class distribution (log scale)

All randomness is seeded with `RANDOM_SEED = 42`.

---

## Methodological choices worth noting

- **SMOTE inside the CV loop, not before it.** Synthetic minority samples are generated only on each fold's training side. Generating them globally first (a common shortcut) leaks information into the validation folds and inflates CV scores.
- **One-hot encoding over the union of train + test categorical levels.** The NSL-KDD test split contains `service` values absent from training; encoding only on training yields columns of zeros at test time and silently breaks tree splits.
- **`class_weight="balanced"` for Random Forest and Logistic Regression** as well as SMOTE for XGBoost — covers both reweighting and resampling strategies for imbalance.
- **Held-out evaluation on the official `KDDTest+` split.** No tuning on the test set; CV is used only on the training partition.

---

## Building the reports

Both reports use [Tectonic](https://tectonic-typesetting.github.io/) (no `sudo` install needed):

```bash
brew install tectonic        # macOS

tectonic assignment_report/assignment_report.tex
tectonic research_paper/paper.tex
```

`research_paper/paper.tex` builds the IEEE-format paper; `assignment_report/assignment_report.tex` builds the longer college submission. Both pull figures from `../figures/`.

---

## Author

**Sudip Adhikari** · Roll 250578 · M.Sc. Computer Engineering · Softwarica College of IT & E-Commerce (Coventry University) · Kathmandu, Nepal

Coursework project for the Machine Learning module, 2026 cohort.
