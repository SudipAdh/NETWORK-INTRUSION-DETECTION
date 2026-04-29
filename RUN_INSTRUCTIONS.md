# How to Run This Project

**Module:** STW7072CEM Machine Learning
**Author:** Sudip Adhikari (250578)

This document is a comprehensive set of instructions for executing the
intrusion detection pipeline submitted as coursework. Following these
steps will reproduce every figure, table, and result in
`research_paper/paper.pdf`.

## Demo video

A short screencast of the code running is available at:

<https://drive.google.com/file/d/12qWAM443JASkQnvJphx7Uv3OxtabJP6s/view?usp=sharing>

The video walks through the Jupyter notebook from raw data inspection
through preprocessing, training, evaluation, and the per-class results.
If the link does not load, please contact the author at
`xudip12@gmail.com`.

---

## 1. What's in this submission

```
SudipAdhikari_250578/
├── README.md                    Project overview
├── RUN_INSTRUCTIONS.md          This file
├── requirements.txt             Python dependencies
├── research_paper/
│   ├── paper.tex                IEEE-format paper source
│   └── paper.pdf                THE SUBMISSION DOCUMENT
├── notebooks/
│   └── NID_pipeline.ipynb       Jupyter notebook — runs the full pipeline
├── src/                         Modular Python source
│   ├── config.py                Paths, random seed, label maps
│   ├── data_loader.py           NSL-KDD loader + 22→5 attack mapping
│   ├── preprocess.py            One-hot + StandardScaler
│   ├── models.py                LR / RF / XGBoost definitions
│   ├── evaluate.py              Metrics, confusion matrix, feature importance
│   └── run_experiments.py       Same pipeline as the notebook (script form)
├── figures/                     Generated PNGs (cm_*, fi_*, class_distribution)
├── results/                     comparison.csv + per-model JSON / CSV / .npy
└── assignment_report/           Long-form internal report (supporting only — not the submission)
```

The IEEE paper at `research_paper/paper.pdf` is the assessed deliverable.
The notebook at `notebooks/NID_pipeline.ipynb` is the runnable prototype
required by the assignment brief.

---

## 2. Prerequisites

- **Python 3.10 or newer** (developed on 3.13.2)
- **Git** (only if cloning from GitHub rather than the zip)
- **Approximately 200 MB of disk space** (mostly the dataset)
- **Approximately 8 GB of RAM** (peaks during the SMOTE-resampled fit)

### Platform-specific dependency

XGBoost requires OpenMP. Install it once per machine:

| OS       | Command                                            |
|----------|----------------------------------------------------|
| macOS    | `brew install libomp`                              |
| Ubuntu / Debian | `sudo apt-get install libomp-dev`           |
| Windows  | OpenMP is bundled with Visual Studio's redistributable; usually no action needed. |

---

## 3. Get the dataset

The NSL-KDD dataset is **not** included in this zip (licence + size). Download
it from one of the canonical mirrors:

- Kaggle: <https://www.kaggle.com/datasets/hassan06/nslkdd>
- University of New Brunswick (original): <https://www.unb.ca/cic/datasets/nsl.html>

Extract the archive so that the structure looks like:

```
SudipAdhikari_250578/
└── dataset/
    └── archive/
        └── nsl-kdd/
            ├── KDDTrain+.txt
            └── KDDTest+.txt
```

Only `KDDTrain+.txt` and `KDDTest+.txt` are required; other files in the
archive are ignored by the loader.

---

## 4. Set up the Python environment

From the project root:

```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .venv\Scripts\activate           # Windows PowerShell

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

`requirements.txt` pins:

```
pandas
numpy
scikit-learn
matplotlib
seaborn
xgboost
imbalanced-learn
joblib
```

For the notebook you also need Jupyter:

```bash
pip install jupyter
```

---

## 5. Reproduce the experiments — choose ONE of the three options

### Option A. Run the Jupyter notebook (recommended — the assignment brief asks for this)

```bash
jupyter notebook notebooks/NID_pipeline.ipynb
```

Then click *Cell → Run All* in the notebook UI. The notebook walks through
the pipeline step by step with markdown explanations and produces all
plots, the comparison table, the confusion matrix, and the feature
importance figure inline.

The repo ships the notebook **with execution outputs already saved**, so
you can also just open it to inspect the results without re-running.

Total wall-clock time on a 2023 MacBook M2: roughly 8–10 minutes.

### Option B. Run the equivalent script

```bash
PYTHONPATH=src python src/run_experiments.py
```

This is exactly the same pipeline as the notebook but in script form. It
prints progress to stdout and writes:

- `results/comparison.csv` — overall metrics, one row per model
- `results/<model>_overall.json` — full metric dict
- `results/<model>_per_class.csv` — per-class precision / recall / F1
- `figures/cm_<model>.png` — confusion matrix (counts + row-normalised)
- `figures/fi_<model>.png` — top-15 feature importance
- `figures/class_distribution.png` — train vs test class distribution

### Option C. Run on Google Colab

Upload the contents of the zip (or clone the repo) to Colab, then run the
notebook. Replace the `pip install` step with:

```python
!pip install -r requirements.txt -q
```

Colab does not need the OpenMP step — its container image already has it.

---

## 6. Re-build the paper PDF (optional)

The submitted PDF is at `research_paper/paper.pdf`. To rebuild it from
source you need a LaTeX engine. The project was built with
[Tectonic](https://tectonic-typesetting.github.io/), which does not
require `sudo`:

```bash
brew install tectonic           # macOS
tectonic research_paper/paper.tex
```

Any other LaTeX engine (TeX Live, MikTeX, Overleaf) works equally well —
the paper uses standard packages only (IEEEtran, hyperref, booktabs,
graphicx, amsmath, siunitx, balance).

---

## 7. Verifying the headline results

After running Option A or B you should see the following on the held-out
KDDTest+ split:

| Algorithm           | Accuracy | Weighted F1 | Macro F1 | ROC-AUC |
|---------------------|---------:|------------:|---------:|--------:|
| Logistic Regression |  77.91 % |      0.7631 |   0.5745 |  0.8970 |
| Random Forest       |  75.05 % |      0.7112 |   0.5382 |  0.9476 |
| **XGBoost**         |**78.66 %**|     0.7582 | **0.6337** | **0.9537** |

Numbers are deterministic because every random source is seeded with
`RANDOM_SEED = 42` (see `src/config.py`).

---

## 8. Source code repository

The complete project is also published at:

<https://github.com/SudipAdh/NETWORK-INTRUSION-DETECTION>

The GitHub repository may receive minor updates after submission; the
zip submitted on Campus 4.0 is the canonical version for grading.

---

## 9. Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `OSError: dlopen... libomp.dylib` | OpenMP missing on macOS | `brew install libomp` |
| `FileNotFoundError: KDDTrain+.txt` | Dataset not in the expected path | Re-check Section 3 |
| `ModuleNotFoundError: imblearn` | Dependencies not installed | `pip install -r requirements.txt` |
| Different numbers from the table | Random seed different / wrong sklearn / wrong xgboost | `pip install -r requirements.txt` exactly |
| Notebook kernel can't import `config` | `sys.path` not set | Ensure the first code cell ran (`sys.path.insert(0, ...)`) |

If a different problem appears, please contact the author at
`xudip12@gmail.com`.
