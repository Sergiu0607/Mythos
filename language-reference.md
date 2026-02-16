# Mythos Language Reference

Complete reference for the Mythos programming language.

## Table of Contents

1. [Syntax](#syntax)
2. [Data Types](#data-types)
3. [Operators](#operators)
4. [Control Flow](#control-flow)
5. [Functions](#functions)
6. [Classes](#classes)
7. [Modules](#modules)

## Syntax

### Comments

```mythos
# Single-line comment

# Multi-line comments
# are just multiple
# single-line comments
```

### Statements

Statements can be separated by newlines or semicolons:

```mythos
x = 10
y = 20

# Or
x = 10; y = 20
```

## Data Types

### Numbers

```mythos
integer = 42
float_num = 3.14
negative = -10
scientific = 1.5e10
```

### Strings

```mythos
single = 'Hello'
double = "World"
multiline = "This is a
multiline string"

# String concatenation
greeting = "Hello" + " " + "World"

# String interpolation (planned)
name = "Alice"
message = "Hello, ${name}!"
```

### Booleans

```mythos
is_true = true
is_false = false
```

### Null

```mythos
empty = null
```

### Arrays

```mythos
numbers = [1, 2, 3, 4, 5]
mixed = [1, "two", true, null]

# Access
first = numbers[0]

# Methods
numbers.push(6)
numbers.pop()
length = numbers.length()
```

### Objects

```mythos
person = {
  name: "Alice",
  age: 30,
  address: {
    city: "New York",
    zip: "10001"
  }
}

# Access
name = person.name
city = person.address.city

# Modify
person.age = 31
```

### Vectors

```mythos
# 2D Vector
v2 = Vector2(10, 20)
v2.x = 15
length = v2.length()

# 3D Vector
v3 = Vector3(1, 2, 3)
normalized = v3.normalize()
```

## Operators

### Arithmetic

```mythos
x + y    # Addition
x - y    # Subtraction
x * y    # Multiplication
x / y    # Division
x ^ y    # Power
x % y    # Modulo
-x       # Negation
```

### Comparison

```mythos
x == y   # Equal
x != y   # Not equal
x < y    # Less than
x > y    # Greater than
x <= y   # Less than or equal
x >= y   # Greater than or equal
```

### Logical

```mythos
x and y  # Logical AND
x or y   # Logical OR
not x    # Logical NOT
```

### Assignment

```mythos
x = 10       # Assignment
x += 5       # Add and assign
x -= 5       # Subtract and assign
x *= 2       # Multiply and assign
x /= 2       # Divide and assign
```

## Control Flow

### If Statements

```mythos
if condition {
  # code
}

if condition {
  # code
} else {
  # code
}

if condition1 {
  # code
} elif condition2 {
  # code
} else {
  # code
}
```

### While Loops

```mythos
while condition {
  # code
}

# With break and continue
while true {
  if should_break {
    break
  }
  if should_skip {
    continue
  }
  # code
}
```

### For Loops

```mythos
# Iterate over range
for i in range(10) {
  print(i)
}

# Iterate over array
for item in array {
  print(item)
}

# Iterate over object keys
for key in object.keys() {
  print(key, object[key])
}
```

### Match Statements (Pattern Matching)

```mythos
match value {
  case 1 {
    print("One")
  }
  case 2 {
    print("Two")
  }
  default {
    print("Other")
  }
}
```

## Functions

### Function Declaration

```mythos
function add(a, b) {
  return a + b
}

# Call
result = add(5, 3)
```

### Arrow Functions

```mythos
add = (a, b) -> a + b

# Multi-line
multiply = (a, b) -> {
  result = a * b
  return result
}
```

### Default Parameters

```mythos
function greet(name = "World") {
  return "Hello, " + name + "!"
}

greet()          # "Hello, World!"
greet("Alice")   # "Hello, Alice!"
```

### Rest Parameters

```mythos
function sum(...numbers) {
  total = 0
  for num in numbers {
    total += num
  }
  return total
}

sum(1, 2, 3, 4, 5)  # 15
```

### Higher-Order Functions

```mythos
function apply(func, value) {
  return func(value)
}

double = (x) -> x * 2
result = apply(double, 5)  # 10
```

## Classes

### Class Declaration

```mythos
class Person {
  function constructor(name, age) {
    this.name = name
    this.age = age
  }
  
  function greet() {
    return "Hello, I'm " + this.name
  }
  
  function birthday() {
    this.age += 1
  }
}

# Create instance
person = new Person("Alice", 30)
person.greet()
person.birthday()
```

### Inheritance

```mythos
class Student extends Person {
  function constructor(name, age, grade) {
    super(name, age)
    this.grade = grade
  }
  
  function study() {
    print(this.name + " is studying")
  }
}

student = new Student("Bob", 20, "A")
student.greet()
student.study()
```

## Modules

### Import

```mythos
import math
import web
import game

# Import specific items
from math import sin, cos, Vector3
from web import ui, server
```

### Export

```mythos
# In module file
export function myFunction() {
  # code
}

export class MyClass {
  # code
}

export const MY_CONSTANT = 42
```

## Special Constructs

### Scene Declaration (for games)

```mythos
scene main {
  camera position:(0, 5, 10)
  light sun type:directional
  cube size:1 position:(0, 0, 0)
}
```

### Web App Declaration

```mythos
web.app {
  route "/" {
    # handler code
  }
}
```

## Built-in Functions

### Console

```mythos
print(value)           # Print to console
input(prompt)          # Get user input
```

### Type Conversion

```mythos
string(value)          # Convert to string
number(value)          # Convert to number
boolean(value)         # Convert to boolean
```

### Array Functions

```mythos
len(array)             # Get length
range(start, end)      # Create range
```

### Math Functions

```mythos
abs(x)                 # Absolute value
sqrt(x)                # Square root
sin(x), cos(x), tan(x) # Trigonometry
floor(x), ceil(x)      # Rounding
min(...), max(...)     # Min/Max
```

## Error Handling

```mythos
try {
  # code that might fail
} catch error {
  print("Error:", error)
} finally {
  # cleanup code
}
```

## Async/Await

```mythos
async function fetchData(url) {
  response = await http.get(url)
  return response.json()
}

# Use
data = await fetchData("https://api.example.com/data")
```
