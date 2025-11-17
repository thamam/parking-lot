"""Setup script for Mouceifi."""
from setuptools import setup, find_packages
import os

# Read README for long description
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='mouceifi',
    version='0.1.0',
    author='Mouceifi Contributors',
    description='Natural Language to Mouse Command Translator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/mouceifi',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: System :: Hardware',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
    ],
    python_requires='>=3.8',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'mouceifi=mouceifi.main:main',
        ],
    },
    keywords='mouse automation natural-language control accessibility',
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/mouceifi/issues',
        'Source': 'https://github.com/yourusername/mouceifi',
    },
)
