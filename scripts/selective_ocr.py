"""Render one flagged physical PDF page, then invoke local Tesseract."""
from pathlib import Path
import shutil
import subprocess
import tempfile

def ocr_page(pdf, page_number, dpi=300):
    executable = shutil.which('tesseract')
    if executable is None:
        raise RuntimeError('OCR requested but Tesseract is not installed/on PATH')
    import pypdfium2 as pdfium
    document = pdfium.PdfDocument(str(pdf))
    try:
        if not 1 <= page_number <= len(document):
            raise ValueError('physical page out of range')
        page = document[page_number - 1]
        try:
            bitmap = page.render(scale=dpi / 72)
            try:
                with tempfile.TemporaryDirectory(prefix='research-ocr-') as folder:
                    image = Path(folder) / 'page.png'
                    bitmap.to_pil().save(image)
                    result = subprocess.run(
                        [executable, str(image), 'stdout', '-l', 'eng'],
                        check=True, capture_output=True, text=True, encoding='utf-8',
                        timeout=120,
                    )
                    return result.stdout
            finally:
                bitmap.close()
        finally:
            page.close()
    finally:
        document.close()
