"""
Loto Feature Generation System Setup
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="loto-feature-system",
    version="2.0.0",
    author="AI System Architect",
    author_email="",
    description="宝くじ時系列特徴量生成システム",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/loto-feature-system",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "gpu": [
            "cudf-cu11>=24.0.0",
            "cuml-cu11>=24.0.0",
            "cupy-cuda11x>=12.0.0",
            "dask-cuda>=24.0.0",
        ],
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "pylint>=2.17.0",
        ],
    },
)
