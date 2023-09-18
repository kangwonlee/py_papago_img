'''
Split a PDF file into PNG files.

References:
  https://wooiljeong.github.io/python/pdf-to-image/
  https://pymupdf.readthedocs.io/en/latest/the-basics.html#extract-images-from-a-pdf
'''

import os
import pathlib
import sys
from typing import List


import fitz


def main(argv:List[str], png_folder:pathlib.Path=pathlib.Path('pdf2png')):
    pdf_path = pathlib.Path(os.getenv('PDF_PATH', argv[1]))
    assert pdf_path.exists(), f'"{pdf_path}" does not exist'

    pdf_stem = pdf_path.stem

    png_folder.mkdir(exist_ok=True)

    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc):
        img = page.get_pixdata()
        img.save(png_folder / pdf_stem+f'_{i:04d}.png')


if __name__ == '__main__':
    main(sys.argv)
