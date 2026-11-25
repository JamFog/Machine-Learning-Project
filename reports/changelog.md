# Reflective changelog

The consequential decisions and changes made during the project, why each was made, and the evidence behind it.
Experiment IDs (E…, D…) refer to `reports/experiment_log.md`.

| # | Milestone | Change | Why | Evidence |
|---|---|---|---|---|
| 1 | 2 | Sampled 100 books per period instead of using all of PG-19 | Periods range from 396 to 13,144 books; a model trained on all of them could score well by guessing recent periods | Notebook 01, period counts |
| 2 | 2 | Reduced every book to a 5,000-word excerpt from the middle, after removing books under 5,000 words | Older books were shorter, so length could reveal the period; the start and end contain modern introductions and notes | Notebook 02; leakage register risks 4–5 |
| 3 | 2 | Split and cross-validation grouped by author | Otherwise the model can recognise an author instead of a period | Leakage register risk 1 |
| 4 | 3 | TF-IDF keeps letters only | Years written in the text would give away the period | Leakage register risk 3 |
| 5 | 3 | `min_df` raised from 2 to 10 | Top logistic-regression words were character names (sancho, yorick); `min_df=10` kept the same score with fewer names | E02–E03 |
| 6 | 3 | Dropped Naive Bayes from the original plan | Not taught in the module; logistic regression, kNN, tree, random forest and boosting were used instead | README plan vs notebook 03 |
| 7 | 3 | Added the title-page check (87 books removed) and re-ran every model | Error analysis showed 123 of 357 training books were wrong for all three models, many because of wrong dates or translations. The rule is applied to every book before the split, not only to misclassified ones | E07, D01; leakage register risk 9 |
| 8 | 3 | Chose settings with the one-standard-error rule and gradient boosting as the preferred model | Avoids picking the luckiest setting; boosting was best on CV and beat LR on 4 of 5 folds | E09–E14 |
| 9 | 3 | Test set used once, for boosting only | Brief rule; keeps the final estimate honest | E15 (test macro-F1 0.52) |
| 10 | 4 | Corrected wording in notebooks 01–02 (First Folio grouping, Don Quixote date, "only books originally written in English") | The text claimed more than the code did | Notebook 01–02 checks against `train.csv` / `sample.csv` |
| 11 | 4 | Added a small MLP but **did not** adopt it | Comparable to boosting on CV (0.528 vs 0.506) but not consistently better across folds, seed-sensitive, overfits and harder to interpret; testing it would mean choosing after seeing test scores | E16–E20 |
| 12 | 4 | Re-timed models in the same session | Training times differed 3–4× between sessions, which had made the MLP look faster than boosting | Notebook 04 timing table |
| 13 | 4 | Tested three style features but **did not** add them | Clear trends over time and 0.37 macro-F1 alone, but no gain when added to TF-IDF (boosting got worse) | E21–E22 |
| 14 | 4 | Robustness check on other parts of each book | To check the middle excerpt wasn't driving the results; scores changed by at most 0.025 | E23 |
| 15 | 4 | Error slices with author-level bootstrap intervals | Single-number scores hid that 1850–1899 (recall 0.39) and books near a period boundary (0.40) are much harder | Notebook 06 |
