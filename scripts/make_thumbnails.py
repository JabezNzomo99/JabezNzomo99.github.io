#!/usr/bin/env python3
"""Normalise Figma exports into site thumbnails.

Figma cannot export WebP, so export frames as PNG (ideally square, >=600px)
and run them through here to get the 800x800 WebP the site expects.

    python3 scripts/make_thumbnails.py ~/Downloads/*.png
    python3 scripts/make_thumbnails.py --fit ~/Downloads/include2.png

Output lands in assets/thumbnails/ using the source filename, lowercased with
spaces and underscores turned into hyphens, so "INCLUDE 2.png" -> include-2.webp
"""
import argparse
import pathlib
import re
import sys

from PIL import Image, ImageOps

SIZE = 800
OUT_DIR = pathlib.Path(__file__).resolve().parent.parent / "assets" / "thumbnails"


def slugify(stem):
    return re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sources", nargs="+", type=pathlib.Path)
    ap.add_argument("--fit", action="store_true",
                    help="centre-crop to square instead of padding on white; "
                         "loses the edges but fills the frame")
    ap.add_argument("--pad-colour", default="white",
                    help="background for padding (default: white)")
    ap.add_argument("--quality", type=int, default=82)
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    failed = False

    for src in args.sources:
        if not src.is_file():
            print(f"!! {src}: not a file", file=sys.stderr)
            failed = True
            continue

        im = Image.open(src)
        # Flatten transparency onto the pad colour so WebP has no alpha fringe.
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            bg = Image.new("RGBA", im.size, args.pad_colour)
            im = Image.alpha_composite(bg, im)
        im = im.convert("RGB")

        if args.fit:
            im = ImageOps.fit(im, (SIZE, SIZE), method=Image.LANCZOS)
        else:
            im = ImageOps.pad(im, (SIZE, SIZE), method=Image.LANCZOS,
                              color=args.pad_colour)

        out = OUT_DIR / f"{slugify(src.stem)}.webp"
        im.save(out, quality=args.quality, method=6)
        kb = out.stat().st_size // 1024
        flag = "  <-- over 300KB, lower --quality" if kb > 300 else ""
        print(f"{src.name} -> assets/thumbnails/{out.name}  {kb}KB{flag}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
