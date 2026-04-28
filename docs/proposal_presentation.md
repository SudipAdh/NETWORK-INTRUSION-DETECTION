# Proposal Presentation — Slide Content
### Use this to build your slides in PowerPoint / Google Slides

---

## SLIDE 1: Title Slide

**A Comparative Study of Classical Machine Learning Algorithms for Multi-Class Network Intrusion Detection**

Sudip Adhikari
M.Sc. Computer Engineering
National College of Engineering, Tribhuvan University

Machine Learning — Project Proposal

---

## SLIDE 2: Why This Topic?

**The Problem**

- Cyberattacks are growing fast — Nepal alone saw a sharp rise in cyber incidents over the past few years, and most organizations here still rely on basic signature-based firewalls
- Traditional intrusion detection systems work on predefined rules — they can catch known attacks but completely miss new or slightly modified ones
- We need systems that can actually learn patterns from network traffic and flag suspicious activity on their own

**Why it matters to me:**
I wanted to work on something that has a clear, practical use case beyond just academics. Network security is one area where ML can make a real difference, and the dataset for this is well-established — so I can focus on the actual analysis instead of spending weeks cleaning messy data.

---

## SLIDE 3: What I Plan to Do

**Project Objectives**

1. Build and compare multiple classical ML models (not just one algorithm) to classify network traffic into Normal vs. 4 attack categories
2. See which algorithms handle the tricky part — detecting rare attack types like R2L and U2R that make up less than 2% of the data
3. Analyze which network features matter most for detection (feature importance)
4. Provide a clear, honest comparison with proper evaluation metrics — not just accuracy, but precision, recall, F1-score, and confusion matrices

**Scope:** This is a classification problem with 5 classes — Normal, DoS, Probe, R2L, and U2R.

---

## SLIDE 4: The Dataset — NSL-KDD

**Why NSL-KDD?**

- It is the most widely used benchmark dataset in network intrusion detection research
- Improved version of the original KDD Cup 1999 dataset — removes duplicate records that used to bias older results
- Publicly available, no access issues

**Dataset at a glance:**

| Detail | Value |
|--------|-------|
| Training samples | ~125,973 |
| Test samples | ~22,544 |
| Features | 41 network traffic features |
| Classes | 5 (Normal, DoS, Probe, R2L, U2R) |
| Format | CSV, ready to use |

**The challenge:** The classes are heavily imbalanced. DoS attacks dominate, while R2L and U2R are extremely rare — which is realistic but makes classification harder.

---

## SLIDE 5: How I Will Do It (Methodology)

**Step-by-step approach:**

```
Raw Data --> Preprocessing --> Feature Engineering --> Model Training --> Evaluation
```

1. **Preprocessing:** Handle categorical features (protocol type, service, flag) using encoding, normalize numerical features, deal with class imbalance using techniques like SMOTE if needed

2. **Algorithms I will compare:**
   - Logistic Regression (baseline)
   - K-Nearest Neighbors (KNN)
   - Decision Tree
   - Random Forest
   - Support Vector Machine (SVM)
   - XGBoost (gradient boosting)

3. **Evaluation:** 10-fold cross-validation, confusion matrices for each model, per-class precision/recall/F1, ROC-AUC curves

4. **Analysis:** Feature importance ranking, comparison table across all models, discussion on which model works best for which attack type

---

## SLIDE 6: Expected Outcomes

**What I expect to find:**

- Tree-based models (Random Forest, XGBoost) will likely outperform others overall — this is consistent with existing literature
- But the real question is how each model handles the rare classes (R2L, U2R) — that is where the interesting analysis lies
- Simpler models like Logistic Regression might still do surprisingly well on binary (normal vs. attack) but struggle with multi-class

**Deliverables:**
- Complete Python codebase with reproducible results
- Detailed comparison report with visualizations
- Trained models with evaluation metrics for each algorithm

---

## SLIDE 7: Timeline and Tools

**Rough Timeline:**

| Week | Task |
|------|------|
| Week 1 | Data loading, exploration, preprocessing |
| Week 2 | Train baseline models (LR, KNN, DT) |
| Week 3 | Train advanced models (RF, SVM, XGBoost) |
| Week 4 | Evaluation, comparison, feature analysis |
| Week 5 | Report writing and final presentation |

**Tools:**
- Python (scikit-learn, pandas, matplotlib, seaborn)
- Jupyter Notebook for experimentation
- XGBoost library

**References:**
- Tavallaee et al. (2009) — NSL-KDD dataset paper
- Ahmad et al. (2021) — Network intrusion detection using ML: A comparative study
- Dhanabal & Shantharajah (2015) — Study on NSL-KDD with ML

---

## Speaker Notes / Tips

- **Slide 2:** Start by talking about why you picked this topic — keep it personal. Mention that everyone else in class picked agriculture or IoT topics, and you wanted to try something different in cybersecurity.
- **Slide 4:** Emphasize that the dataset is a gold standard benchmark — no risk of data availability issues.
- **Slide 5:** When explaining methodology, stress that you are comparing 6 algorithms, not just running one — that is what makes it a proper study.
- **Slide 6:** Be honest about expected outcomes. Teachers appreciate when you say "I expect X but want to verify" rather than overclaiming.
- **Keep it conversational.** You are proposing what you plan to do, not defending a thesis. Relax.
