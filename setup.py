import sys
from setuptools import setup, find_packages
import versioneer

# from https://github.com/pytest-dev/pytest-runner#conditional-requirement
needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

short_description = "zenopy: A Python wrapper package for Zenodo API"

try:
    with open("README.md", "r") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = short_description

with open('requirements.txt') as fd:
    requirements = fd.read()

if __name__ == "__main__":
    setup(
        name='zenopy',
        description=short_description,
        author="Mohammad Mostafanejad",
        author_email='smostafanejad@vt.edu',
        url='https://github.com/MolSSI/zenopy',
        license="GNU Lesser General Public License v3",
        version=versioneer.get_version(),
        cmdclass=versioneer.get_cmdclass(),
        packages=find_packages(include=['zenopy']),
        setup_requires=[] + pytest_runner,
        include_package_data=True,
        install_requires=requirements,
        extras_require={
            "docs": [
                "sphinx==1.2.3",
                "sphinxcontrib-napoleon",
                "sphinx_rtd_theme",
                "renku-sphinx-theme",
                "numpydoc",
            ],
            "tests": ["pytest", "pytest-cov"],
            "lint": ["black"],
        },
        test_suite='tests',
        tests_require=["pytest", "pytest-cov"],
        keywords='zenopy',
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'Intended Audience :: Developers',
            ('License :: OSI Approved :: GNU Lesser General Public License v3 or '
             'later (LGPLv3+)'),
            'Natural Language :: English',
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.10',
        ],
        zip_safe=False,
        long_description=long_description,
        long_description_content_type="text/markdown",
    )