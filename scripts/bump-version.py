#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Version bump utility for ChifferSkiftaren.

Usage:
    python3 scripts/bump-version.py patch      # 0.1.0 → 0.1.1
    python3 scripts/bump-version.py minor      # 0.1.0 → 0.2.0
    python3 scripts/bump-version.py major      # 0.1.0 → 1.0.0
    python3 scripts/bump-version.py 0.2.0      # Set to specific version
"""

import sys
import os
import re
from pathlib import Path


def parse_version(version_str):
    """Parse semantic version string into (major, minor, patch) tuple."""
    match = re.match(r'^(\d+)\.(\d+)\.(\d+)$', version_str.strip())
    if not match:
        raise ValueError(f"Invalid version format: {version_str}. Expected X.Y.Z")
    return tuple(int(x) for x in match.groups())


def version_to_string(major, minor, patch):
    """Convert version tuple to string."""
    return f"{major}.{minor}.{patch}"


def bump_version(current_version, bump_type):
    """Bump version according to type (major|minor|patch)."""
    major, minor, patch = parse_version(current_version)
    
    if bump_type == 'major':
        return version_to_string(major + 1, 0, 0)
    elif bump_type == 'minor':
        return version_to_string(major, minor + 1, 0)
    elif bump_type == 'patch':
        return version_to_string(major, minor, patch + 1)
    else:
        raise ValueError(f"Unknown bump type: {bump_type}")


def update_version_file(new_version):
    """Update VERSION file."""
    version_file = Path(__file__).parent.parent / 'VERSION'
    version_file.write_text(f"{new_version}\n", encoding='utf-8')
    print(f"✓ Updated VERSION: {new_version}")


def update_readme(new_version):
    """Update version badge in README."""
    readme_file = Path(__file__).parent.parent / 'README.md'
    content = readme_file.read_text(encoding='utf-8')
    
    # Replace version badge if it exists, or add it after title
    if '<!-- version:' in content:
        # Update existing marker
        content = re.sub(
            r'<!-- version: .*? -->\nVersion: .*?\n',
            f'<!-- version: {new_version} -->\nVersion: **{new_version}**\n',
            content
        )
    else:
        # Add version badge after main title and description
        lines = content.split('\n')
        insert_idx = 2  # After title and first description line
        lines.insert(insert_idx, f'<!-- version: {new_version} -->')
        lines.insert(insert_idx + 1, f'Version: **{new_version}**\n')
        content = '\n'.join(lines)
    
    readme_file.write_text(content, encoding='utf-8')
    print(f"✓ Updated README")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    arg = sys.argv[1]
    
    version_file = Path(__file__).parent.parent / 'VERSION'
    if not version_file.exists():
        print("ERROR: VERSION file not found!")
        sys.exit(1)
    
    current_version = version_file.read_text(encoding='utf-8').strip()
    print(f"Current version: {current_version}")
    
    # Determine new version
    if arg in ['major', 'minor', 'patch']:
        new_version = bump_version(current_version, arg)
    else:
        # Treat as explicit version
        try:
            parse_version(arg)  # Validate format
            new_version = arg
        except ValueError as e:
            print(f"ERROR: {e}")
            sys.exit(1)
    
    print(f"New version: {new_version}")
    
    # Update files
    update_version_file(new_version)
    update_readme(new_version)
    
    print(f"\n✓ Version bumped to {new_version}")
    print("Next steps:")
    print(f"  git add VERSION README.md")
    print(f"  git commit -m 'chore: bump version to {new_version}'")
    print(f"  git tag v{new_version}")


if __name__ == '__main__':
    main()
