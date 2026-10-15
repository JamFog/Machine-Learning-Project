# Data

## Source

- **Name:** PG-19 (Project Gutenberg books published before 1919)
- **Publisher:** Google DeepMind — https://github.com/google-deepmind/pg19
- **Licence:** Apache License 2.0 (dataset); the underlying Project Gutenberg texts are public domain.
- **Citation:** Rae, J. W., Potapenko, A., Jayakumar, S. M., Hillier, C., & Lillicrap, T. P. (2019).
  *Compressive Transformers for Long-Range Sequence Modelling.* arXiv:1911.05507.

The full corpus is ~11 GB, so it is **not** committed to this repository.

## Contents

The dataset is hosted in the public Google Cloud Storage bucket `gs://deepmind-gutenberg`:

- `metadata.csv` — one row per book: `id`, `short_book_title`, `publication_date`, `url`
- `train/`, `validation/`, `test/` — one `<id>.txt` file per book

This project only uses `metadata.csv` and a stratified subsample of a few hundred books from
`train/`.

## Download

Metadata (small):

```powershell
curl -o data/raw/metadata.csv https://storage.googleapis.com/deepmind-gutenberg/metadata.csv
```

Individual books can be fetched by id:

```
https://storage.googleapis.com/deepmind-gutenberg/train/<id>.txt
```

The sampled book ids, and the code that downloads them, will live in `notebooks/01_data_audit.ipynb`
/ `src/`.

## Folder layout

| Folder | Contents | Tracked in git? |
|---|---|---|
| `raw/` | `metadata.csv` and downloaded book `.txt` files, unmodified | No |
| `interim/` | Sampled subset with assigned period labels | No |
| `processed/` | Extracted feature matrices | No |
