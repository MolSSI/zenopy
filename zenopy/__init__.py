# -*- coding: utf-8 -*-

"""
zenopy
A Python wrapper package for Zenodo API
"""

import textwrap

# Bring up the classes so that they appear to be directly in
# the zenopy package.

from zenopy.client import Zenodo    # noqa: E402
from zenopy import metadata # noqa: E402

wrap_text = textwrap.TextWrapper(width=120)
wrap_stdout = textwrap.TextWrapper(width=120)

# Handle versioneer
from ._version import get_versions  # noqa: E402

__author__ = """Mohammad Mostafanejad"""
__email__ = "smostafanejad@vt.edu"
versions = get_versions()
__version__ = versions["version"]
__git_revision__ = versions["full-revisionid"]
del get_versions, versions
