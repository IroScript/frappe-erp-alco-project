"""
Dynamic Color Extraction & Gradient Engine for Alco Pharma E-Commerce
Extracts dominant color distribution (>50% primary, 2nd largest secondary)
from actual product packaging image pixels.
"""

import colorsys
import io
import json
import os
import urllib.request
from collections import defaultdict
from PIL import Image

# Global in-memory and disk cache for ultra-fast response (0ms)
CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "gradient_cache.json")
GRADIENT_CACHE: dict[str, tuple[str, str, str, list[dict]]] = {}

if os.path.exists(CACHE_FILE):
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            _loaded = json.load(f)
            for k, v in _loaded.items():
                GRADIENT_CACHE[k] = tuple(v)
    except Exception:
        pass

def save_cache_to_disk():
    try:
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(GRADIENT_CACHE, f, indent=2)
    except Exception:
        pass

def build_deep_light_gradient(primary_hex: str, secondary_hex: str = None, has_distinct_secondary: bool = False) -> tuple[str, str, str, str]:
    """
    Constructs a modern 3-stop deep-to-light luxury gradient from extracted packaging colors.
    Stop 1 (0%): Deep shadow shade of primary hue (anchor for contrast & readability)
    Stop 2 (55%): Vibrant mid-tone body of primary hue (energetic brand color)
    Stop 3 (100%): Radiant light highlight (secondary color pop or specular tint)
    """
    def hex_to_rgb(h_str):
        h_str = h_str.lstrip('#')
        return tuple(int(h_str[i:i+2], 16) / 255.0 for i in (0, 2, 4))

    def rgb_to_hex(r, g, b):
        return f"#{int(round(r*255)):02x}{int(round(g*255)):02x}{int(round(b*255)):02x}"

    def hsl_to_hex(h, l, s):
        r, g, b = colorsys.hls_to_rgb(h, max(0.0, min(1.0, l)), max(0.0, min(1.0, s)))
        return rgb_to_hex(r, g, b)

    h1, l1, s1 = colorsys.rgb_to_hls(*hex_to_rgb(primary_hex))
    
    # 1. Deep part (0%): Rich, deep dark tone (L: ~21%, high saturation)
    deep_hex = hsl_to_hex(h1, 0.21, min(0.92, max(0.78, s1 * 1.15)))
    
    # 2. Mid part (55%): Vibrant energetic packaging tone (L: ~43%)
    mid_hex = hsl_to_hex(h1, 0.43, min(0.88, max(0.72, s1 * 1.10)))
    
    # 3. Light part (100%): Radiant luminous accent
    if has_distinct_secondary and secondary_hex:
        h2, l2, s2 = colorsys.rgb_to_hls(*hex_to_rgb(secondary_hex))
        light_hex = hsl_to_hex(h2, 0.58, min(0.92, max(0.72, s2 * 1.10)))
    else:
        # Monochromatic specular highlight
        light_hex = hsl_to_hex(h1, 0.63, min(0.82, max(0.60, s1 * 0.95)))
        
    gradient = f"linear-gradient(135deg, {deep_hex} 0%, {mid_hex} 55%, {light_hex} 100%)"
    return gradient, deep_hex, mid_hex, light_hex

