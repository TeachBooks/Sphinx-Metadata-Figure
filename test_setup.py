#!/usr/bin/env python3
"""
Test Script for Custom Figure Extension
========================================

This script verifies that the custom figure extension is properly set up
and can be imported correctly.
"""

import sys
from pathlib import Path

def test_extension_import():
    """Test if the custom_figure extension can be imported."""
    print("Testing custom_figure extension import...")
    
    # Add _ext to path
    ext_path = Path(__file__).parent / '_ext'
    sys.path.insert(0, str(ext_path))
    
    try:
        import custom_figure
        print("✓ custom_figure module imported successfully")
        
        # Check if required components exist
        assert hasattr(custom_figure, 'CustomFigure'), "CustomFigure class not found"
        print("✓ CustomFigure class found")
        
        assert hasattr(custom_figure, 'setup'), "setup() function not found"
        print("✓ setup() function found")
        
        assert hasattr(custom_figure, 'VALID_LICENSES'), "VALID_LICENSES not found"
        print("✓ VALID_LICENSES list found")
        print(f"  Valid licenses: {len(custom_figure.VALID_LICENSES)} types")
        
        return True
        
    except ImportError as e:
        print(f"✗ Failed to import custom_figure: {e}")
        return False
    except AssertionError as e:
        print(f"✗ Assertion failed: {e}")
        return False


def test_required_packages():
    """Test if required packages are installed."""
    print("\nTesting required packages...")
    
    packages = [
        ('sphinx', 'Sphinx'),
        ('myst_parser', 'MyST Parser'),
        ('docutils', 'Docutils'),
    ]
    
    all_installed = True
    for module_name, display_name in packages:
        try:
            __import__(module_name)
            print(f"✓ {display_name} is installed")
        except ImportError:
            print(f"✗ {display_name} is NOT installed")
            all_installed = False
    
    return all_installed


def test_file_structure():
    """Test if all required files exist."""
    print("\nTesting file structure...")
    
    base_path = Path(__file__).parent
    required_files = [
        '_ext/custom_figure.py',
        '_static/custom_figure.css',
        'conf.py',
        'index.md',
        'requirements.txt',
        'README.md',
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = base_path / file_path
        if full_path.exists():
            print(f"✓ {file_path} exists")
        else:
            print(f"✗ {file_path} is missing")
            all_exist = False
    
    return all_exist


def main():
    """Run all tests."""
    print("=" * 60)
    print("Custom Figure Extension - Setup Verification")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("File Structure", test_file_structure()))
    results.append(("Required Packages", test_required_packages()))
    results.append(("Extension Import", test_extension_import()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "PASSED ✓" if passed else "FAILED ✗"
        print(f"{test_name:.<40} {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✓ All tests passed! The extension is ready to use.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Build documentation: make html")
        print("3. View output: open _build/html/index.html")
        return 0
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
        print("\nTo fix missing packages, run:")
        print("  pip install -r requirements.txt")
        return 1


if __name__ == '__main__':
    sys.exit(main())
