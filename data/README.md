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

This project only uses `metadata.csv` and a stratified subsample of 500 books (100 per period).
PG-19's own train/validation/test folders are not used as splits; the project makes its own split in notebook 02.

## Download

Metadata (small):

```powershell
curl -o data/raw/metadata.csv https://storage.googleapis.com/deepmind-gutenberg/metadata.csv
```

Individual books can be fetched by id:

```
https://storage.googleapis.com/deepmind-gutenberg/train/<id>.txt
```

Most books are in `train/`; a few are in `validation/` or `test/` instead, so the download code tries
all three folders.

The sampled book ids are saved to `interim/sample.csv`, and the code that downloads them is in
`notebooks/01_data_audit.ipynb`. Book texts are saved to `raw/books/<id>.txt`.

## Folder layout

| Folder | Contents | Tracked in git? |
|---|---|---|
| `raw/` | `metadata.csv` and downloaded book `.txt` files, unmodified | No |
| `interim/` | Sampled subset with assigned period labels | No |
| `processed/` | `train.csv` and `test.csv`: one 5,000-word excerpt per book with its label (written by notebook 02) | No |

## Data statement

**Provenance.** Books and publication dates come from PG-19's `metadata.csv` and book files (see Source above).
The dates were assigned by PG-19 / Project Gutenberg, not by this project. They are sometimes the date of an edition,
of the original work (for translations), or of the book's subject, rather than of first publication.

**Unit of analysis and target.** One book = one row. The target is the publication period, derived from
`publication_date`: pre-1750, 1750–1799, 1800–1849, 1850–1899, 1900–1918.

**Variables used** (`processed/train.csv`, `processed/test.csv`):

| Column | Meaning | Role |
|---|---|---|
| `id` | PG-19 book id | Identifier only |
| `title` | PG-19 short title (includes "by Author" for most books) | Identifier only; used to derive `group` |
| `publication_date` | Year from PG-19 metadata | Used only to make `period`; never a model input |
| `period` | One of the five periods | **Target** |
| `group` | Author name taken from the title (the title itself if no author) | Grouping for the author-grouped split and CV; not a model input |
| `excerpt` | 5,000 consecutive words from the middle of the cleaned book | **Model input** (TF-IDF, letters only) |

**Exclusions, in order** (details in notebooks 01–02):

| Step | Books removed | Books left |
|---|---|---|
| Before sampling: duplicate Bibles, modern documents with wrong dates, non-English texts, all but one volume/part of each work | – | – |
| Stratified sample, 100 per period | – | 500 |
| Under 5,000 words (so length can't reveal the period) | 23 | 477 |
| Excerpt mentions a year more than 20 years after the label | 31 | 446 |
| Title page shows a much later year, or says the book is a translation | 87 | 359 |

**Final data:** 359 books, from 48 (pre-1750) to 95 (1900–1918) per period; split 288 train / 71 test, grouped by
author and stratified by period.

**Known limits and representation gaps.**
- English-language books only, all published by 1918, almost all from Project Gutenberg's volunteer-selected
  collection. This favours well-known, out-of-copyright, mostly British and American authors and literary or
  educational texts. Other genres, regions and less famous writers are under-represented.
- Some labels are still wrong. Books whose wrong date is not visible in the excerpt or on the title page are not caught,
  and translations that don't say so remain.
- The periods are unbalanced after cleaning (48 vs 95 books), because older books were more often mislabelled or translated.
- Author names come from titles, so spelling variants count as different authors.

**Privacy.** All texts are public domain and the authors died long ago. The data contains no personal data about living
people, and no personal data is collected or stored by this project.
