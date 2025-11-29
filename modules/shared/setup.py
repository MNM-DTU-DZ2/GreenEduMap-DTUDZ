"""
Setup script for shared GreenEduMap modules
"""

from setuptools import setup, find_packages

setup(
    name="greenedumap-shared",
    version="1.0.0",
    description="Shared database models and utilities for GreenEduMap",
    author="GreenEduMap Team",
    packages=find_packages(),
    install_requires=[
        "sqlalchemy>=2.0.25",
        "asyncpg>=0.29.0",
        "geoalchemy2>=0.14.3",
        "psycopg2-binary>=2.9.9",
        "pydantic>=2.5.0",
        "python-dotenv>=1.0.0",
    ],
    python_requires=">=3.11",
)
