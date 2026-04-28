# Screencast Script — NID Coursework Demo

The brief asks for a "**short screencast/video of your code running**".
Plan: 5–7 minutes, screen recording with voice-over, walking through
the notebook executing on your machine.

Use **macOS QuickTime** (File → New Screen Recording) or **OBS Studio**
to record. Speak naturally; the notes below are talking points, not a
script to read aloud word-for-word.

---

## Pre-flight (do this once, before recording)

1. Activate the virtual environment so `jupyter` is on your `PATH`.
2. Open a single browser tab on `http://localhost:8888` running the
   Jupyter server.
3. Have the notebook `NID_pipeline.ipynb` open and ready, but
   **with all outputs cleared** so the audience sees them appear live.
   - Notebook UI: *Kernel → Restart Kernel and Clear All Outputs*.
4. Close every other window so the recording is clean.
5. Test your microphone level.

---

## Recording outline (5–7 minutes)

### 0:00 – 0:30 · Introduction

> "Hi, I'm Sudip Adhikari, student ID 250578, and this is a short demo
> of my Machine Learning coursework on network intrusion detection.
> The goal of the project was to compare three classical machine learning
> algorithms — Logistic Regression, Random Forest, and XGBoost — on the
> NSL-KDD benchmark dataset, and to do so honestly, with proper per-class
> reporting and per-fold cross-validation."

(*Show the notebook's title cell on screen.*)

### 0:30 – 1:30 · The dataset and the problem

> "NSL-KDD has 125,000 training records and 22,500 test records. Each
> record describes a single network connection across 41 features.
> Connections are labelled as either Normal or one of four attack
> categories: DoS, Probe, R2L, and U2R."

(*Run cells 1 and 2 — the imports and the dataset loader.*)

> "Notice the class imbalance — U2R has only 52 training samples,
> 0.04 percent of the data. This is the central difficulty of the
> dataset and the reason why per-class metrics matter."

(*Run the class distribution plot cell. Pause on the figure.*)

### 1:30 – 2:30 · Preprocessing

> "I one-hot encode the three categorical features over the union of
> train and test categories. This is important because the test set has
> service strings that don't appear in training; if I encoded only on
> training, those test rows would have all-zero columns and silently
> break tree splits."

(*Run the preprocessing cell — show the 41 → 122 feature growth.*)

### 2:30 – 3:30 · SMOTE — and why it goes inside the CV loop

> "To handle the class imbalance I use SMOTE, which generates synthetic
> minority samples. The crucial detail is *when* to apply it. The
> common shortcut is to SMOTE-resample the whole training set once,
> then split into folds — but that leaks synthetic samples derived from
> the validation neighbours back into training. Cross-validation scores
> become inflated. So I apply SMOTE inside each fold instead, on the
> training side only."

(*Run the SMOTE cell; show the resampled class counts.*)

### 3:30 – 5:00 · The training loop (this is the slow part)

> "Now we train all three models. Each one runs 5-fold stratified
> cross-validation with per-fold SMOTE, then refits on the full
> resampled training set, then evaluates on the held-out test set."

(*Run the training cell. Talk over the output as it appears.*)

> "Cross-validation F1 is around 0.97–0.99 for all three models —
> looks great. But watch what happens on the test set..."

(*When the test results print, pause briefly.*)

> "...test F1 drops to around 0.71 to 0.76. That's roughly a
> 22-percentage-point gap. This is **not** ordinary overfitting — it's
> the dataset doing what it was designed to do. The NSL-KDD test split
> deliberately contains attack subtypes that are absent in training,
> so cross-validation measures fit on the training distribution while
> the held-out test measures generalisation to a different distribution.
> Studies that quote only the CV number are reporting the wrong
> number, and a big part of this paper is making that gap visible."

### 5:00 – 6:00 · The headline result

(*Run the comparison-table cell.*)

> "XGBoost wins on accuracy, macro F1, and ROC-AUC. Random Forest is
> the fastest. Logistic Regression is competitive on weighted F1, but
> the per-class table will show that's a majority-class effect."

(*Run the confusion-matrix and feature-importance cells.*)

> "On the confusion matrix you can see most of the errors are R2L and
> U2R attacks being misclassified as Normal — exactly the dangerous
> cases. The feature-importance plot shows the model relies most on
> connection-flag and service signals, which a network analyst would
> already monitor."

### 6:00 – 6:30 · Closing

> "Full discussion is in the IEEE paper — including the social,
> ethical, legal, and professional implications of deploying such a
> detector in a context like Nepal, where security capacity is
> uneven. The complete code is on GitHub at
> github.com/SudipAdh/NETWORK-INTRUSION-DETECTION. Thank you for watching."

---

## After recording

- Trim the front and back of the video so it starts and ends cleanly.
- Export at 720p or 1080p, MP4 format.
- Filename: `SudipAdhikari_250578_demo.mp4`.
- Place it inside the submission zip if it is under 100 MB. If larger,
  upload to Google Drive (set sharing to "anyone with the link") and
  paste the link into the cover page of the submission.
