# Upload to GitHub

Suggested repository name: `aapl-intelligent-system`

Suggested description: `Streamlit research dashboard for AAPL forecasting, ensemble explainability, GJR-GARCH volatility and financial-report retrieval.`

Suggested topics: `python`, `streamlit`, `time-series`, `stock-forecasting`, `explainable-ai`, `rag`, `research`.

## Browser upload

1. Extract the ZIP. Open its `aapl-intelligent-system` folder.
2. On GitHub, create a new repository with the suggested name. Choose public or private visibility yourself. Leave automatic README, license and gitignore initialization unchecked because the folder already supplies README and gitignore files.
3. Choose **uploading an existing file** (or **Add file → Upload files**).
4. Upload the contents of the folder, not the ZIP. `app.py`, `requirements.txt` and `README.md` must appear at the repository root.
5. Include `.github`, `.streamlit`, `.gitignore` and `.gitattributes`. They are part of the package; file managers may hide dot-prefixed files.
6. Commit with a message such as `Add AAPL Intelligent System dashboard`.
7. Inspect the README and open the Actions tab to see the test result after GitHub runs it.

Do not upload `.venv`, API keys, populated `secrets.toml` or private financial reports. The package does not include an actual secrets file.

## Git command line

From inside the extracted folder, with Git installed:

```sh
git init
git add .
git status
git commit -m "Add AAPL Intelligent System dashboard"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/aapl-intelligent-system.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your account name and create the empty remote repository first. Review `git status` before committing. Authentication uses your own GitHub credentials.

## Hosting

Uploading source to GitHub does not run a Streamlit server. GitHub Pages cannot execute this Python application. You can run it locally using the README instructions. A public hosted version needs separate hosting and access/privacy decisions.
