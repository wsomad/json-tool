from setuptools import setup, find_packages

setup(
    name="json-tool", # Project name
    version="0.1", # Project version
    packages=find_packages(where="src"),  # Ensure the package is found in "src"
    package_dir={"": "src"},  # Set "src" as the package root
    entry_points={
        "console_scripts": [
            "json-tool=cli:main",  # Make sure this points to your CLI entry
        ],
    },
    install_requires=[],
)   