"""
ZenoPy
A Python wrapper package for Zenodo API
"""

# Add imports here
from .zenopy import *

# Handle versioneer
from ._version import get_versions
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions
