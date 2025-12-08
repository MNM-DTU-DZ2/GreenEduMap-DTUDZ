#!/usr/bin/env python3
"""
GreenEduMap License Header Automation
Automatically adds GPL-3.0 license headers to all code files in the GreenEduMap project.

This script processes Python, JavaScript, TypeScript, SQL, Shell, and other files
across the project to ensure proper GPL-3.0 license attribution.
"""

import os
import re
from pathlib import Path
from typing import Dict, Set

# Project Information
PROJECT_NAME = "GreenEduMap-DTUDZ"
PROJECT_DESCRIPTION = "Open Data Platform for Green Urban Development"
COPYRIGHT_YEAR = "2025"
COPYRIGHT_HOLDER = "DTU-DZ2 Team"

# GPL-3.0 License Headers for Different File Types
LICENSE_HEADERS: Dict[str, str] = {
    # Python files
    'py': f'''#!/usr/bin/env python3
"""
{PROJECT_NAME} - {PROJECT_DESCRIPTION}
Copyright (C) {COPYRIGHT_YEAR} {COPYRIGHT_HOLDER}

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

''',
    
    # JavaScript/TypeScript files
    'js': f'''/*
 * {PROJECT_NAME} - {PROJECT_DESCRIPTION}
 * Copyright (C) {COPYRIGHT_YEAR} {COPYRIGHT_HOLDER}
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */

''',
    
    # SQL files
    'sql': f'''--
-- {PROJECT_NAME} - {PROJECT_DESCRIPTION}
-- Copyright (C) {COPYRIGHT_YEAR} {COPYRIGHT_HOLDER}
--
-- This program is free software: you can redistribute it and/or modify
-- it under the terms of the GNU General Public License as published by
-- the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program. If not, see <https://www.gnu.org/licenses/>.
--

''',
    
    # Shell scripts
    'sh': f'''#!/bin/bash
#
# {PROJECT_NAME} - {PROJECT_DESCRIPTION}
# Copyright (C) {COPYRIGHT_YEAR} {COPYRIGHT_HOLDER}
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

''',
    
    # PowerShell scripts
    'ps1': f'''# {PROJECT_NAME} - {PROJECT_DESCRIPTION}
# Copyright (C) {COPYRIGHT_YEAR} {COPYRIGHT_HOLDER}
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

''',
}

# Same header for TypeScript, TSX, JSX, and Vue files as JavaScript
LICENSE_HEADERS['ts'] = LICENSE_HEADERS['js']
LICENSE_HEADERS['tsx'] = LICENSE_HEADERS['js']
LICENSE_HEADERS['jsx'] = LICENSE_HEADERS['js']
LICENSE_HEADERS['vue'] = LICENSE_HEADERS['js']
LICENSE_HEADERS['mjs'] = LICENSE_HEADERS['js']

def has_license_header(content: str) -> bool:
    """
    Check if file already has a license header.
    
    Args:
        content: File content to check
        
    Returns:
        True if license header is present, False otherwise
    """
    # Check for common license indicators
    indicators = [
        f'Copyright (C) {COPYRIGHT_YEAR} {COPYRIGHT_HOLDER}',
        'GNU General Public License',
        PROJECT_NAME,
        'GreenEduMap'
    ]
    
    # Check first 1500 characters for license header
    header_section = content[:1500]
    return any(indicator in header_section for indicator in indicators)


def add_license_header(file_path: Path) -> bool:
    """
    Add license header to file if missing.
    
    Args:
        file_path: Path to the file to process
        
    Returns:
        True if header was added, False if skipped
    """
    ext = file_path.suffix[1:]  # Remove leading dot
    
    if ext not in LICENSE_HEADERS:
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Try with different encoding
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        except Exception as e:
            print(f"⚠️  Cannot read {file_path}: {e}")
            return False
    except Exception as e:
        print(f"⚠️  Error reading {file_path}: {e}")
        return False
    
    # Skip if already has license
    if has_license_header(content):
        return False
    
    # Skip empty files
    if not content.strip():
        return False
    
    # Get appropriate header
    header = LICENSE_HEADERS[ext]
    
    # Language-specific preprocessing
    if ext == 'py':
        # Remove existing shebang if present
        content = re.sub(r'^#!/usr/bin/env python3\s*\n', '', content)
    elif ext == 'sh':
        # Remove existing shebang if present
        content = re.sub(r'^#!/bin/bash\s*\n', '', content)
        content = re.sub(r'^#!/bin/sh\s*\n', '', content)
    
    # Write new content with header
    new_content = header + content
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    except Exception as e:
        print(f"⚠️  Error writing to {file_path}: {e}")
        return False


