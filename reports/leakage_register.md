# Leakage register

Leakage is when information that would not be available when making a real prediction gets into training or
evaluation, making the scores look better than they really are. Each risk below lists how it could leak, how it is
handled, and what risk remains.

| # | Risk | How it could leak | How it is handled | Where | Remaining risk |
|---|---|---|---|---|---|
| 1 | Same author in train and test | The model recognises an author's style or recurring topics instead of the period | Train/test split and every CV fold are grouped by author (`StratifiedGroupKFold`); 0 authors appear in both sets | Notebook 02, 03 | Author names come from titles, so spelling variants (e.g. "E. Phillips Oppenheim" vs "E. Philips Oppenheim") count as different authors |
| 2 | Same work in train and test | Volumes, parts or editions of one work share most of their text | Titles reduced to a "work" key and only the earliest copy of each work kept | Notebook 01 | Anthologies can overlap with single works (e.g. the Shakespeare First Folio) |
| 3 | Years written in the text | A year like "1850" in the text directly gives away the period | TF-IDF keeps letters only (`token_pattern`), so numbers are never features | Notebook 03 | Years written as words (e.g. "eighteen hundred") are still kept |
| 4 | Text added after publication | Modern introductions, footnotes and editor's notes use later language than the label | 5,000-word excerpt from the middle of each book; text in [square brackets] and "FOOTNOTES" headings removed | Notebook 02 | 5 of 359 excerpts still mention a footnote or transcriber |
| 5 | Book length | Older books in the sample are shorter, so length could reveal the period | Books under 5,000 words removed; every excerpt is exactly 5,000 words | Notebook 02 | None found |
| 6 | Preprocessing fitted on all data | Building the TF-IDF vocabulary on every book lets validation/test books influence training | TF-IDF is inside the model pipeline, so it is fitted on the training part of each fold only | Notebook 03 | None found |
| 7 | Using the test set to make choices | Tuning or choosing a model using test scores makes the test score optimistic | Test-set rule: all tuning and model choice use CV on the training set; the test set is used once, on the chosen model only | Notebook 03 | None found; the test cell was run once and nothing was changed afterwards |
| 8 | Character and place names | The model memorises names from individual books instead of learning period language | Author-grouped split (names don't carry over); `min_df=10` removes words found in fewer than 10 books | Notebook 03 | Common first names (e.g. harry, john) remain; they may partly reflect names popular at the time |
| 9 | Removing books based on model errors | Removing only the books a model got wrong makes the scores look better | Label clean-up is done by rules applied to every book before the split (year check, title-page check), never by hand-picking misclassified books | Notebook 02 | The title-page rule was prompted by error analysis on the training folds, but it is applied to all books equally |

## Related: label quality

Not leakage, but it affects how far the scores can be trusted:
- Some PG-19 publication dates are wrong (e.g. *The Submarine Boys for the Flag*, labelled 1705, published c. 1910).
  Books with a much later year in the excerpt or on the title page are removed, but books that mention no year are not caught.
- Translations are dated by either the original or the translation. Translations that say so on the title page are removed;
  others remain (e.g. *The Princess of Montpensier*).
