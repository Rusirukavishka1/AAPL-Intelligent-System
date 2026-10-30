# Included research exports

These are saved artifacts supplied with the research dashboard, not live market data.

| File | Contents |
| --- | --- |
| `research.json` | Dashboard metadata, model outputs, metrics and ensemble contributions |
| `corpus.json` | Built-in research passages for retrieval |
| `test_predictions.csv` | Historical predictions and actual outcomes |
| `test_metrics_by_seed.csv` | Price and directional metrics across three seeds |
| `direction_accuracy_CI.csv` | Previously computed block-bootstrap intervals |
| `paired_DA_family_adjusted.csv` | Previously computed paired directional comparisons |
| `prospective_validation_folds.csv` | Saved pre-test validation results |
| `tuning_trials.csv` | Recorded candidate settings and selection results |
| `leakage_checks.csv` | Programmed audit outcomes from the archived experiment |

Source coverage is 2010-01-04 to 2026-10-01. The saved historical test has 629 targets from 2024-04-01 to 2026-10-01 for seeds 42, 123 and 2026. The raw source CSV, fitted model binaries and training notebook are not included here.

The included presentation exports retain the currently selected models. Paired inference retains its original adjustment family; no new statistical analysis was performed during repository preparation. Checks are evidence about the implemented protocol, not proof that all sources of bias are absent. The test era was previously inspected, and source data provenance and redistribution rights need owner confirmation.

Do not place personal reports or API credentials in this directory.
