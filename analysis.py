from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Dict

import numpy as np
from PIL import Image, ImageStat, ImageFilter
from sklearn.cluster import KMeans
from skimage import color as skcolor


@dataclass
class ImageMetrics:
    width: int
    height: int
    brightness: float
    contrast: float
    saturation: float
    sharpness: float
    colorfulness: float


def _to_numpy_rgb(image: Image.Image) -> np.ndarray:
    if image.mode != "RGB":
        image = image.convert("RGB")
    return np.asarray(image)


def compute_metrics(image: Image.Image) -> ImageMetrics:
    img_rgb = image.convert("RGB")
    width, height = img_rgb.size

    # Brightness and contrast via PIL stats
    stat = ImageStat.Stat(img_rgb)
    mean = np.mean(stat.mean)
    rms = np.mean(stat.rms)
    brightness = mean / 255.0
    contrast = min(max((rms - mean) / 255.0 + 0.5, 0.0), 1.0)

    # Saturation via HSV
    hsv = img_rgb.convert("HSV")
    sat_channel = np.asarray(hsv)[:, :, 1].astype(np.float32) / 255.0
    saturation = float(np.clip(np.mean(sat_channel), 0.0, 1.0))

    # Sharpness via Laplacian variance proxy (using edge enhancement)
    edges = img_rgb.filter(ImageFilter.FIND_EDGES)
    edges_np = np.asarray(edges.convert("L"), dtype=np.float32)
    sharpness = float(np.var(edges_np) / (255.0 ** 2))

    # Colorfulness (Hasler and Süsstrunk proxy)
    arr = _to_numpy_rgb(img_rgb).astype(np.float32)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    rg = np.abs(r - g)
    yb = np.abs(0.5 * (r + g) - b)
    std_rg, std_yb = np.std(rg), np.std(yb)
    mean_rg, mean_yb = np.mean(rg), np.mean(yb)
    colorfulness = float(np.sqrt(std_rg**2 + std_yb**2) + 0.3 * np.sqrt(mean_rg**2 + mean_yb**2)) / 255.0

    return ImageMetrics(
        width=width,
        height=height,
        brightness=float(brightness),
        contrast=float(np.clip(contrast, 0.0, 1.0)),
        saturation=saturation,
        sharpness=sharpness,
        colorfulness=float(np.clip(colorfulness, 0.0, 1.0)),
    )


def extract_palette(image: Image.Image, num_colors: int = 5, sample_size: int = 30000) -> List[Tuple[int, int, int]]:
    img = image.convert("RGB")
    arr = np.asarray(img)
    h, w, _ = arr.shape
    pixels = arr.reshape(-1, 3)
    if pixels.shape[0] > sample_size:
        idx = np.random.choice(pixels.shape[0], sample_size, replace=False)
        pixels = pixels[idx]

    # KMeans for palette
    kmeans = KMeans(n_clusters=num_colors, n_init=4, random_state=42)
    kmeans.fit(pixels)
    centers = kmeans.cluster_centers_.astype(np.uint8)
    palette = [tuple(map(int, c)) for c in centers]
    return palette


def heuristic_style_mood_meaning(metrics: ImageMetrics, palette: List[Tuple[int, int, int]]) -> Dict[str, str]:
    # Basic heuristic narrative
    mood = []
    if metrics.brightness < 0.35:
        mood.append("dark")
    elif metrics.brightness > 0.65:
        mood.append("bright")
    if metrics.saturation > 0.6:
        mood.append("vivid")
    elif metrics.saturation < 0.25:
        mood.append("muted")
    if metrics.colorfulness > 0.6:
        mood.append("colorful")
    
    style = []
    if metrics.sharpness > 0.015 and metrics.contrast > 0.55:
        style.append("crisp/graphic")
    if metrics.saturation < 0.3 and metrics.brightness > 0.6:
        style.append("minimal/airy")
    if metrics.saturation > 0.55 and metrics.colorfulness > 0.55:
        style.append("expressive")

    meaning = "The image suggests an atmosphere that could be interpreted based on color and contrast relationships. Consider focal points and narrative hints to strengthen the message."

    return {
        "style": ", ".join(style) or "mixed",
        "mood": ", ".join(mood) or "balanced",
        "meaning": meaning,
    }


def suggestions_for_artists(metrics: ImageMetrics) -> List[str]:
    tips: List[str] = []
    if metrics.brightness < 0.3:
        tips.append("Increase exposure or lift shadows to reveal details in dark regions.")
    if metrics.brightness > 0.75:
        tips.append("Reduce highlights to avoid washed-out areas; add tonal depth.")
    if metrics.contrast < 0.45:
        tips.append("Increase contrast or refine local contrast to enhance separation.")
    if metrics.saturation < 0.25:
        tips.append("Introduce accent colors or selective saturation to add interest.")
    if metrics.saturation > 0.75:
        tips.append("Dial back saturation or balance hues for a more cohesive palette.")
    if metrics.sharpness < 0.008:
        tips.append("Add subtle sharpening or increase edge clarity for definition.")
    if metrics.colorfulness < 0.25:
        tips.append("Consider a richer palette or stronger color contrasts to elevate impact.")
    if not tips:
        tips.append("Strong technical balance. Explore composition and storytelling refinements.")
    return tips


def rgb_to_hex(color: Tuple[int, int, int]) -> str:
    return "#%02x%02x%02x" % color



