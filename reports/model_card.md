# Model card: publication-period classifier for English books (PG-19)

A model card records what a model is for, the evidence about how well it works, and its limits and risks.
All numbers come from the notebooks; experiment IDs (E…) refer to `reports/experiment_log.md`.

## 1. Model details

| | |
|---|---|
| **Task** | Multi-class classification: predict which of five periods an English book was published in: pre-1750, 1750–1799, 1800–1849, 1850–1899, 1900–1918 |
| **Input** | A 5,000-word excerpt from the middle of the book (plain text) |
| **Output** | One period, plus a probability for each period (see calibration: these are not reliable) |
| **Model** | TF-IDF word features (letters only, words in at least 10 books) → gradient boosting (scikit-learn `GradientBoostingClassifier`, 400 rounds, learning rate 0.1, depth 3, `max_features="sqrt"`, seed 42) |
| **Size** | 7,123 input words (vocabulary learnt from the 288 training books); 400 rounds × 5 trees (one per period) of depth 3 |
| **Trained on** | 288 books (notebook 03); evaluated once on 71 held-out books |
| **Owner** | James Fogarty, CT4101 portfolio project (University of Galway), 2026 |
| **Code** | `notebooks/03_models.ipynb` (training, test), `06_errors_interpretation.ipynb` (errors, calibration, explanations) |

## 2. Intended use

- **Purpose:** a course project showing whether the language of a book carries enough signal to estimate its
  publication period, and how reliably.
- **Possible users, if developed further:** researchers and digital-library cataloguers who want a *rough first guess*
  of the era of an undated or suspiciously dated public-domain English text, to be checked by a person.
- **Decision it could influence:** which period a book is catalogued under, or which books to send for expert checking.

**Out of scope (the model must not be used for):**
- Authenticating, valuing or dating manuscripts, documents or books for sale, legal, insurance or provenance purposes.
- Deciding whether a text is a forgery, or who wrote it.
- Texts outside the training conditions: not English, published after 1918, shorter than 5,000 words, translations,
  modern texts imitating an older style, or non-book texts (letters, newspapers, legal records).
- Writing dates into catalogues automatically, without a person checking each one.
- Any decision about people.

## 3. Data

Full details are in the data statement (`data/README.md`).

- **Source:** PG-19 (Google DeepMind, Apache 2.0), built from Project Gutenberg public-domain books. Dates come from
  PG-19's metadata and are sometimes edition dates or the original work's date.
- **Sample:** 100 books per period, then cleaned to 359 (removed: too short, later year in the text, later year or
  translation note on the title page). Split 288 / 71, grouped by author.
- **Representation gaps:** English only; up to 1918; mostly well-known British and American authors chosen by Project
  Gutenberg volunteers; literary and educational texts dominate. Performance on other genres, regions and less famous
  writers is **unknown**.
- **Label noise:** some dates are still wrong (books whose wrong date is not visible in the excerpt or title page),
  and unlabelled translations remain.
- **Privacy:** public-domain texts by long-dead authors; no personal data about living people is used or stored.

## 4. Performance

| Model (same 5 author-grouped folds) | Macro-F1 (CV, mean ± std) |
|---|---|
| Zero-R baseline (always the most common period) | 0.08 ± 0.00 |
| Logistic regression (C=100) | 0.46 ± 0.07 |
| **Gradient boosting (this model)** | **0.51 ± 0.06** |
| Small neural network (MLP, not adopted, E16–E20) | 0.53 ± 0.05 |

- **Held-out test set (used once):** macro-F1 **0.52 (95% CI 0.37–0.63)**, accuracy 0.51 (CI 0.39–0.62). The intervals
  come from resampling authors (E26).
- **Near misses:** 80% of test mistakes and 82% of out-of-fold mistakes are in a neighbouring period; only 6 of 288
  out-of-fold predictions are three or more periods away.
- **Robustness:** scores change by at most 0.025 when the model is tested on text from 25% or 75% of the way through
  each book instead of the middle (E23).
- **Calibration:** strongly overconfident. Average confidence is 0.78 but only 50% of predictions are right (ECE 0.28);
  even predictions made with more than 95% confidence are right only 64% of the time (E27).

## 5. Error slices

Out-of-fold predictions on the 288 training books; 95% confidence intervals from 1,000 author-level bootstrap resamples (E24).

| Slice | Books | Accuracy (recall) | 95% CI |
|---|---|---|---|
| All | 288 | 0.50 | 0.44–0.55 |
| pre-1750 | 38 | 0.55 | 0.38–0.72 |
| 1750–1799 | 47 | 0.43 | 0.29–0.57 |
| 1800–1849 | 56 | 0.50 | 0.38–0.64 |
| **1850–1899** | 71 | **0.39** | 0.28–0.52 |
| 1900–1918 | 76 | 0.61 | 0.50–0.72 |
| Within 10 years of a period boundary | 136 | 0.40 | 0.32–0.47 |
| More than 10 years from a boundary | 152 | 0.59 | 0.50–0.66 |

