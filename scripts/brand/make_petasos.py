#!/usr/bin/env python3
"""Draws the Petasos pixel-art mark and renders every app icon from it.

Needs rsvg-convert and ImageMagick (magick) on PATH.
Run: python3 scripts/brand/make_petasos.py
"""
import struct
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

SIZE = 32

PALETTE = {
    "o": "#0d0f17",
    "b": "#0055a4",
    "s": "#003f7a",
    "h": "#2f7fd0",
    "g": "#f5c518",
    "w": "#f2f4fa",
    "f": "#aeb8cc",
}

GRID = [
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    ".....o....................o.....",
    "....owo..o............o..owo....",
    "....owwoowo..........owoowwo....",
    ".....owwfwwo..oooo..owwfwwo.....",
    ".....ofwwfwwoohhhhoowwfwwfo.....",
    "......ofwwfobbhhhhbbofwwfo......",
    ".......ofwwobbbbbbbbowwfo.......",
    "........ofobbbbbbbbbbofo........",
    ".........obbbbbbbbbbbbo.........",
    ".........obbbbbbbbbbbbo.........",
    ".........oggggggggggggo.........",
    "......ooobggggggggggggbooo......",
    "....oobbbbbbbbbbbbbbbbbbbboo....",
    "...obbbbbbbbbbbbbbbbbbbbbbbbo...",
    "..obbbbbbbbbbbbbbbbbbbbbbbbbbo..",
    "...oobbssssssssssssssssssbboo...",
    ".....ooossssssssssssssssooo.....",
    "........oooooooooooooooo........",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
]


def validate_grid():
    if len(GRID) != SIZE or any(len(row) != SIZE for row in GRID):
        raise ValueError("The pixel grid must be 32 by 32.")
    if len(set(PALETTE.values())) > 7:
        raise ValueError("The mark must use at most seven colours.")
    if any(pixel not in PALETTE and pixel != "." for row in GRID for pixel in row):
        raise ValueError("Every opaque pixel must have a palette entry.")
    if any(row != row[::-1] for row in GRID):
        raise ValueError("The mark must be symmetric from left to right.")
    if any(pixel != "." for pixel in GRID[0] + GRID[-1]):
        raise ValueError("The top and bottom edges must stay transparent.")
    if any(row[0] != "." or row[-1] != "." for row in GRID):
        raise ValueError("The left and right edges must stay transparent.")
    for y, row in enumerate(GRID):
        for x, pixel in enumerate(row):
            if pixel in (".", "o"):
                continue
            neighbours = (GRID[y - 1][x], GRID[y + 1][x],
                          row[x - 1], row[x + 1])
            if "." in neighbours:
                raise ValueError(f"Missing outline beside pixel ({x}, {y}).")


def render_runs():
    rectangles = []
    for y, row in enumerate(GRID):
        x = 0
        while x < SIZE:
            pixel = row[x]
            start = x
            while x < SIZE and row[x] == pixel:
                x += 1
            if pixel == ".":
                continue
            colour = PALETTE[pixel]
            rectangles.append(
                f'    <rect x="{start}" y="{y}" width="{x - start}" '
                f'height="1" fill="{colour}"/>'
            )
    return "\n".join(rectangles)


def make_svg(rectangles, tile=False):
    title = "Petasos app icon" if tile else "Petasos"
    elements = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" '
        'viewBox="0 0 32 32" shape-rendering="crispEdges" '
        'role="img" aria-labelledby="title">',
        f'  <title id="title">{title}</title>',
    ]
    if tile:
        # A 0.75 scale keeps art pixels on whole device pixels at 512 and 1024.
        elements.extend([
            f'  <rect width="32" height="32" rx="7" fill="{PALETTE["o"]}"/>',
            '  <g transform="translate(4 4) scale(0.75)">',
            rectangles,
            "  </g>",
        ])
    else:
        elements.append(rectangles)
    elements.append("</svg>")
    return "\n".join(elements) + "\n"


def rasterize(svg, size, out):
    subprocess.run(
        ["rsvg-convert", "-w", str(size), "-h", str(size), str(svg), "-o", str(out)],
        check=True,
    )


def write_icns(pngs, out):
    chunks = b"".join(
        kind + struct.pack(">I", len(data) + 8) + data for kind, data in pngs
    )
    out.write_bytes(b"icns" + struct.pack(">I", len(chunks) + 8) + chunks)


def main():
    validate_grid()
    rectangles = render_runs()
    mark = ROOT / "src/renderer/src/assets/petasos.svg"
    tile = ROOT / "build/icon.svg"
    mark.write_text(make_svg(rectangles))
    tile.write_text(make_svg(rectangles, tile=True))

    build = ROOT / "build"
    rasterize(tile, 1024, build / "icon.png")
    rasterize(tile, 512, ROOT / "resources/icon.png")

    tmp = build / ".icon-sizes"
    tmp.mkdir(exist_ok=True)
    sizes = {}
    for size in (16, 24, 32, 48, 64, 128, 256, 512, 1024):
        sizes[size] = tmp / f"{size}.png"
        rasterize(tile, size, sizes[size])
    subprocess.run(
        ["magick", *[str(sizes[s]) for s in (16, 24, 32, 48, 64, 128, 256)],
         str(build / "icon.ico")],
        check=True,
    )
    icns_types = [(b"icp4", 16), (b"icp5", 32), (b"icp6", 64), (b"ic07", 128),
                  (b"ic08", 256), (b"ic09", 512), (b"ic10", 1024)]
    write_icns([(kind, sizes[s].read_bytes()) for kind, s in icns_types],
               build / "icon.icns")
    for path in sizes.values():
        path.unlink()
    tmp.rmdir()
    print("Wrote", mark.relative_to(ROOT), "and the icons in build/ and resources/")


if __name__ == "__main__":
    main()