def extract_dynamic_gradient(image_source: str) -> tuple[str, str, str, list[dict]]:
    """
    Extracts primary and secondary dominant colors from an image,
    calculates exact percentage breakdown, and returns dynamic CSS gradient.

    Returns:
        (gradient_css, primary_hex, secondary_hex, breakdown_list)
    """
    if not image_source:
        return "linear-gradient(135deg, #1e3a8a 0%, #0284c7 100%)", "#1e3a8a", "#0284c7", []

    if image_source in GRADIENT_CACHE:
        return GRADIENT_CACHE[image_source]

    try:
        if image_source.startswith("http://") or image_source.startswith("https://"):
            req = urllib.request.Request(image_source, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                raw_bytes = resp.read()
            img = Image.open(io.BytesIO(raw_bytes))
        else:
            img = Image.open(image_source)

        img = img.convert("RGBA")
        # Resize to 100x100 for fast & statistically robust sampling
        img = img.resize((100, 100), Image.Resampling.LANCZOS)
        pixels = list(img.getdata())
    except Exception as err:
        default_grad = "linear-gradient(135deg, #1e3a8a 0%, #0284c7 100%)"
        return default_grad, "#1e3a8a", "#0284c7", [{"color": "Blue", "percentage": 100.0, "hex": "#1e3a8a"}]

    # Filter out transparent or plain white/light-gray background pixels
    product_pixels = []
    for r, g, b, a in pixels:
        if a < 128:
            continue
        h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        # Background filter: near-white or pure white
        if v > 0.90 and s < 0.12:
            continue
        # Pure dark / edge noise
        if v < 0.08:
            continue
        product_pixels.append((r, g, b, h * 360, s, v))

    if not product_pixels:
        default_grad = "linear-gradient(135deg, #1e3a8a 0%, #0284c7 100%)"
        GRADIENT_CACHE[image_source] = (default_grad, "#1e3a8a", "#0284c7", [])
        return GRADIENT_CACHE[image_source]

    # Classify pixels into standard chromatic color families
    buckets = defaultdict(list)
    for r, g, b, h, s, v in product_pixels:
        if s < 0.16:
            bucket_name = "Neutral"
        elif h >= 345 or h < 15:
            bucket_name = "Red"
        elif 15 <= h < 42:
            bucket_name = "Orange"
        elif 42 <= h < 68:
            bucket_name = "Yellow"
        elif 68 <= h < 165:
            bucket_name = "Green"
        elif 165 <= h < 195:
            bucket_name = "Teal"
        elif 195 <= h < 255:
            bucket_name = "Blue"
        elif 255 <= h < 290:
            bucket_name = "Purple"
        else:
            bucket_name = "Pink"
        buckets[bucket_name].append((r, g, b, s, v))

    # Calculate exact percentages for chromatic colors
    chromatic_total = sum(len(v) for k, v in buckets.items() if k != "Neutral")
    if chromatic_total > 0:
        pcts = {k: (len(v) / chromatic_total) * 100 for k, v in buckets.items() if k != "Neutral"}
    else:
        total = len(product_pixels)
        pcts = {k: (len(v) / total) * 100 for k, v in buckets.items()}

    sorted_colors = sorted(pcts.items(), key=lambda x: x[1], reverse=True)

    def get_vibrant_hex(pixel_list):
        # Sort by saturation & brightness to get the most vibrant representative color
        sorted_px = sorted(pixel_list, key=lambda x: (x[3] * 0.7 + x[4] * 0.3), reverse=True)
        top_n = max(1, int(len(sorted_px) * 0.35))
        sample = sorted_px[:top_n]
        r = int(sum(p[0] for p in sample) / top_n)
        g = int(sum(p[1] for p in sample) / top_n)
        b = int(sum(p[2] for p in sample) / top_n)
        # Ensure sufficient luminance contrast for white text
        lum = 0.299 * r + 0.587 * g + 0.114 * b
        if lum > 190:
            factor = 180 / lum
            r = int(r * factor)
            g = int(g * factor)
            b = int(b * factor)
        return f"#{r:02x}{g:02x}{b:02x}", (r, g, b)

    primary_name, primary_pct = sorted_colors[0]
    primary_hex, (pr, pg, pb) = get_vibrant_hex(buckets[primary_name])

    breakdown_list = []
    for c_name, c_pct in sorted_colors:
        c_hex, _ = get_vibrant_hex(buckets[c_name])
        breakdown_list.append({
            "color": c_name,
            "percentage": round(c_pct, 1),
            "hex": c_hex
        })

    # Determine secondary color: second largest distinct color
    has_distinct_secondary = len(sorted_colors) > 1 and sorted_colors[1][1] >= 5.0
    if has_distinct_secondary:
        secondary_name, secondary_pct = sorted_colors[1]
        secondary_hex, _ = get_vibrant_hex(buckets[secondary_name])
    else:
        secondary_hex = None

    gradient, deep_hex, mid_hex, light_hex = build_deep_light_gradient(
        primary_hex, secondary_hex, has_distinct_secondary
    )
    result = (gradient, primary_hex, secondary_hex or light_hex, breakdown_list)
    GRADIENT_CACHE[image_source] = result
    save_cache_to_disk()
    return result
