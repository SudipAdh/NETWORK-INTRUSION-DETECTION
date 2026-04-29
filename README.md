# Network Intrusion Detection — A Comparative Study

A reproducible comparative study of three classical machine-learning algorithms — **Logistic Regression**, **Random Forest**, and **XGBoost** — on the **NSL-KDD** benchmark for multi-class network intrusion detection (Normal, DoS, Probe, R2L, U2R).

This is the M.Sc. Machine Learning coursework project (module **STW7072CEM**) for **Sudip Adhikari (250578)**, Softwarica College of IT & E-Commerce in collaboration with Coventry University.

| Resource | Link |
|----------|------|
| **GitHub repository** | <https://github.com/SudipAdh/NETWORK-INTRUSION-DETECTION> |
| **Demo screencast** | <https://drive.google.com/file/d/12qWAM443JASkQnvJphx7Uv3OxtabJP6s/view?usp=sharing> |
| **Research paper (assessed)** | [`research_paper/paper.pdf`](research_paper/paper.pdf) |
| **Long-form report** | [`assignment_report/assignment_report.pdf`](assignment_report/assignment_report.pdf) |

---

## Headline results (KDDTest+)

| Algorithm           | Accuracy | Weighted F1 | Macro F1 | ROC-AUC | Train time |
|---------------------|---------:|------------:|---------:|--------:|-----------:|
| Logistic Regression |  77.91 % |      0.7631 |   0.5745 |  0.8970 |   330.3 s  |
| Random Forest       |  75.05 % |      0.7112 |   0.5382 |  0.9476 |    53.8 s  |
| **XGBoost**         |**78.66 %**|     0.7582 | **0.6337** | **0.9537** | 90.1 s |

XGBoost wins on three of four held-out metrics and is the only model with credible U2R detection (per-class F1 = 0.4356). Cross-validation weighted F1 (0.97 – 0.99) is ~22 percentage points higher than the held-out test F1 — a property of NSL-KDD deliberately including unseen attack subtypes in its test split, and a number that papers reporting only CV results quietly hide.

---

## Repository layout

```
.
├── src/                       Python source — pipeline, models, evaluation
│   ├── config.py              Paths, random seed, label map
│   ├── data_loader.py         NSL-KDD loader + 22-attack → 5-class mapping
│   ├── preprocess.py          One-hot + StandardScaler
│   ├── models.py              LR / RF / XGBoost definitions
│   ├── evaluate.py            Metrics, confusion matrix, feature importance
│   └── run_experiments.py     End-to-end driver (script form of the notebook)
├── notebooks/
│   └── NID_pipeline.ipynb     Pedagogical Jupyter walkthrough (the runnable prototype)
├── figures/                   Class distribution, confusion matrices, feature-importance plots
├── results/                   comparison.csv + per-model JSON / CSV / .npy
├── assignment_report/         Long-form report (LaTeX + PDF)
├── research_paper/            IEEE-format paper (LaTeX + PDF) — the assessed deliverable
├── requirements.txt
└── README.md
```

The `dataset/` directory is gitignored on GitHub but is **bundled inside the submitted coursework zip** so the marker can run the project without downloading anything.

---

## How to run the project

Tested on macOS (Apple Silicon) with **Python 3.10+** (developed on 3.13.2).

### 1. Get the dataset

If you are working from the **submission zip**, the dataset is already at
`dataset/archive/nsl-kdd/` — skip to step 2.

If you are working from **GitHub**, download NSL-KDD and place the two
text files manually:

```
dataset/archive/nsl-kdd/
├── KDDTrain+.txt
└── KDDTest+.txt
```

Sources:
- Kaggle: <https://www.kaggle.com/datasets/hassan06/nslkdd>
- University of New Brunswick (original): <https://www.unb.ca/cic/datasets/nsl.html>

### 2. Set up the Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .venv\Scripts\activate           # Windows PowerShell
pip install --upgrade pip
pip install -r requirements.txt
pip install jupyter
```

On macOS, XGBoost requires OpenMP:
```bash
brew install libomp
```
On Ubuntu / Debian: `sudo apt-get install libomp-dev`.

### 3. Run — choose one of the two options

**Option A — Jupyter notebook (recommended; the notebook is the assessed prototype):**
```bash
jupyter notebook notebooks/NID_pipeline.ipynb
```
The notebook ships with execution outputs already saved, so you can either
open it and read, or *Cell → Run All* to re-execute (~8–10 min).

**Option B — Equivalent script:**
```bash
PYTHONPATH=src python src/run_experiments.py
```
This produces the same `results/` and `figures/` artefacts as the notebook.

### 4. (Optional) re-build the paper PDF

```bash
brew install tectonic
tectonic research_paper/paper.tex
tectonic assignment_report/assignment_report.tex
```

---

## Methodological choices worth noting

- **SMOTE is applied inside each cross-validation fold**, on the training side only. Generating SMOTE samples before splitting (a common shortcut) leaks information into validation folds and inflates CV scores by several points.
- **One-hot encoding spans the union of train + test categorical levels.** NSL-KDD's test split contains `service` values absent from training; encoding only on training would yield silent zero-columns at test time.
- **Class-balanced weighting for LR and RF** plus SMOTE for XGBoost — covers both reweighting and resampling strategies for imbalance.
- **Held-out evaluation on the official KDDTest+ split.** No tuning on the test set; cross-validation is used only on the training partition.
- **`RANDOM_SEED = 42`** is set everywhere; results are bit-for-bit reproducible.

---

## Author

**Sudip Adhikari** · 250578 · M.Sc. Computer Engineering · Softwarica College of IT & E-Commerce (Coventry University) · Kathmandu, Nepal · `xudip12@gmail.com`

Coursework project for **STW7072CEM Machine Learning**, 2026 cohort.
