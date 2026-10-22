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
│   ├── interim/            Sampled subset (git-ignored)
│   └── processed/          Feature matrices (git-ignored)
├── notebooks/              Numbered notebooks, run in order
├── src/                    Reusable Python code imported by the notebooks
└── reports/
    └── figures/            Figures used in the report
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
3. Run the notebooks in `notebooks/` in numerical order (Kernel → Restart & Run All).

## Notebooks

| Notebook | Purpose | Milestone |
|---|---|---|
| `01_data_audit.ipynb` | Load metadata, data audit, define period buckets, sample books | 2 |
| `02_baseline.ipynb` | Text audit and preparation, train/test split, Zero-R baseline | 2 |
| `03_model_comparison.ipynb` | Naive Bayes / Logistic Regression vs baseline, tuning, error analysis | 3 |

## Evaluation design (summary)

- 80/20 train/test split **grouped by author** (no author in both sets) and stratified by period;
  the test set is held out until final evaluation.
- Stratified k-fold cross-validation on the training set, also grouped by author, for model selection and tuning.
- Baseline: majority-class (Zero-R). Candidate models: Multinomial Naive Bayes, Logistic Regression.
- Metrics: accuracy and macro-averaged F1.

## Assistance declaration

See [`ASSISTANCE.md`](ASSISTANCE.md).

