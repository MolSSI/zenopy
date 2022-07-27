"""
ZenoPy
A Python wrapper package for Zenodo API
"""

# Add imports here
import client
import entities

# Handle versioneer
from ._version import get_versions
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions
