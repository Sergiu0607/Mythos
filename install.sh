#!/bin/bash
# Mythos Installation Script for macOS/Linux

echo "========================================="
echo "  Mythos Programming Language Installer"
echo "========================================="
echo ""

# Check Python version
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
    PIP_CMD=pip3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
    PIP_CMD=pip
else
    echo "❌ Error: Python is not installed."
    echo "Please install Python 3.8 or higher from https://python.org"
    exit 1
fi

echo "✓ Found Python: $($PYTHON_CMD --version)"

# Check Python version is 3.8+
PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Error: Python $REQUIRED_VERSION or higher is required."
    echo "You have Python $PYTHON_VERSION"
    exit 1
fi

echo "✓ Python version is compatible"

# Install dependencies
echo ""
echo "Installing dependencies..."
$PIP_CMD install numpy --quiet

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Install Mythos
echo ""
echo "Installing Mythos..."
$PIP_CMD install -e . --quiet

if [ $? -eq 0 ]; then
    echo "✓ Mythos installed successfully!"
else
    echo "❌ Failed to install Mythos"
    exit 1
fi

# Verify installation
echo ""
echo "Verifying installation..."

if command -v mythos &> /dev/null; then
    echo "✓ Mythos command is available"
    mythos --version
else
    echo "⚠️  Warning: 'mythos' command not found in PATH"
    echo ""
    echo "You can still run Mythos using:"
    echo "  $PYTHON_CMD mythos_cli/cli.py"
    echo ""
    echo "Or add Python scripts to your PATH:"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
    echo "Add this line to your ~/.bashrc or ~/.zshrc to make it permanent"
fi

echo ""
echo "========================================="
echo "  Installation Complete! 🎉"
echo "========================================="
echo ""
echo "Try these commands:"
echo "  mythos run examples/hello_world.mythos"
echo "  mythos repl"
echo "  mythos --help"
echo ""
echo "For more information, see QUICKSTART.md"