- The weakest group is **1850–1899**: 65 of the 147 books from 1850–1918 are confused between 1850–1899 and 1900–1918,
  and these are *not* concentrated near 1900, so topic and genre seem to play a part (E25).
- Books near a period boundary are much harder, as expected when language changes gradually but labels change at a fixed year.
- The intervals are wide (38–76 books per slice), so small differences between periods are not meaningful.

## 6. Interpretability

- **Global (permutation importance on held-out folds, E28):** no single word matters much (largest drop ≈ 0.01 macro-F1);
  reliance is spread over many words. Old spellings and formal words (*shew*, *thereof*, *unacquainted*) are most frequent
  in older periods, plainer words (*across*, *took*, *feel*) in later ones. No years, publisher names or modern editorial
  words appear among the top words. Style features (notebook 05) agree: sentences get shorter and semicolons rarer over time.
- **Local (leave-one-word-out, E29):** George Gissing's *Demos* (1886) is predicted 1900–1918 with 96% probability.
  Contractions in dialogue (*wasn*, *doesn*) and words like *newspaper* and *working* push it towards the 1900s; a
  character's name (*richard*) is among the words pulling it back, so names still have a small influence.
- **Limits of these explanations:** they describe what the model relies on, not what causes a book to belong to a period;
  correlated words share credit, so groups of related words look less important than they are; only 150 words per fold
  were tested; drops are small and noisy with ~58 books per fold; leave-one-word-out ignores interactions and explains
  one prediction of one fitted model.

## 7. Stakeholders, harms and misuse

| Stakeholder | Possible benefit | Possible harm |
|---|---|---|
| Cataloguers / digital libraries | Faster triage of undated or suspicious records | Wrong dates copied into catalogues, misleading later users |
| Researchers using the catalogue | Better metadata | Studies of language change built on wrong dates; under-represented writers dated less accurately (untested) |
| Readers | Better browsing by era | Books shown in the wrong era |
| Collectors, sellers, buyers | – | **Misuse:** a confident wrong date used to support a document's age or value |

Main risks: (1) **overconfidence**, which invites too much trust; (2) **errors concentrated in 1850–1899 and near
boundaries**; (3) a **sample biased towards canonical Anglo-American books**, so accuracy elsewhere is unknown;
(4) **automation bias**, people accepting the model's date without checking.

## 8. Human oversight, challenge and escalation

- The model only **suggests** a period; a person (cataloguer or researcher) makes every final decision and records it.
- Show the **top two periods** instead of a single answer, and do not show the raw probability as "confidence"
  until the model is recalibrated.
- **Escalate** to an expert when the prediction disagrees with the existing metadata by two or more periods, when the top
  two periods are not neighbours, or when the text is outside scope (see Section 2).
- Anyone can **challenge** a date through the normal catalogue-correction route; corrections are logged and used as
  new labelled data.
- The owner can withdraw the model at any time; the existing manual cataloguing process is the fallback.

## 9. Monitoring, drift and update triggers

| Signal | Why | Trigger for review |
|---|---|---|
| Share of excerpt words not in the model's vocabulary | New kinds of text (other genres, dialects, OCR errors) — data drift | Clearly above the range seen in training |
| Mix of predicted periods | A sudden shift suggests a different collection or a pipeline problem | Large change from previous batches |
| Accuracy on a regular sample checked by people, per period | Performance and fairness across periods | Macro-F1 below about 0.45, or one period's recall falling well below the others |
| Rate of reviewer overrides | Users' trust and real-world usefulness | Rising override rate |
| Input checks: length, language, translation notes | Out-of-scope inputs | Any input failing the checks is rejected, not predicted |

Retraining is a governed decision: retrain only on new, checked labels; compare the new model with the current one on
the same protocol; keep the old version for rollback.

## 10. Regulation and governance

- **EU AI Act:** as a cataloguing aid that makes no decisions about people, this would most likely be **minimal risk**.
  Using it to authenticate documents for legal or financial purposes would be out of scope and would need a separate assessment.
- **NIST AI RMF:** *Govern* (owner and out-of-scope uses above), *Map* (stakeholders and harms, Section 7),
  *Measure* (slices, calibration, robustness, Sections 4–5), *Manage* (oversight and monitoring, Sections 8–9).

## 11. Remaining limitations

- Small data: 288 training books (38–76 per period), so all estimates are uncertain (test CI 0.37–0.63).
- Fixed period boundaries treat 1849 and 1851 as different classes; the model is weakest near them.
- Word-frequency features mix up period with topic and genre (e.g. realist fiction, military manuals).
- Probabilities are badly calibrated; recalibration was not tested.
- Label noise and hidden translations remain in both training and test data.

## 12. Recommendation

**Do not deploy as an automatic dating tool.** Accuracy is about 50% across five periods, the model is strongly
overconfident, and it has only been tested on canonical Project Gutenberg books.

At most, a **pilot in shadow mode** could be justified: the model's suggestions are logged next to human cataloguers'
decisions on an undated collection, without being shown or used, to measure real accuracy. Before even that, the
probabilities should be recalibrated, more books per period collected (especially 1850–1918), and the model evaluated
on the target collection.
