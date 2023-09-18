import pathlib
import sys
from typing import List


# https://wooiljeong.github.io/python/pdf-to-image/
import fitz


def main(argv:List[str], png_folder:pathlib.Path=pathlib.Path('pdf2png')):
    pdf_path = pathlib.Path(argv[1])
    assert pdf_path.exists(), f'"{pdf_path}" does not exist'

    pdf_stem = pdf_path.stem

    png_folder.mkdir(exist_ok=True)

    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc):
        img = page.get_pixdata()
        img.save(png_folder / pdf_stem+f'_{i:04d}.png')
