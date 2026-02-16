#!/usr/bin/env python3
"""
Test script to verify Mythos installation
Run this to check if everything is working correctly
"""

import sys
import os

def test_python_version():
    """Check Python version"""
    print("Testing Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (Need 3.8+)")
        return False

def test_numpy():
    """Check if numpy is installed"""
    print("\nTesting numpy...")
    try:
        import numpy
        print(f"✓ numpy {numpy.__version__} (OK)")
        return True
    except ImportError:
        print("✗ numpy not found (Run: pip install numpy)")
        return False

def test_mythos_modules():
    """Check if Mythos modules can be imported"""
    print("\nTesting Mythos modules...")
    
    modules = [
        'compiler.lexer.lexer',
        'compiler.parser.parser',
        'compiler.bytecode.compiler',
        'runtime.vm',
    ]
    
    all_ok = True
    for module in modules:
        try:
            __import__(module)
            print(f"✓ {module} (OK)")
        except ImportError as e:
            print(f"✗ {module} (FAILED: {e})")
            all_ok = False
    
    return all_ok

def test_examples_exist():
    """Check if example files exist"""
    print("\nTesting example files...")
    
    examples = [
        'examples/hello_world.mythos',
        'examples/math_demo.mythos',
        'examples/web_app.mythos',
        'examples/game_2d.mythos',
        'examples/game_3d.mythos',
    ]
    
    all_ok = True
    for example in examples:
        if os.path.exists(example):
            print(f"✓ {example} (OK)")
        else:
            print(f"✗ {example} (NOT FOUND)")
            all_ok = False
    
    return all_ok

def test_cli():
    """Test if CLI can be imported"""
    print("\nTesting CLI...")
    try:
        from mythos_cli.cli import MythosCLI
        print("✓ CLI module (OK)")
        return True
    except ImportError as e:
        print(f"✗ CLI module (FAILED: {e})")
        return False

def test_lexer():
    """Test basic lexer functionality"""
    print("\nTesting lexer...")
    try:
        from compiler.lexer.lexer import Lexer
        lexer = Lexer("x = 10")
        tokens = lexer.tokenize()
        if len(tokens) > 0:
            print(f"✓ Lexer works (Generated {len(tokens)} tokens)")
            return True
        else:
            print("✗ Lexer failed (No tokens generated)")
            return False
    except Exception as e:
        print(f"✗ Lexer failed ({e})")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("Mythos Installation Test")
    print("=" * 50)
    
    results = []
    
    results.append(("Python Version", test_python_version()))
    results.append(("NumPy", test_numpy()))
    results.append(("Mythos Modules", test_mythos_modules()))
    results.append(("Example Files", test_examples_exist()))
    results.append(("CLI", test_cli()))
    results.append(("Lexer", test_lexer()))
    
    print("\n" + "=" * 50)
    print("Test Results")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{name:20} {status}")
    
    print("=" * 50)
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Mythos is ready to use!")
        print("\nTry these commands:")
        print("  mythos run examples/hello_world.mythos")
        print("  mythos repl")
        print("  python mythos_cli/cli.py --help")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        print("\nCommon fixes:")
        print("  - Install numpy: pip install numpy")
        print("  - Make sure you're in the Mythos directory")
        print("  - Check that all files are present")
        return 1

if __name__ == '__main__':
    sys.exit(main())
