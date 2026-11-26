"""news-image-20261126 entrypoint.

Writes one image summing up the world news of Thursday 26 November 2026
to /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png locally).

The grader runs standard library only, so Pillow is optional:
  - if Pillow imports, the poster is drawn fresh by render.py
    (deterministic: same code + same bundled fonts => same bytes);
  - otherwise the bundled, pre-rendered entry.png is copied as-is.
Either path writes identical bytes on both grader runs: the poster is
drawn from fixed text and bundled fonts with no clock, randomness or
network input, and the fallback copies the bundled file byte for byte.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BUNDLED_PNG = os.path.join(HERE, "entry.png")


def output_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, "entry.png")


def main():
    dest = output_path()
    try:
        from PIL import Image  # noqa: F401  (guarded: grader is stdlib-only)
    except ImportError:
        shutil.copyfile(BUNDLED_PNG, dest)
        return 0

    try:
        sys.path.insert(0, HERE)
        import render

        img = render.build_poster()
        img.save(dest, format="PNG")
    except Exception:
        # Any rendering surprise (missing font, odd Pillow build):
        # fall back to the bundled image, byte for byte.
        shutil.copyfile(BUNDLED_PNG, dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
