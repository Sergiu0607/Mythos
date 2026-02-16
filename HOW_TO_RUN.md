# How to Run Mythos - Simple Guide

## TL;DR (Too Long; Didn't Read)

```bash
# 1. Go to Mythos folder
cd path/to/Mythos

# 2. Install
pip install -e .

# 3. Run
mythos run examples/hello_world.mythos
```

## Why Brew/Choco Don't Work

❌ `brew install mythos` - Won't work (not published yet)
❌ `choco install mythos` - Won't work (not published yet)
❌ `pip install mythos-lang` - Won't work (not published yet)

✅ Mythos is a **local project** - install it from the folder!

## Three Ways to Run Mythos

### Way 1: Install It (Recommended)

```bash
# Navigate to Mythos folder
cd path/to/Mythos

# Install
pip install -e .

# Now you can use 'mythos' command anywhere
mythos run examples/hello_world.mythos
mythos repl
```

### Way 2: Use the Installer Scripts

**Windows:**
```bash
cd path\to\Mythos
install.bat
```

**Mac/Linux:**
```bash
cd path/to/Mythos
chmod +x install.sh
./install.sh
```

### Way 3: Run Directly (No Install)

```bash
cd path/to/Mythos
python mythos_cli/cli.py run examples/hello_world.mythos
```

## Test Your Installation

```bash
# Run the test script
python test_installation.py
```

This will check if everything is working!

## Common Problems

### Problem: "mythos: command not found"

**Solution 1:** Use Python directly
```bash
python mythos_cli/cli.py run file.mythos
```

**Solution 2:** Add Python Scripts to PATH (see INSTALLATION_GUIDE.md)

### Problem: "No module named 'numpy'"

**Solution:**
```bash
pip install numpy
```

### Problem: "Python is not installed"

**Solution:** Install Python from https://python.org
- Make sure to check "Add Python to PATH"!

## Quick Commands

Once installed:

```bash
# Run a file
mythos run file.mythos

# Interactive mode
mythos repl

# Create new project
mythos init my-project

# Get help
mythos --help
```

## Examples to Try

```bash
mythos run examples/hello_world.mythos
mythos run examples/math_demo.mythos
mythos run examples/web_app.mythos
mythos run examples/game_2d.mythos
mythos run examples/game_3d.mythos
```

## Still Having Issues?

1. Check [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) - Detailed troubleshooting
2. Check [QUICKSTART.md](QUICKSTART.md) - Step-by-step guide
3. Run `python test_installation.py` - Diagnose problems

## Summary

1. Mythos is **not in package managers yet** (it's brand new!)
2. Install it **locally** from the Mythos folder
3. Use `pip install -e .` or run the installer scripts
4. Or just run directly with `python mythos_cli/cli.py`

That's it! 🚀
