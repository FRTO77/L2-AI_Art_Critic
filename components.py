from __future__ import annotations

from typing import List, Tuple

import streamlit as st

from analysis import ImageMetrics, rgb_to_hex


def render_palette(palette: List[Tuple[int, int, int]], title: str) -> None:
    st.subheader(title)
    cols = st.columns(len(palette)) if palette else [st]
    for idx, color in enumerate(palette):
        hex_code = rgb_to_hex(color)
        with cols[idx]:
            st.markdown(
                f"<div style='height:64px;border-radius:8px;background:{hex_code};border:1px solid rgba(0,0,0,0.1)'></div>",
                unsafe_allow_html=True,
            )
            st.caption(hex_code)


def render_metrics(metrics: ImageMetrics, title: str) -> None:
    st.subheader(title)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Brightness", f"{metrics.brightness:.2f}")
        st.metric("Contrast", f"{metrics.contrast:.2f}")
    with c2:
        st.metric("Saturation", f"{metrics.saturation:.2f}")
        st.metric("Sharpness", f"{metrics.sharpness:.3f}")
    with c3:
        st.metric("Colorfulness", f"{metrics.colorfulness:.2f}")
        st.metric("Resolution", f"{metrics.width}×{metrics.height}")



