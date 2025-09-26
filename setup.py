"""
Setup script for ZenCrawler package

This script allows the ZenCrawler package to be installed using pip
and provides entry points for command-line usage.
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    """Read README.md file for long description"""
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "A powerful and flexible web crawler for property data extraction"

# Read requirements from requirements.txt
def read_requirements():
    """Read requirements from requirements.txt"""
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return [
        'crawl4ai>=0.7.3',
        'pydantic>=2.11.9',
        'psutil>=7.1.0',
        'requests>=2.25.0',
        'pyproj>=3.0.0',
    ]

setup(
    name="zencrawler",
    version="1.0.0",
    author="ZenCrawler Team",
    author_email="support@zencrawler.com",
    description="A powerful and flexible web crawler for property data extraction",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/zencrawler/zencrawler",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-asyncio>=0.18.0',
            'black>=21.0.0',
            'flake8>=3.9.0',
            'mypy>=0.910',
        ],
        'csv': [
            'pandas>=1.3.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'zencrawler=zencrawler.cli:cli_entry_point',
        ],
    },
    include_package_data=True,
    package_data={
        'zencrawler': [
            'sites/*/config/*.json',
            'sites/*/config/*.yaml',
        ],
    },
    keywords=[
        'web crawler',
        'property data',
        'data extraction',
        'web scraping',
        'real estate',
        'crawl4ai',
        'pydantic',
    ],
    project_urls={
        "Bug Reports": "https://github.com/zencrawler/zencrawler/issues",
        "Source": "https://github.com/zencrawler/zencrawler",
        "Documentation": "https://zencrawler.readthedocs.io/",
    },
)