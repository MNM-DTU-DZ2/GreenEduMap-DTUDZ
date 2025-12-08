#
# GreenEduMap-DTUDZ - Open Data Platform for Green Urban Development
# Copyright (C) 2025 DTU-DZ2 Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#

"""
Setup script for shared GreenEduMap modules
"""

from setuptools import find_packages, setup

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
