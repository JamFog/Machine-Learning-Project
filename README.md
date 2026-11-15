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
    ├── leakage_register.md     Leakage risks and how each is handled
    ├── experiment_log.md       Seed policy and every experiment run, in order
    ├── experiment_results.csv  All cross-validation results (written by notebook 03)
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

Notebook 03 takes a few minutes, mostly for the random forest and gradient boosting.

## Notebooks

| Notebook | Purpose | Milestone |
|---|---|---|
| `01_data_audit.ipynb` | Load metadata, data audit, define period buckets, remove duplicate works, sample 100 books per period, download texts | 2 |
| `02_baseline.ipynb` | Text audit and cleaning, 5,000-word excerpts, wrong-date and translation checks, train/test split, Zero-R baseline | 2 (updated in 3) |
| `03_models.ipynb` | Logistic regression, kNN, decision tree, random forest and gradient boosting: tuning, error analysis, comparison, final test, responsible use and plan for weeks 8–12 | 3 |

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

## Results so far (Milestone 3)

| Model | Macro-F1 (5-fold CV, mean ± std) |
|---|---|
| Zero-R baseline | 0.084 ± 0.002 |
| kNN (k=15) | 0.324 ± 0.046 |
| Decision tree (depth 6) | 0.341 ± 0.038 |
| Logistic regression (C=100) | 0.460 ± 0.067 |
| Random forest (100 trees) | 0.498 ± 0.073 |
| **Gradient boosting (400 rounds)** | **0.506 ± 0.064** |

**Preferred model:** gradient boosting. On the 71 held-out test books it scores **macro-F1 0.519** and accuracy 0.507,
close to its cross-validation estimate. 80% of its mistakes are in a neighbouring period.
See notebook 03 for the full analysis, limitations and the plan for weeks 8–12.

## Assistance declaration

See [`ASSISTANCE.md`](ASSISTANCE.md).

