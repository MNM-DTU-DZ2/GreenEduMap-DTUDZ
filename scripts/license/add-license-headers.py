#!/usr/bin/env python3
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


import os
import re
from pathlib import Path

# License headers for different file types
HEADERS = {
    'python': '''#
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

''',
    'typescript': '''/**
 * GreenEduMap-DTUDZ - Open Data Platform for Green Urban Development
 * Copyright (C) 2025 DTU-DZ2 Team
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
    'shell': '''#!/bin/bash
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

''',
    'sql': '''--
-- GreenEduMap-DTUDZ - Open Data Platform for Green Urban Development
-- Copyright (C) 2025 DTU-DZ2 Team
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

'''
}

# File extensions mapping
EXTENSIONS = {
    '.py': 'python',
    '.ts': 'typescript',
    '.tsx': 'typescript',
    '.js': 'typescript',
    '.jsx': 'typescript',
    '.sh': 'shell',
    '.bash': 'shell',
    '.sql': 'sql',
}

# Directories to skip
SKIP_DIRS = {
    'node_modules', '.git', '__pycache__', 'dist', 'build', 
    '.next', 'venv', 'env', '.venv', 'coverage', '.pytest_cache',
    'migrations', 'alembic'
}

# Files to skip
SKIP_FILES = {
    'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
    '.env', '.env.local', '.env.production',
}

def has_license_header(content):
    """Check if file already has GPL license header"""
    patterns = [
        r'GNU General Public License',
        r'GreenEduMap-DTUDZ',
        r'DTU-DZ2 Team',
        r'Copyright \(C\) 2025'
    ]
    return any(re.search(pattern, content[:1000]) for pattern in patterns)

def add_license_header(filepath):
    """Add license header to file if not present"""
    ext = filepath.suffix.lower()
    if ext not in EXTENSIONS:
        return False
    
    header_type = EXTENSIONS[ext]
    header = HEADERS[header_type]
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if has_license_header(content):
            return False  # Already has header
        
        # Handle shebang for shell/python scripts
        if content.startswith('#!'):
            lines = content.split('\n', 1)
            if len(lines) > 1:
                new_content = lines[0] + '\n' + header + lines[1]
            else:
                new_content = lines[0] + '\n' + header
        else:
            new_content = header + content
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True  # Header added
    
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def scan_directory(root_dir):
    """Scan directory and add headers to files"""
    root_path = Path(root_dir)
    added_count = 0
    skipped_count = 0
    already_has_count = 0
    
    for filepath in root_path.rglob('*'):
        # Skip directories
        if filepath.is_dir():
            continue
        
        # Skip if in excluded directory
        if any(skip_dir in filepath.parts for skip_dir in SKIP_DIRS):
            continue
        
        # Skip if excluded file
        if filepath.name in SKIP_FILES:
            continue
        
        # Skip if not a code file
        if filepath.suffix.lower() not in EXTENSIONS:
            continue
        
        # Try to add header
        result = add_license_header(filepath)
        if result:
            print(f"✅ Added header: {filepath}")
            added_count += 1
        elif result is False:
            already_has_count += 1
        else:
            skipped_count += 1
    
    return added_count, already_has_count, skipped_count

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        root_dir = sys.argv[1]
    else:
        root_dir = '.'
    
    print(f"🔍 Scanning {root_dir} for files without license headers...")
    print()
    
    added, already_has, skipped = scan_directory(root_dir)
    
    print()
    print("=" * 60)
    print(f"✅ Headers added: {added}")
    print(f"ℹ️  Already has header: {already_has}")
    print(f"⏭️  Skipped: {skipped}")
    print("=" * 60)
