# Configuration file for the Sphinx documentation builder.

import os
import sys
from pathlib import Path

# Ścieżka do katalogu źródłowego projektu
sys.path.insert(0, os.path.abspath('C:/Users/kubap/Desktop/TU_ROBIE_PYTHON/Zwierzatko_PythonProject/src'))

# -- Project information -----------------------------------------------------
project = 'Zwierzatko_PythonProject'
copyright = '2025, Jakub Pawlik s30647'
author = 'Jakub Pawlik s30647'
release = '1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = []
language = 'pl'

# -- Options for HTML output -------------------------------------------------
html_theme = 'furo'

# Jeśli chcesz używać własnych statycznych plików (np. niestandardowe CSS/obrazy)
html_static_path = ['_static']

# Przykład: jeśli chcesz dodać własny CSS, odkomentuj poniższe:
# html_css_files = [
#     'custom.css',
# ]
