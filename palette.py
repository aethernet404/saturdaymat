#!/usr/bin/env python3
"""Generate a color palette chart for Saturday Mat website."""
import struct, zlib, os

colors = [
    ("Sand",       "#F3E7D3", (243, 231, 211)),
    ("Shell",      "#FBF6EB", (251, 246, 235)),
    ("Seaglass",   "#6E9A90", (110, 154, 144)),
    ("Deep Sea",   "#2E4A45", (46, 74, 69)),
    ("Coral",      "#DE7C50", (222, 124, 80)),
    ("Ink",        "#3B2F22", (59, 47, 34)),
    ("Ink Soft",   "#7A6A55", (122, 106, 85)),
]

swatch_w, swatch_h = 200, 100
gap, pad = 24, 50
cols = 4
rows = (len(colors) + cols - 1) // cols

width = cols * swatch_w + (cols - 1) * gap + pad * 2
height = rows * (swatch_h + 60) + (rows - 1) * gap + pad * 2 + 20

raw = bytearray()
for y in range(height):
    raw.append(0)
    for x in range(width):
        raw.extend([248, 242, 234, 255])  # warm bg

# Draw swatches
for i, (name, hex_str, rgb) in enumerate(colors):
    col = i % cols
    row_idx = i // cols
    sx = pad + col * (swatch_w + gap)
    sy = pad + row_idx * (swatch_h + 60 + gap)

    for dy in range(swatch_h):
        for dx in range(swatch_w):
            px, py = sx + dx, sy + dy
            idx = py * (width * 4 + 1) + 1 + px * 4
            raw[idx:idx+3] = bytes(rgb)
            raw[idx+3] = 255

def chunk(t, d):
    c = t + d
    h = struct.pack(">I", len(d)) + c + struct.pack(">I", zlib.crc32(c) & 0xffffffff)
    return h

ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
png = b'\x89PNG\r\n\x1a\n'
png += chunk(b'IHDR', ihdr)
png += chunk(b'IDAT', zlib.compress(bytes(raw)))
png += chunk(b'IEND', b'')

path = "/opt/data/home/saturday-mat/images/color-palette.png"
with open(path, "wb") as f:
    f.write(png)
print(f"Created: {path} ({width}x{height}, {len(png)} bytes)")
