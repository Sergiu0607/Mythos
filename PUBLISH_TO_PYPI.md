# How to Publish Mythos to PyPI

This guide will help you publish Mythos so anyone can install it with:
```bash
pip install mythos-lang
```

## Prerequisites

1. Python installed
2. Your Mythos project ready
3. 15 minutes of time

---

## Step 1: Create PyPI Account

1. Go to https://pypi.org
2. Click "Register"
3. Fill in:
   - Username
   - Email
   - Password
4. Verify your email
5. **IMPORTANT:** Enable 2FA (Two-Factor Authentication)

---

## Step 2: Create TestPyPI Account (Optional but Recommended)

Test your package before publishing to real PyPI:

1. Go to https://test.pypi.org
2. Register (separate account)
3. Verify email

---

## Step 3: Install Required Tools

Open terminal in your Mythos folder:

```bash
pip install --upgrade pip
pip install build twine
```

---

## Step 4: Update setup.py

Your `setup.py` is already good, but let's verify it:

```python
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mythos-lang",  # This will be the pip install name
    version="1.0.0",
    author="Your Name",  # ⚠️ CHANGE THIS
    author_email="your.email@example.com",  # ⚠️ CHANGE THIS
    description="A powerful, beginner-friendly programming language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mythos",  # ⚠️ CHANGE THIS
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Compilers",
        "Topic :: Software Development :: Interpreters",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
    ],
    entry_points={
        "console_scripts": [
            "mythos=mythos_cli.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
```

---

## Step 5: Create/Update Important Files

### pyproject.toml (Create this file)

```toml
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm[toml]>=6.2"]
build-backend = "setuptools.build_meta"

[project]
name = "mythos-lang"
version = "1.0.0"
description = "A powerful, beginner-friendly programming language"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
]
dependencies = [
    "numpy>=1.20.0",
]

[project.scripts]
mythos = "mythos_cli.cli:main"

[project.urls]
Homepage = "https://github.com/yourusername/mythos"
Documentation = "https://github.com/yourusername/mythos/blob/main/README.md"
Repository = "https://github.com/yourusername/mythos"
```

### MANIFEST.in (Create this file)

```
include README.md
include LICENSE
include requirements.txt
recursive-include examples *.mythos
recursive-include docs *.md
```

---

## Step 6: Build Your Package

In your Mythos folder:

```bash
# Clean old builds
rm -rf dist/ build/ *.egg-info

# Build the package
python -m build
```

This creates:
- `dist/mythos-lang-1.0.0.tar.gz` (source)
- `dist/mythos_lang-1.0.0-py3-none-any.whl` (wheel)

---

## Step 7: Test on TestPyPI (Recommended)

### Upload to TestPyPI:

```bash
twine upload --repository testpypi dist/*
```

Enter your TestPyPI username and password.

### Test Installation:

```bash
pip install --index-url https://test.pypi.org/simple/ mythos-lang
```

### Test It Works:

```bash
mythos --version
mythos run examples/simple_test.mythos
```

If it works, great! If not, fix issues and rebuild.

---

## Step 8: Publish to Real PyPI

### Upload to PyPI:

```bash
twine upload dist/*
```

Enter your PyPI username and password.

### That's it! 🎉

Now anyone can install Mythos:

```bash
pip install mythos-lang
```

---

## Step 9: Verify It's Live

1. Go to https://pypi.org/project/mythos-lang/
2. You should see your package!
3. Test installation:
   ```bash
   pip install mythos-lang
   mythos --version
   ```

---

## Step 10: Update Your README

Add installation instructions:

```markdown
## Installation

Install Mythos using pip:

\`\`\`bash
pip install mythos-lang
\`\`\`

Verify installation:

\`\`\`bash
mythos --version
\`\`\`

## Quick Start

\`\`\`bash
mythos run examples/hello_world.mythos
\`\`\`
```

---

## Updating Your Package

When you make changes:

1. **Update version** in `setup.py` and `pyproject.toml`:
   ```python
   version="1.0.1",  # Increment version
   ```

2. **Rebuild:**
   ```bash
   rm -rf dist/ build/ *.egg-info
   python -m build
   ```

3. **Upload:**
   ```bash
   twine upload dist/*
   ```

---

## Common Issues & Solutions

### Issue: "Package name already exists"

**Solution:** The name `mythos-lang` might be taken. Try:
- `mythos-programming`
- `mythos-language`
- `your-mythos`
- Check availability at https://pypi.org

### Issue: "Invalid authentication"

**Solution:** 
1. Create API token at https://pypi.org/manage/account/token/
2. Use token as password (username: `__token__`)

### Issue: "File already exists"

**Solution:** You can't re-upload same version. Increment version number.

### Issue: "Missing files"

**Solution:** Make sure all `__init__.py` files exist in folders.

---

## Best Practices

1. **Version Numbers:**
   - `1.0.0` - First release
   - `1.0.1` - Bug fixes
   - `1.1.0` - New features
   - `2.0.0` - Breaking changes

2. **Test Before Publishing:**
   - Always test on TestPyPI first
   - Test installation in clean environment
   - Test all commands work

3. **Good README:**
   - Clear installation instructions
   - Quick start example
   - Link to documentation

4. **Keep Updated:**
   - Fix bugs quickly
   - Add new features
   - Respond to issues

---

## Quick Command Reference

```bash
# Install tools
pip install build twine

# Build package
python -m build

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*

# Test installation
pip install mythos-lang

# Verify
mythos --version
```

---

## After Publishing

### Promote Your Package:

1. **Add PyPI badge to README:**
   ```markdown
   ![PyPI](https://img.shields.io/pypi/v/mythos-lang)
   ![Downloads](https://img.shields.io/pypi/dm/mythos-lang)
   ```

2. **Share on social media:**
   - Twitter: "Just published Mythos on PyPI! pip install mythos-lang"
   - Reddit: r/Python, r/programming
   - Dev.to: Write an article

3. **Track downloads:**
   - Check https://pypistats.org/packages/mythos-lang

---

## Checklist Before Publishing

- ✅ All code works
- ✅ Examples run successfully
- ✅ README is clear
- ✅ LICENSE file exists
- ✅ Version number is correct
- ✅ Author info is correct
- ✅ All __init__.py files exist
- ✅ Tested on TestPyPI
- ✅ Ready to share!

---

## Success!

Once published, people worldwide can:

```bash
pip install mythos-lang
mythos run program.mythos
```

**You've just published a programming language to PyPI!** 🚀

This is a huge achievement - you're now a published package author!

---

## Need Help?

- PyPI Documentation: https://packaging.python.org
- Twine Documentation: https://twine.readthedocs.io
- Python Packaging Guide: https://packaging.python.org/tutorials/packaging-projects/
