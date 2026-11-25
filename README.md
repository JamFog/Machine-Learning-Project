# Classifying Historical Publishing Period from Literary Language

CT4101 Machine Learning Portfolio Project — James Fogarty (23349263)

**Question:** Can a machine-learning model classify an English-language book into its historical
publication period (e.g. pre-1750, 1750–1799, 1800–1849, 1850–1899, 1900–1918) based on the
language used within it? This is a multi-class classification task.

**Dataset:** [PG-19](https://github.com/google-deepmind/pg19) (Google DeepMind), Apache License 2.0;
underlying Project Gutenberg texts are public domain. See [`data/README.md`](data/README.md) for
download instructions. Data is not committed to this repository.

> Rae, J. W., Potapenko, A., Jayakumar, S. M., Hillier, C., & Lillicrap, T. P. (2019).
> *Compressive Transformers for Long-Range Sequence Modelling.* arXiv:1911.05507.

## Project structure

```
├── README.md               Project overview, setup and run instructions
├── requirements.txt        Pinned Python packages
├── ASSISTANCE.md           Assistance / generative-AI declaration
├── data/
│   ├── README.md           Dataset source, licence, download instructions
│   ├── raw/                Downloaded PG-19 files (git-ignored)
│   ├── interim/            Sampled subset, sample.csv (git-ignored)
│   └── processed/          Prepared train.csv / test.csv excerpts (git-ignored)
├── notebooks/              Numbered notebooks, run in order
├── src/                    Reusable Python code imported by the notebooks
└── reports/
    ├── model_card.md           Model card: intended use, performance, slices, risks, recommendation
    ├── changelog.md            Reflective changelog: important decisions and their evidence
    ├── leakage_register.md     Leakage risks and how each is handled
    ├── experiment_log.md       Seed policy and every experiment run, in order
    ├── *.csv                   Results tables written by notebooks 03–06
    └── figures/                Figures used in the report
```

## Setup

Requires **Python 3.15** (tested on Windows 11).

```powershell
# from the repository root
python -m venv .venv
.venv\Scripts\Activate.ps1          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m ipykernel install --user --name ct4101-pg19
```

## Running

1. Download the data as described in [`data/README.md`](data/README.md).
2. Start Jupyter: `jupyter lab`
3. Run the notebooks in `notebooks/` in numerical order (Kernel → Restart Kernel and Run All Cells).
   Each notebook saves the files the next one needs, so they must be run in order.

Notebooks 03–06 each take a few minutes (notebook 04 is the slowest: every MLP setting is run with 3 seeds).

## Notebooks

| Notebook | Purpose | Milestone |
|---|---|---|
| `01_data_audit.ipynb` | Load metadata, data audit, define period buckets, remove duplicate works, sample 100 books per period, download texts | 2 |
| `02_baseline.ipynb` | Text audit and cleaning, 5,000-word excerpts, wrong-date and translation checks, train/test split, Zero-R baseline | 2 (updated in 3) |
| `03_models.ipynb` | Logistic regression, kNN, decision tree, random forest and gradient boosting: tuning, error analysis, comparison, final test, responsible use and plan for weeks 8–12 | 3 |
| `04_mlp.ipynb` | Small neural network (MLP): capacity, regularisation, 3 seeds, learning curves, fold-by-fold comparison with boosting, time and size (CV only) | 4 |
| `05_features_robustness.ipynb` | Three engineered style features (alone and added to TF-IDF), and robustness to which part of the book is used (CV only) | 4 |
| `06_errors_interpretation.ipynb` | Out-of-fold error analysis with author-level bootstrap intervals, test result with intervals, calibration, permutation importance and a local explanation | 4 |

## Evaluation design (summary)

- **Data:** 359 books after cleaning (48–95 per period), each reduced to a 5,000-word excerpt from the middle of the book.
- **Split:** 80/20 train/test (288 / 71 books), **grouped by author** (no author in both sets) and stratified by period.
- **Cross-validation:** 5-fold, grouped by author and stratified, on the training set only. Every model uses the same folds.
- **Features:** TF-IDF word weights (letters only, so years can't be used; words must appear in at least 10 books),
  fitted inside each fold to avoid leakage.
- **Models:** Zero-R baseline, logistic regression, kNN (cosine distance), decision tree, random forest, gradient boosting.
- **Metrics:** macro-F1 (main), accuracy, confusion matrix, and the share of mistakes in a neighbouring period.
- **Model choice:** each model's main setting is chosen with the one-standard-error rule; the preferred model is chosen
  from the cross-validation results only.
- **Test set:** used once, at the end, for the preferred model only.

## Results

| Model | Macro-F1 (5-fold CV, mean ± std) |
|---|---|
| Zero-R baseline | 0.084 ± 0.002 |
| kNN (k=15) | 0.324 ± 0.046 |
| Decision tree (depth 6) | 0.341 ± 0.038 |
| Logistic regression (C=100) | 0.460 ± 0.067 |
| Random forest (100 trees) | 0.498 ± 0.073 |
| **Gradient boosting (400 rounds)** | **0.506 ± 0.064** |

| Small neural network (MLP, 64 units, `alpha=10`; not adopted) | 0.528 ± 0.051 |

**Preferred model:** gradient boosting. On the 71 held-out test books (used once) it scores **macro-F1 0.52
(95% CI 0.37–0.63)** and accuracy 0.51, close to its cross-validation estimate. 80% of its mistakes are in a
neighbouring period. The MLP was comparable on cross-validation but not consistently better across folds, so boosting was kept.

**Main findings (Milestone 4):**
- **Hardest cases:** 1850–1899 (recall 0.39) and books within 10 years of a period boundary (0.40 vs 0.59 further away).
  Many 1850–1899 and 1900–1918 books are confused in both directions, not only near 1900, so topic and genre play a part.
- **Overconfident:** average confidence 0.78 against 50% accuracy (ECE 0.28), so the probabilities are not reliable.
- **Interpretation:** no single word matters much; old spellings and formal words point to older periods, plainer words to later ones.
- **Robust** to using a different part of each book (scores change by at most 0.025). Three style features carry signal
  on their own but did not improve the model.

**Recommendation:** do not deploy as an automatic dating tool; see [`reports/model_card.md`](reports/model_card.md).

## Documentation

- [`data/README.md`](data/README.md): data source, download and **data statement**
- [`reports/model_card.md`](reports/model_card.md): **model card**
- [`reports/changelog.md`](reports/changelog.md): **reflective changelog**
- [`reports/experiment_log.md`](reports/experiment_log.md) and [`reports/leakage_register.md`](reports/leakage_register.md)

## Assistance declaration

See [`ASSISTANCE.md`](ASSISTANCE.md).

