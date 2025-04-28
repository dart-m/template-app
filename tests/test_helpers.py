from app.utils.helpers import *

from pathlib import Path

import docx

filepath_docx = Path("tests/files/test.docx")
filepath_md   = Path("tests/files/test.md")


def test_converter_docx():
    converter(filepath_docx, filepath_md, to="md")
    with open(filepath_md, "r", encoding="UTF-8") as f:
        md_file = f.read()
    assert len(md_file) > 500


def test_converter_md():
    converter(filepath_md, filepath_docx, to="docx")
    doc = docx.Document(filepath_docx)
    assert len(doc.paragraphs) == 67


def test_get_chunks():
    max_length = 2300
    with open(filepath_md, "r", encoding="UTF-8") as f:
        md_file = f.read()
    assert len(get_chunks(md_file, max_length)) == 5
