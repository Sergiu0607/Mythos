# Mythos Installation Guide

## Current Status

Mythos is a **newly created programming language** that exists as a local project on your machine. It's not yet published to package managers like Homebrew, Chocolatey, or PyPI.

## Why Package Managers Don't Work Yet

When you try:
```bash
brew install mythos      # ❌ Won't work
choco install mythos     # ❌ Won't work
pip install mythos-lang  # ❌ Won't work
```

These fail because Mythos hasn't been published to these repositories yet. This is normal for a new project!

## How to Install Mythos (Current Method)

### Method 1: Automated Installation (Easiest)

**Windows:**
1. Open PowerShell or Command Prompt
2. Navigate to the Mythos folder:
   ```bash
   cd path\to\Mythos
   ```
3. Run the installer:
   ```bash
   install.bat
   ```

**macOS/Linux:**
1. Open Terminal
2. Navigate to the Mythos folder:
   ```bash
   cd path/to/Mythos
   ```
3. Make the installer executable and run it:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

### Method 2: Manual Installation

**Step 1: Check Python**
```bash
python --version
# Should show Python 3.8 or higher
```

**Step 2: Install Dependencies**
```bash
# Windows
pip install numpy

# macOS/Linux
pip3 install numpy
```

**Step 3: Install Mythos**
```bash
# Windows
cd path\to\Mythos
pip install -e .

# macOS/Linux
cd path/to/Mythos
pip3 install -e .
```

**Step 4: Verify**
```bash
mythos --version
```

### Method 3: Run Without Installing

If you don't want to install, just run directly:

```bash
# Windows
python mythos_cli\cli.py run examples\hello_world.mythos

# macOS/Linux
python3 mythos_cli/cli.py run examples/hello_world.mythos
```

## Troubleshooting

### "mythos: command not found"

This means Python's Scripts folder isn't in your PATH.

**Quick Fix - Use Python directly:**
```bash
python mythos_cli/cli.py run file.mythos
```

**Permanent Fix - Add to PATH:**

**Windows:**
1. Search for "Environment Variables" in Start Menu
2. Click "Environment Variables"
3. Under "User variables", find "Path"
4. Add: `C:\Users\YourName\AppData\Local\Programs\Python\Python311\Scripts`
5. Restart terminal

**macOS/Linux:**
Add to `~/.bashrc` or `~/.zshrc`:
```bash
export PATH="$HOME/.local/bin:$PATH"
```
Then run: `source ~/.bashrc`

### "Python is not installed"

**Windows:**
1. Download from https://python.org
2. Run installer
3. ✅ CHECK "Add Python to PATH"
4. Restart terminal

**macOS:**
```bash
brew install python3
```

**Linux:**
```bash
sudo apt install python3 python3-pip  # Ubuntu/Debian
sudo dnf install python3 python3-pip  # Fedora
```

### "ModuleNotFoundError: No module named 'numpy'"

```bash
pip install numpy
```

### "Permission denied" (Linux/macOS)

```bash
pip3 install --user -e .
```

## Testing Your Installation

### Test 1: Version Check
```bash
mythos --version
```

### Test 2: Hello World
```bash
mythos run examples/hello_world.mythos
```

### Test 3: REPL
```bash
mythos repl
>>> print("It works!")
>>> exit
```

### Test 4: Math Demo
```bash
mythos run examples/math_demo.mythos
```

## Creating an Alias (Optional)

If `mythos` command doesn't work, create an alias:

**Windows PowerShell:**
Add to your PowerShell profile:
```powershell
function mythos { python C:\path\to\Mythos\mythos_cli\cli.py $args }
```

**macOS/Linux Bash/Zsh:**
Add to `~/.bashrc` or `~/.zshrc`:
```bash
alias mythos='python3 /path/to/Mythos/mythos_cli/cli.py'
```

## Future: Official Package Manager Support

Once Mythos is published, you'll be able to install via:

```bash
# PyPI (Python Package Index)
pip install mythos-lang

# Homebrew (macOS)
brew install mythos

# Chocolatey (Windows)
choco install mythos

# APT (Ubuntu/Debian)
sudo apt install mythos
```

But for now, use the local installation methods above!

## Quick Reference

```bash
# After installation, use these commands:
mythos run file.mythos          # Run a program
mythos repl                     # Interactive shell
mythos init my-project          # Create project
mythos web app.mythos           # Start web server
mythos game game.mythos         # Run game
mythos --help                   # Show help
```

## Need More Help?

- See [QUICKSTART.md](QUICKSTART.md) for a step-by-step guide
- See [README.md](README.md) for project overview
- See [docs/getting-started.md](docs/getting-started.md) for tutorials
- Check [docs/command-reference.md](docs/command-reference.md) for all commands

## Summary

✅ Mythos is installed locally, not from package managers
✅ Use `install.bat` (Windows) or `install.sh` (macOS/Linux)
✅ Or run directly: `python mythos_cli/cli.py`
✅ Package manager support coming in the future!

Happy coding with Mythos! 🚀
