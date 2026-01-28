import os
import sys
from typing import List

sys.path.insert(0, os.path.abspath(".."))

project = "Steadfast Courier Python SDK"
copyright = "2026, Md Mojno Miya"
author = "Md Mojno Miya"
release = "0.3.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "myst_parser",
    "sphinx_rtd_theme",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_static_path: List[str] = []

autodoc_member_order = "bysource"
autodoc_typehints = "description"

source_suffix = {
    ".rst": None,
    ".md": "markdown",
}
