# Architecture and data flow

`app.py` loads `data/research.json` and `data/corpus.json` relative to its own location. Selecting a seed selects matching historical rows, metrics and attribution arrays. Charts do not retrain the original forecasting models.

## Quantitative Engine

Saved base forecasts, stacking results and volatility outputs feed comparison tables and historical charts. Ridge explanations add signed input contributions to a reference prediction. XGBoost explanations add TreeSHAP contributions to a row-specific bias. Reconstruction tests compare those sums with the exported predictions. These are model explanations, not causal explanations of market movements.

## AI Knowledge Engine

`rag.ingest` extracts PDF pages or decodes UTF-8 text. It forms overlapping passages of up to 1,200 characters with a 1,000-character stride. Each passage retains title, page, source kind and availability date.

`rag.retrieve` filters by selected source scope and cutoff, then applies a BM25-style lexical score. It returns up to five passages, requiring two distinct matching query tokens when the query contains at least two retained tokens.

Optional `rag.generate` sends the question and passages to the Responses API. It requests source labels and an English answer and handles provider errors. Retrieved text is treated as evidence, not instructions. Citation-ID validation does not establish factual support.

Uploads, submitted search settings and the last result remain in session state. They are not shared persistent document storage. Credentials are supplied at runtime; the example file is blank. The local launchers bind to loopback.
