# Experiment log

## Seed and evaluation policy

- Every random step uses `config.RANDOM_STATE = 42` (sampling, splits, trees, forest, boosting), so re-running gives the same numbers.
- Exception: each neural-network (MLP) setting is run with 3 seeds (0, 1, 2) for its starting weights, to measure how much
  the result depends on the seed. The folds still use seed 42.
- Model selection uses 5-fold cross-validation on the training set, grouped by author and stratified by period.
  All models use the same folds.
- Main metric: macro-F1. Secondary: accuracy, confusion matrix, share of mistakes in a neighbouring period.
- Settings are chosen with the one-standard-error rule: the simplest setting whose mean macro-F1 is within one standard
  error (std / √5) of the best.
- The test set is used once, at the end, for the chosen model only.

## Runs

All scores are macro-F1 from 5-fold grouped CV on the training set (mean ± std), unless stated otherwise.

### Version 1 data: 446 books (357 train / 89 test)

| ID | Experiment | Settings | Result | Decision |
|---|---|---|---|---|
| E01 | Zero-R baseline | always predicts the most common period | 0.072 ± 0.001 (accuracy 0.221) | The score every model must beat |
| E02 | Logistic regression, tune C | TF-IDF letters only, `min_df=2`; C = 0.1, 1, 10, 100, 1000 | 0.181, 0.417, **0.453**, 0.442, 0.444 | Top words full of character names (sancho, yorick, jules) |
| E03 | Vocabulary size check | LR C=10; `min_df` = 2, 5, 10, 20 | 0.453, 0.440, **0.455**, 0.427 | Use `min_df=10`: same score, fewer names. Run as a separate script, not in a notebook; repeat it by changing `min_df` in `tfidf()` |
| E04 | Logistic regression, tune C | `min_df=10`; C = 0.1, 1, 10, 100, 1000 | 0.200, 0.400, **0.455 ± 0.063**, 0.431, 0.439 | C=10 |
| E05 | kNN, tune k | cosine distance; k = 1, 3, 5, 10, 15, 25, 40 | 0.258, 0.302, 0.299, 0.320, **0.358**, 0.335, 0.329 | k=15 |
| E06 | Decision tree, tune depth | max_depth = 2, 4, 6, 10, 15, 25, None | 0.244, 0.303, **0.311**, 0.278, 0.288, 0.287, 0.287 | depth 6 |
| E07 | Model disagreement | LR C=10, kNN k=15, tree depth 6 | 123 of 357 books wrong for all three | Many look like label problems (wrong dates, translations) |

### Data change

| ID | Change | Result |
|---|---|---|
| D01 | Title-page check added to notebook 02: remove books whose first 3,000 characters show a year more than 20 years after the label, or say they are translated | 87 books removed (49 later year, 47 translations, 9 both); 359 remain (48–95 per period); split 288 train / 71 test |

### Version 2 data: 359 books (288 train / 71 test)

| ID | Experiment | Settings | Result | Decision |
|---|---|---|---|---|
| E08 | Zero-R baseline | as E01 | 0.084 ± 0.002 (accuracy 0.264) | New baseline |
| E09 | Logistic regression, tune C | `min_df=10`; C = 0.1, 1, 10, 100, 1000 | 0.092, 0.363, 0.425, 0.460, **0.474 ± 0.060** | C=100 (0.460 ± 0.067) by the one-standard-error rule |
| E10 | kNN, tune k | k = 1, 3, 5, 10, 15, 25, 40 | 0.301, 0.271, **0.345 ± 0.055**, 0.278, 0.324, 0.287, 0.272 | k=15 (0.324) by the one-standard-error rule |
| E11 | Decision tree, tune depth | max_depth = 2, 4, 6, 10, 15, 25, None | 0.249, 0.306, **0.341 ± 0.038**, 0.337, 0.319, 0.319, 0.319 | depth 6 |
| E12 | Random forest, number of trees | 50, 100, 300, 500 trees | 0.428, 0.498, 0.486, **0.506 ± 0.082** | 100 trees (0.498) by the one-standard-error rule |
| E13 | Gradient boosting, number of rounds | learning rate 0.1, depth 3, `max_features="sqrt"`; 50, 100, 200, 400 rounds | 0.406, 0.439, 0.470, **0.506 ± 0.064** | 400 rounds; still rising |
| E14 | Fold-by-fold comparison | chosen settings, same folds | Boosting beats LR on 4/5 folds (+0.046 per fold on average), forest on 3/5 (+0.039) | Boosting chosen as preferred model |
| E15 | **Final test (run once)** | Boosting, 400 rounds, trained on all 288 training books | **Test macro-F1 0.519, accuracy 0.507**; 80% of mistakes in a neighbouring period | Matches the CV estimate (0.506 ± 0.064) |

### Neural network (notebook 04, same data and folds, cross-validation only)

MLP pipeline: TF-IDF → `StandardScaler(with_mean=False)` → `MLPClassifier` (ReLU, Adam, lr 0.001, batch 32, early stopping on a
10% hold-out, patience 10, max 200 epochs). Each setting is the mean of 3 seeds; "seed ±" is the spread between seeds.

