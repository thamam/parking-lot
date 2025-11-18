"""
Setup configuration for AI Duo Validator.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / 'README.md'
long_description = ''
if readme_file.exists():
    with open(readme_file, 'r', encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='ai-duo-validator',
    version='1.0.0',
    description='Orchestrator for AI-to-AI validation coordination between two Claude Code agents',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='AI Duo Validator Team',
    author_email='',
    url='https://github.com/yourusername/ai-duo-validator',
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    install_requires=[
        'click>=8.1.0,<9.0.0',
        'colorama>=0.4.6,<1.0.0',
        'python-dateutil>=2.8.2,<3.0.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.4.0,<8.0.0',
            'pytest-cov>=4.1.0,<5.0.0',
            'black>=23.0.0,<24.0.0',
            'flake8>=6.0.0,<7.0.0',
            'mypy>=1.5.0,<2.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'orchestrator=src.cli:cli',
        ],
    },
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords='ai orchestration validation code-review agent-coordination',
    project_urls={
        'Documentation': 'https://github.com/yourusername/ai-duo-validator#readme',
        'Source': 'https://github.com/yourusername/ai-duo-validator',
        'Tracker': 'https://github.com/yourusername/ai-duo-validator/issues',
    },
)