def should_skip_path(file_path: Path, base_dir: Path) -> bool:
    """
    Check if path should be skipped (dependencies, build folders, etc.).
    
    Args:
        file_path: Path to check
        base_dir: Base directory of the project
        
    Returns:
        True if path should be skipped, False otherwise
    """
    try:
        relative_path = str(file_path.relative_to(base_dir))
    except ValueError:
        return True  # Skip files outside base directory
    
    # Directories to skip
    skip_dirs = [
        'node_modules',
        'dist',
        'build',
        '.git',
        '.next',
        '.nuxt',
        '__pycache__',
        '.pytest_cache',
        '.venv',
        'venv',
        'env',
        '.env',
        'coverage',
        '.nyc_output',
        'tmp',
        'temp',
        '.turbo',
        'out',
        'public',
        'static',
        'assets/images',
        'migrations',
        '.github',
    ]
    
    # Files to skip
    skip_files = [
        'package-lock.json',
        'yarn.lock',
        'pnpm-lock.yaml',
        '.gitignore',
        '.dockerignore',
        'tsconfig.json',
        'next.config.ts',
        'next.config.js',
        'tailwind.config.js',
        'tailwind.config.ts',
        'postcss.config.js',
        'prettier.config.js',
        'eslint.config.mjs',
    ]
    
    # Check if filename should be skipped
    if file_path.name in skip_files:
        return True
    
    # Check if any skip pattern is in the path
    path_str = f'/{relative_path}'
    for skip_dir in skip_dirs:
        if f'/{skip_dir}/' in path_str or relative_path.startswith(skip_dir):
            return True
    
    return False


def main():
    """Main function to process all files in the project."""
    # Get the project root directory (3 levels up from scripts/license/)
    script_dir = Path(__file__).parent
    base_dir = script_dir.parent.parent
    
    print("=" * 80)
    print(f"Adding GPL-3.0 License Headers to {PROJECT_NAME}")
    print("=" * 80)
    print(f"Project: {PROJECT_NAME}")
    print(f"Base directory: {base_dir}")
    print(f"Copyright: {COPYRIGHT_YEAR} {COPYRIGHT_HOLDER}")
    print("=" * 80)
    print()
    
    # File extensions to process
    extensions = ['*.py', '*.js', '*.ts', '*.tsx', '*.jsx', '*.vue', '*.sql', '*.sh', '*.ps1', '*.mjs']
    
    total_files = 0
    updated_files = 0
    skipped_files = 0
    excluded_files = 0
    
    updated_file_list = []
    
    for ext_pattern in extensions:
        files = list(base_dir.rglob(ext_pattern))
        
        for file_path in files:
            total_files += 1
            
            # Skip dependency folders and build artifacts
            if should_skip_path(file_path, base_dir):
                excluded_files += 1
                continue
            
            try:
                if add_license_header(file_path):
                    updated_files += 1
                    relative_path = file_path.relative_to(base_dir)
                    updated_file_list.append(str(relative_path))
                    print(f"✅ Added: {relative_path}")
                else:
                    skipped_files += 1
            except Exception as e:
                print(f"❌ Error processing {file_path}: {e}")
    
    # Print summary
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total files scanned:           {total_files}")
    print(f"✅ Headers added:              {updated_files}")
    print(f"⏭️  Skipped (already licensed): {skipped_files}")
    print(f"🚫 Excluded (deps/build):      {excluded_files}")
    print("=" * 80)
    
    if updated_file_list:
        print()
        print("Updated files:")
        for file in updated_file_list:
            print(f"  - {file}")
    
    print()
    print("✅ License header addition complete!")


if __name__ == "__main__":
    main()
