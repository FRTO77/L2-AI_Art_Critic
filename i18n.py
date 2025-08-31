from __future__ import annotations

from typing import Dict


STRINGS: Dict[str, Dict[str, str]] = {
    "en": {
        "title": "AI Art Critic / Image Describer",
        "sidebar_language": "Language",
        "sidebar_ai_toggle": "Use AI model (OpenAI Vision)",
        "upload": "Upload image",
        "palette": "Color Palette",
        "metrics": "Image Metrics",
        "analysis": "Analysis",
        "heuristic": "Heuristic Critique",
        "ai_critique": "AI Critique",
        "export_md": "Export to Markdown",
        "style": "Style",
        "mood": "Mood",
        "meaning": "Possible meaning",
        "tips": "Suggestions for artists",
        "no_image": "Please upload an image to begin.",
        "footer": "Subjective critique. Use creatively.",
    },
    "ru": {
        "title": "AI‑критик / Описатель изображений",
        "sidebar_language": "Язык",
        "sidebar_ai_toggle": "Использовать AI (OpenAI Vision)",
        "upload": "Загрузите изображение",
        "palette": "Палитра",
        "metrics": "Метрики изображения",
        "analysis": "Аналитика",
        "heuristic": "Эвристическая критика",
        "ai_critique": "AI‑критика",
        "export_md": "Экспорт в Markdown",
        "style": "Стиль",
        "mood": "Настроение",
        "meaning": "Возможный смысл",
        "tips": "Советы художникам",
        "no_image": "Пожалуйста, загрузите изображение.",
        "footer": "Субъективная критика. Используйте творчески.",
    },
}


def t(key: str, lang: str = "en") -> str:
    lang_map = STRINGS.get(lang, STRINGS["en"])  # fallback to en
    return lang_map.get(key, key)



