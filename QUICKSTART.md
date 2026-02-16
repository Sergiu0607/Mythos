# Mythos Quick Start Guide

Get Mythos running on your machine in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip (comes with Python)

Check your Python version:
```bash
python --version
# or
python3 --version
```

## Installation

### Step 1: Navigate to Mythos Directory

```bash
cd path/to/Mythos
```

### Step 2: Install Dependencies

```bash
# Windows
pip install numpy

# macOS/Linux
pip3 install numpy
```

### Step 3: Install Mythos

**Option A: Install as Package (Recommended)**
```bash
# Windows
pip install -e .

# macOS/Linux
pip3 install -e .
```

**Option B: Run Without Installing**
```bash
# Just use Python directly
python mythos_cli/cli.py --help
```

### Step 4: Verify Installation

If you installed as a package:
```bash
mythos --version
```

If running directly:
```bash
python mythos_cli/cli.py --version
```

## Your First Program

### 1. Hello World

Create a file `hello.mythos`:
```mythos
print("Hello, Mythos!")
```

Run it:
```bash
# If installed
mythos run hello.mythos

# If running directly
python mythos_cli/cli.py run hello.mythos
```

### 2. Try the Examples

Run the included examples:

```bash
# Hello World
mythos run examples/hello_world.mythos

# Math Demo
mythos run examples/math_demo.mythos

# Web App (starts server on port 8000)
mythos run examples/web_app.mythos

# 2D Game
mythos run examples/game_2d.mythos

# 3D Game
mythos run examples/game_3d.mythos
```

### 3. Interactive REPL

Try the interactive shell:

```bash
mythos repl
```

Then type:
```mythos
>>> x = 10
>>> y = 20
>>> print(x + y)
30
>>> exit
```

## Common Issues & Solutions

### Issue: "mythos: command not found"

**Solution 1**: Add Python Scripts to PATH

Windows:
```bash
# Add to PATH (replace with your Python version)
set PATH=%PATH%;C:\Users\YourName\AppData\Local\Programs\Python\Python311\Scripts
```

macOS/Linux:
```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"
```

**Solution 2**: Use Python directly
```bash
python mythos_cli/cli.py run file.mythos
```

**Solution 3**: Create an alias

Windows (PowerShell profile):
```powershell
function mythos { python path/to/Mythos/mythos_cli/cli.py $args }
```

macOS/Linux (~/.bashrc or ~/.zshrc):
```bash
alias mythos='python3 /path/to/Mythos/mythos_cli/cli.py'
```

### Issue: "ModuleNotFoundError: No module named 'numpy'"

**Solution**: Install numpy
```bash
pip install numpy
```

### Issue: "No module named 'compiler'"

**Solution**: Make sure you're in the Mythos directory and the folder structure is intact.

## Quick Command Reference

```bash
# Run a program
mythos run file.mythos

# Start REPL
mythos repl

# Create new project
mythos init my-project

# Start web server
mythos web app.mythos --port 8000

# Run a game
mythos game game.mythos

# Build to bytecode
mythos build file.mythos

# Get help
mythos --help
```

## Next Steps

1. Read the [Language Reference](docs/language-reference.md)
2. Explore [Command Reference](docs/command-reference.md)
3. Check out [Examples](examples/)
4. Read [Getting Started Guide](docs/getting-started.md)

## Development Mode

If you want to modify Mythos itself:

```bash
# Install in editable mode
pip install -e .

# Make changes to the code
# Changes take effect immediately

# Run tests
python -m pytest tests/
```

## Troubleshooting

### Windows-Specific

If you see "Python was not found":
1. Install Python from python.org
2. Check "Add Python to PATH" during installation
3. Restart your terminal

### macOS-Specific

If you have multiple Python versions:
```bash
# Use python3 explicitly
python3 mythos_cli/cli.py run file.mythos
```

### Linux-Specific

If pip install fails with permissions:
```bash
# Install for user only
pip3 install --user -e .
```

## Success!

You're now ready to build with Mythos! 🚀

Try creating your first program:

```mythos
# my_first_app.mythos
print("I'm coding in Mythos!")

x = 10
y = 20
print("Sum:", x + y)

function greet(name) {
  return "Hello, " + name + "!"
}

print(greet("World"))
```

Run it:
```bash
mythos run my_first_app.mythos
```

Happy coding! 🎉
