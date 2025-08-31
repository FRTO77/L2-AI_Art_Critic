from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel
from PIL import Image
from io import BytesIO

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage


class LLMConfig(BaseModel):
    provider: str = "OpenAI"
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o-mini"
    temperature: float = 0.2


PROMPT_SYSTEM = (
    "You are an expert art critic and curator. You analyze images with structured, practical feedback: "
    "style, mood, symbolism/meaning, composition, lighting, color theory, and actionable advice. "
    "Be concise and helpful."
)


def _image_to_base64_jpeg(image: Image.Image, max_side: int = 1024, quality: int = 85) -> str:
    img = image.convert("RGB")
    w, h = img.size
    scale = max_side / max(w, h)
    if scale < 1.0:
        img = img.resize((int(w * scale), int(h * scale)))
    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=quality)
    b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{b64}"


def critique_with_openai(image: Image.Image, prompt: str, cfg: LLMConfig) -> Optional[str]:
    if not cfg.openai_api_key:
        return None
    try:
        model = ChatOpenAI(model=cfg.openai_model, temperature=cfg.temperature, api_key=cfg.openai_api_key)
        image_b64 = _image_to_base64_jpeg(image)
        content = [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": image_b64}},
        ]
        messages = [SystemMessage(content=PROMPT_SYSTEM), HumanMessage(content=content)]
        resp = model.invoke(messages)
        return getattr(resp, "content", None)
    except Exception:
        return None


def make_prompt(style: str, mood: str, meaning: str, tips: list[str]) -> str:
    tips_str = "\n".join(f"- {t}" for t in tips)
    return (
        "Analyze this artwork. Provide: style, mood, symbolism/meaning, composition, lighting, color critique, and actionable improvements.\n"
        f"Heuristic baseline:\nStyle: {style}\nMood: {mood}\nMeaning: {meaning}\n"
        f"Initial tips:\n{tips_str}\n"
        "Be concise, structured, and practical."
    )


