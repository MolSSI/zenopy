"""
Unit and regression test for the zenopy package.
"""

# Import package, test suite, and other packages as needed
import zenopy
import pytest
import sys

def test_zenopy_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "zenopy" in sys.modules