| ID | Experiment | Settings | Result | Decision |
|---|---|---|---|---|
| E16 | First MLP | 1 hidden layer, 64 units, `alpha=1e-4` | 0.467 ± 0.065 (seed ± 0.026); training score 0.933 | Level with LR; heavy overfitting |
| E17 | MLP capacity | 16, 64, 256 units (`alpha=1e-4`) | 0.442, 0.467, 0.472 | No clear effect; 256 units is 3.5× slower |
| E18 | MLP regularisation | 64 units; `alpha` = 1e-4, 0.01, 1, 10, 100 | 0.467, 0.449, 0.465, **0.528 ± 0.051** (seed ± 0.011), 0.491 | `alpha=10` by the one-standard-error rule (threshold 0.505) |
| E19 | MLP learning curves | 64 units, `alpha=1e-4`, seed 0 | Training loss ≈ 0.001 within a few epochs; early stopping ends at 12–14 epochs, so the best hold-out score was around epoch 2–4 | Memorises the training books quickly |
| E20 | Fold-by-fold comparison | MLP `alpha=10` (mean of 3 seeds) vs boosting and LR, same folds | Beats boosting on 3/5 folds (+0.023 on average; two of the wins are ties), beats LR on 4/5 (+0.069) | Comparable to boosting, not consistently better. Boosting stays the preferred model; the MLP is not run on the test set |

### Engineered features and robustness (notebook 05, same data and folds, cross-validation only)

| ID | Experiment | Settings | Result | Decision |
|---|---|---|---|---|
| E21 | Style features alone | avg sentence length, type-token ratio, semicolons per 1,000 words; LR (scaled) and boosting | LR 0.311 ± 0.041, boosting 0.370 ± 0.041 | Clear signal from 3 numbers (Zero-R 0.084); sentence length and semicolons fall steadily over time, type-token ratio shows no trend |
| E22 | TF-IDF + style features | LR C=100 and boosting 400 rounds, no other changes | LR 0.463 ± 0.070 (vs 0.460; better on 3/5 folds), boosting 0.482 ± 0.063 (vs 0.506; worse on 4/5) | Not added to the final model; used for interpretation only |
| E23 | Robustness to excerpt position | Trained on middle excerpts; validation books scored on excerpts 25% / 50% / 75% through the book | Boosting 0.481 / 0.506 / 0.514; LR 0.445 / 0.460 / 0.462 | Robust: changes ≤ 0.025, well inside the fold spread. 23% of books' 25%/75% excerpts overlap the middle one (13% of words on average) |

### Error analysis and interpretation (notebook 06, preferred model: boosting 400 rounds)

| ID | Experiment | Settings | Result | Decision |
|---|---|---|---|---|
| E24 | Out-of-fold error slices | Same 5 folds; 95% CIs from 1,000 author-level bootstrap resamples | Overall accuracy 0.50 (CI 0.44–0.55); 1850–1899 recall 0.39 (0.28–0.52), 1900–1918 0.61 (0.50–0.72); within 10 years of a boundary 0.40 (0.32–0.47) vs 0.59 (0.50–0.66); 82% of errors in a neighbouring period | 1850–1899 and books near boundaries are the main weaknesses |
| E25 | 1850–1899 / 1900–1918 confusion | Out-of-fold predictions | 65 of 147 books confused; median 10 vs 11 years from 1900 (confused vs correct) | Not mainly a boundary effect; topic/genre seems to play a part |
| E26 | Test set with uncertainty (reporting only) | Final model from notebook 03, rebuilt | Macro-F1 0.52 (CI 0.37–0.63), accuracy 0.51 (0.39–0.62) | Same as E15; nothing chosen from it |
| E27 | Calibration | Out-of-fold `predict_proba` | Average confidence 0.78 vs accuracy 0.50, ECE 0.28; >0.95 confident books only 64% correct | Strongly overconfident; probabilities not to be shown as confidence |
| E28 | Global explanation | Permutation importance on held-out folds, top 150 words per fold, 5 repeats | Largest mean drop ≈ 0.01 macro-F1; most top words matter in only 1–2 folds | Reliance spread over many words; old spellings/formal words vs plainer modern words |
| E29 | Local explanation | Leave-one-word-out, first 1850–1899 test book predicted 1900–1918 (*Demos*, Gissing, 1886) | Predicted 1900–1918 at 96%; contractions (*wasn*, *doesn*) and *newspaper*, *working* push towards 1900s | Example of confident failure on realist late-Victorian prose |

The full results table, including fold scores and timings, is saved by notebook 03 to `reports/experiment_results.csv`;
the MLP results are saved by notebook 04 to `reports/mlp_results.csv`, notebook 05's to `reports/features_robustness_results.csv`,
and notebook 06's to `reports/error_slices.csv`, `reports/calibration_boosting.csv` and `reports/permutation_importance_boosting.csv`.
