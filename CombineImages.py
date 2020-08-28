#!/usr/bin/env python3

from PIL import Image
from typing import NamedTuple


class MergeArgs(NamedTuple):
    width: int
    height: int
    padding: int
    spacing: int


def crop_source(source_image):
    size_x, size_y = source_image.size
    start_x = 50
    start_y = 400
    end_x = size_x - start_x
    end_y = size_y - 40
    return source_image.crop((start_x, start_y, end_x, end_y))


def accumulate_size(parts):
    total_w, total_h = 0, 0
    for part in parts:
        total_w = total_w + part.width
        total_h = max(total_h, part.height)
    return total_w, total_h


def estimate_marge_args(parts):
    width, height = accumulate_size(parts)
    padding = int(min(width, height) * 0.1)
    spacing = int(width * 0.1)
    return MergeArgs(width + padding * 2 + spacing * max(0, len(parts) - 1), height + padding * 2, padding, spacing)


def merge_images(parts):
    args = estimate_marge_args(parts)
    dest = Image.new("RGBA", (args.width, args.height))
    dest.paste((255, 255, 255), (0, 0, args.width, args.height))
    x, y = args.padding, args.padding
    for part in parts:
        dest.paste(part, (x, y, part.width + x, part.height + y))
        x = x + part.width + args.spacing
    return dest


if __name__ == "__main__":
    src = ["IMG_9274.PNG", "IMG_9273.PNG", "IMG_9272.PNG"]
    parts = [crop_source(Image.open(x)) for x in src]
    dest = merge_images(parts)
    dest.save("merge_output.png")
    dest.show()
