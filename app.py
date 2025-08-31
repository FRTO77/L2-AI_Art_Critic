from __future__ import annotations

import os
from io import BytesIO
from typing import Optional

import streamlit as st
from dotenv import load_dotenv
from PIL import Image

from i18n import t
from analysis import compute_metrics, extract_palette, heuristic_style_mood_meaning, suggestions_for_artists
from components import render_palette, render_metrics
from llm import LLMConfig, critique_with_openai, make_prompt


def _load_cfg() -> LLMConfig:
    load_dotenv()
    return LLMConfig(
        provider=os.getenv("LLM_PROVIDER", "OpenAI"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=float(os.getenv("AI_TEMPERATURE", "0.2")),
    )


def main() -> None:
    st.set_page_config(page_title="AI Art Critic", layout="wide")
    cfg = _load_cfg()

    # Sidebar
    with st.sidebar:
        lang = st.selectbox("Language / Язык", ["en", "ru"], index=0, key="aac_lang")
        use_ai = st.toggle(t("sidebar_ai_toggle", lang), value=False, key="aac_ai_toggle")
        st.markdown("---")
        st.caption(t("footer", lang))

    st.title(t("title", lang))
    file = st.file_uploader(t("upload", lang), type=["jpg", "jpeg", "png", "webp"], key="aac_uploader")

    if not file:
        st.info(t("no_image", lang))
        return

    image = Image.open(file)
    st.image(image, use_container_width=True)

    # Analysis
    metrics = compute_metrics(image)
    palette = extract_palette(image, num_colors=5)

    c1, c2 = st.columns([1, 1])
    with c1:
        render_palette(palette, t("palette", lang))
    with c2:
        render_metrics(metrics, t("metrics", lang))

    st.subheader(t("analysis", lang))
    heur = heuristic_style_mood_meaning(metrics, palette)
    tips = suggestions_for_artists(metrics)

    st.markdown(f"**{t('style', lang)}:** {heur['style']}")
    st.markdown(f"**{t('mood', lang)}:** {heur['mood']}")
    st.markdown(f"**{t('meaning', lang)}:** {heur['meaning']}")
    st.markdown(f"**{t('tips', lang)}:**\n- " + "\n- ".join(tips))

    ai_output: Optional[str] = None
    if use_ai and cfg.provider.lower() == "openai":
        prompt = make_prompt(heur["style"], heur["mood"], heur["meaning"], tips)
        with st.spinner("Contacting AI..."):
            ai_output = critique_with_openai(image, prompt, cfg)

    if ai_output:
        st.subheader(t("ai_critique", lang))
        st.write(ai_output)
    else:
        st.subheader(t("heuristic", lang))
        st.info("LLM disabled or unavailable. Showing heuristic critique only.")

    # Export
    if st.button(t("export_md", lang), type="secondary"):
        md = [
            f"# {t('title', lang)}",
            f"- Style: {heur['style']}",
            f"- Mood: {heur['mood']}",
            f"- Meaning: {heur['meaning']}",
            "- Tips:",
        ]
        md.extend([f"  - {x}" for x in tips])
        if ai_output:
            md.append("\n## AI Critique\n" + ai_output)
        md_str = "\n".join(md)
        st.download_button(
            label=t("export_md", lang),
            data=md_str.encode("utf-8"),
            file_name="critique.md",
            mime="text/markdown",
        )


if __name__ == "__main__":
    main()



