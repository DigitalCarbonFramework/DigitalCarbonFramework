# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(1, os.path.abspath("../src/carbon"))
for path in sys.path:
    print(path)

# -- Project information -----------------------------------------------------

project = "ad-carbon-calculation-framework"
copyright = "2024, OneframeDigital"
author = "Greenbids.ai"

# The full version, including alpha/beta/rc tags
release = "1.O"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.todo",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "myst_parser",  # Markdown support
]

autodoc_default_options = {
    "exclude-members": "model_computed_fields,model_config,model_fields,model_post_init"
}

# Set to False to exclude return type hints
napoleon_use_rtype = True
napoleon_google_docstring = True
napoleon_numpy_docstring = False

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
