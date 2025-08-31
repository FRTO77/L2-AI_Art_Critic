# AI Art Critic / Image Describer

An AI-powered image critic and describer. Upload a photo, painting, or design and get:
- Style, mood, and possible meaning
- Technical analysis (palette, brightness/contrast, sharpness, colorfulness)
- Actionable suggestions for artists to improve composition and impact

Why it’s cool: a practical blend of Computer Vision and LLM reasoning. It makes your portfolio stand out with insightful, structured feedback.

Important: This is subjective critique, not an absolute truth. Use it creatively.

## Features
- Image upload (JPG, PNG, WEBP)
- Color palette extraction and visual swatches
- Metrics: brightness, contrast, saturation, sharpness, colorfulness
- Heuristic style/mood/meaning narrative
- Optional LLM critique (OpenAI Vision). If unavailable, a heuristic critique is provided.
- Export to Markdown
- Bilingual UI (English / Russian)

## Quickstart
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r AI_Art_Critic\requirements.txt

# Generate .env and .env.example
python AI_Art_Critic\create_env.py

# Run the app
streamlit run AI_Art_Critic\app.py
```

## Configuration (.env)
The generator creates `AI_Art_Critic/.env` with placeholders. Keys:
```dotenv
LLM_PROVIDER=OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
AI_TEMPERATURE=0.2
```
Notes:
- If OpenAI isn’t configured, the app still works with heuristic critique.
- Do not commit `.env` to Git.

## Usage
1. Choose language in the sidebar (English or Русский).
2. Upload an image.
3. Review palette, metrics, and heuristic analysis.
4. Optionally enable “Use AI model” for a deeper LLM critique.
5. Export the result as Markdown if desired.

## Tech Stack
- Python, Streamlit
- Pillow, NumPy, scikit-image, scikit-learn
- LangChain (+ OpenAI Vision via `langchain-openai`)
- `python-dotenv` for configuration

## Project Structure
- `app.py` — Streamlit UI and orchestration
- `analysis.py` — image metrics, palette extraction, heuristic narratives
- `llm.py` — LLM integration (OpenAI Vision) and fallbacks
- `components.py` — UI helpers (palette, metrics, sections)
- `i18n.py` — simple bilingual strings (EN/RU)
- `create_env.py` — generates `.env` and `.env.example`
- `requirements.txt`, `.gitignore`, `__init__.py`

## Security & Privacy
- Images are processed locally; if LLM is enabled, a low-resolution base64 preview is sent to the model provider.
- Keep your API keys in `.env` and never commit them.




