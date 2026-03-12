 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/README.md b/README.md
index 41174bebf3a0f64fcf715b1a16f8c4122d17488b..9b70e073cc5620556462538b1567bd0d09f1f531 100644
--- a/README.md
+++ b/README.md
@@ -1,19 +1,31 @@
-# 🎈 Blank app template
+# Medicare MARx + SunFire Roleplay Simulator
 
-A simple Streamlit app template for you to modify!
+This repository runs a Streamlit app that hosts a browser-based training simulator.
 
-[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)
+## What files should be in GitHub?
+Put these files in the **root** of your repo:
 
-### How to run it on your own machine
+- `streamlit_app.py` (main app)
+- `requirements.txt` (Python dependency list)
+- `README.md`
 
-1. Install the requirements
+If you deploy with Streamlit Community Cloud, set:
 
-   ```
-   $ pip install -r requirements.txt
-   ```
+- **Main file path**: `streamlit_app.py`
 
-2. Run the app
+## Run locally
 
-   ```
-   $ streamlit run streamlit_app.py
-   ```
+```bash
+pip install -r requirements.txt
+streamlit run streamlit_app.py
+```
+
+Then open the local URL shown in the terminal (usually `http://localhost:8501`).
+
+## If it "isn't working"
+
+1. Hard refresh the page (`Ctrl+Shift+R` / `Cmd+Shift+R`).
+2. Confirm JavaScript is enabled.
+3. Use Chrome/Edge for best voice API compatibility.
+4. Voice input may fail in some hosted iframe environments due to browser policy.
+5. Even without voice support, typing in the chat still works.
 
EOF
)
