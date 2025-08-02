from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="financial-analysis-crewai",
    version="1.0.0",
    author="Financial Analysis Team",
    author_email="your.email@example.com",
    description="A comprehensive financial analysis system using CrewAI framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/financial-analysis-crewai",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "financial-analysis=financial_analysis_crew:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.csv", "*.md"],
    },
    keywords="financial analysis, crewai, ai agents, data visualization, forecasting",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/financial-analysis-crewai/issues",
        "Source": "https://github.com/yourusername/financial-analysis-crewai",
        "Documentation": "https://github.com/yourusername/financial-analysis-crewai#readme",
    },
) 