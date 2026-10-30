# Package validation

Validated on 30 October 2026 in a clean Linux virtual environment.

- All five existing unittest tests passed.
- Application source and pinned runtime requirements were preserved from the latest supplied dashboard package.
- A scan found no common API-key/private-key patterns or populated secrets.toml file in the prepared repository.
- Removed stale documentation references to an absent training notebook.
- Excluded caches, environments and old build logs from the archive.

Command: `python -m unittest discover -s tests -v`

The tests check page navigation, seed selection, XGBoost explanation selection, retrieval interaction, home shortcuts, evidence filters and additive explanation reconstruction. This is not a live LLM evaluation or a user acceptance study. Windows launchers were retained but not executed on Windows. The GitHub Actions matrix is supplied; its remote runs have not occurred yet.

Environment used for this local test:

- Python 3.12.14
- streamlit 1.50.0
- plotly 6.3.1
- pandas 2.2.3
- pypdf 6.1.3
