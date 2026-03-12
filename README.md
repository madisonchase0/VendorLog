# Medicare MARx + SunFire Roleplay Simulator

This repository runs a Streamlit app that hosts a browser-based training simulator.

## What files should be in GitHub?
Put these files in the **root** of your repo:

- `streamlit_app.py` (main app)
- `requirements.txt` (Python dependency list)
- `README.md`

If you deploy with Streamlit Community Cloud, set:

- **Main file path**: `streamlit_app.py`

## Run locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Then open the local URL shown in the terminal (usually `http://localhost:8501`).

## If it "isn't working"

1. Hard refresh the page (`Ctrl+Shift+R` / `Cmd+Shift+R`).
2. Confirm JavaScript is enabled.
3. Use Chrome/Edge for best voice API compatibility.
4. Voice input may fail in some hosted iframe environments due to browser policy.
5. Even without voice support, typing in the chat still works.
