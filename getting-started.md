# Getting Started with Mythos

Welcome to Mythos! This guide will help you get started with the Mythos programming language.

## Installation

### Option 1: Install from Source (Current Method)

Since Mythos is a new project, you'll install it locally:

#### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

#### Installation Steps

**1. Navigate to the Mythos directory:**
```bash
cd path/to/Mythos
```

**2. Install in development mode:**
```bash
# Windows (PowerShell/CMD)
python setup.py develop

# macOS/Linux
python3 setup.py develop
```

Or using pip:
```bash
# Windows
pip install -e .

# macOS/Linux
pip3 install -e .
```

**3. Verify installation:**
```bash
mythos --version
```

If you get "command not found", you may need to add Python's Scripts directory to your PATH:
- **Windows**: `C:\Users\YourName\AppData\Local\Programs\Python\Python3X\Scripts`
- **macOS/Linux**: `~/.local/bin` or `/usr/local/bin`

### Option 2: Run Directly with Python

If you don't want to install, you can run Mythos directly:

```bash
# Windows
python mythos_cli/cli.py run examples/hello_world.mythos

# macOS/Linux
python3 mythos_cli/cli.py run examples/hello_world.mythos
```

### Option 3: Future Installation (Coming Soon)

Once published, you'll be able to install via:

```bash
# PyPI (Python Package Index)
pip install mythos-lang

# Homebrew (macOS)
brew install mythos

# Chocolatey (Windows)
choco install mythos

# APT (Debian/Ubuntu)
sudo apt install mythos
```

## Your First Mythos Program

Create a file called `hello.mythos`:

```mythos
print("Hello, Mythos!")
```

Run it:

```bash
mythos run hello.mythos
```

## Basic Syntax

### Variables

```mythos
# Variables are dynamically typed
x = 10
name = "Mythos"
is_awesome = true
```

### Functions

```mythos
function greet(name) {
  return "Hello, " + name + "!"
}

message = greet("World")
print(message)
```

### Control Flow

```mythos
# If statements
if x > 10 {
  print("x is greater than 10")
} else {
  print("x is 10 or less")
}

# While loops
count = 0
while count < 5 {
  print(count)
  count = count + 1
}

# For loops
for i in range(5) {
  print(i)
}
```

### Arrays and Objects

```mythos
# Arrays
numbers = [1, 2, 3, 4, 5]
print(numbers[0])  # 1

# Objects
person = {
  name: "Alice",
  age: 30,
  city: "New York"
}
print(person.name)  # Alice
```

## Math Operations

```mythos
# Basic arithmetic
x = 10 + 5
y = 10 - 5
z = 10 * 5
w = 10 / 5
p = 2 ^ 3  # Power: 8

# Advanced math
angle = 45
sin_value = sin(angle)
cos_value = cos(angle)
sqrt_value = sqrt(16)

# Vectors
v1 = Vector3(1, 2, 3)
v2 = Vector3(4, 5, 6)
v3 = v1 + v2
```

## Web Development

```mythos
web.app {
  route "/" {
    page = ui.page("My App")
    page.add(ui.text("Hello, Web!", "h1"))
    page.add(ui.button("Click Me"))
    return page.render()
  }
}

web.start(port: 8000)
```

## Game Development

```mythos
scene main {
  camera position:(0, 5, 10)
  light sun type:directional
  cube size:1 position:(0, 0, 0) color:#FF0000
}

function update(dt) {
  # Game logic
}

game.start()
```

## CLI Commands

```bash
# Run a file
mythos run file.mythos

# Build to bytecode
mythos build file.mythos

# Start web server
mythos web app.mythos --port 8000

# Run a game
mythos game game.mythos

# Interactive REPL
mythos repl

# Create new project
mythos init my-project --type web
```

## Next Steps

- Read the [Language Reference](language-reference.md)
- Explore [Examples](../examples/)
- Check out the [Standard Library](stdlib.md)
- Learn about [Web Development](web.md)
- Learn about [Game Development](games.md)

## Getting Help

- Documentation: https://mythos-lang.org/docs
- Community: https://community.mythos-lang.org
- GitHub: https://github.com/mythos-lang/mythos
- Discord: https://discord.gg/mythos
