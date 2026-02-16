# Mythos Architecture

This document describes the internal architecture of the Mythos programming language.

## Overview

Mythos is a compiled, dynamically-typed programming language with a bytecode virtual machine. The architecture follows a traditional compiler pipeline with modern optimizations.

```
Source Code → Lexer → Parser → AST → Bytecode Compiler → VM → Execution
```

## Components

### 1. Compiler Pipeline

#### Lexer (`compiler/lexer/`)
- **Purpose**: Tokenizes source code into a stream of tokens
- **Input**: Raw source code (string)
- **Output**: List of tokens with type, value, and position information
- **Features**:
  - Handles numbers, strings, identifiers, keywords, operators
  - Supports comments
  - Tracks line and column numbers for error reporting
  - Efficient single-pass scanning

#### Parser (`compiler/parser/`)
- **Purpose**: Builds Abstract Syntax Tree (AST) from tokens
- **Input**: Token stream from lexer
- **Output**: AST representing program structure
- **Features**:
  - Recursive descent parser
  - Operator precedence handling
  - Support for expressions, statements, functions, classes
  - Special constructs for scenes and web apps
  - Error recovery and reporting

#### AST (`compiler/ast/`)
- **Purpose**: Represents program structure as a tree
- **Components**:
  - Expression nodes (literals, binary ops, calls, etc.)
  - Statement nodes (if, while, for, return, etc.)
  - Declaration nodes (functions, classes, variables)
  - Special nodes (scenes, routes, etc.)

#### Bytecode Compiler (`compiler/bytecode/`)
- **Purpose**: Compiles AST to bytecode instructions
- **Input**: AST
- **Output**: Bytecode instructions and constant pool
- **Features**:
  - Stack-based instruction set
  - Constant folding
  - Jump optimization
  - Label resolution
  - Support for closures and nested functions

### 2. Runtime System

#### Virtual Machine (`runtime/vm.py`)
- **Purpose**: Executes bytecode instructions
- **Architecture**: Stack-based VM
- **Features**:
  - Instruction dispatch loop
  - Stack management
  - Variable scoping (local and global)
  - Function call frames
  - Built-in function integration
  - Exception handling

#### Instruction Set
- **Stack Operations**: LOAD_CONST, LOAD_VAR, STORE_VAR, POP, DUP
- **Arithmetic**: ADD, SUB, MUL, DIV, POW, MOD, NEG
- **Comparison**: EQ, NE, LT, GT, LE, GE
- **Logical**: AND, OR, NOT
- **Control Flow**: JUMP, JUMP_IF_FALSE, JUMP_IF_TRUE
- **Functions**: CALL, RETURN, MAKE_FUNCTION
- **Objects**: MAKE_ARRAY, MAKE_OBJECT, GET_MEMBER, SET_MEMBER
- **Special**: IMPORT, CREATE_SCENE, ADD_ROUTE

### 3. Standard Library

#### Math (`standard_library/math/`)
- **core.py**: Basic math, vectors, matrices
  - Vector2, Vector3 classes
  - Matrix4 for transformations
  - Trigonometric functions
  - Linear algebra operations
  
- **physics.py**: Physics calculations
  - Kinematics equations
  - Dynamics (force, momentum, energy)
  - Collision detection
  - Gravity calculations
  - Thermodynamics

#### AI (`standard_library/ai/`)
- **behavior_tree.py**: Behavior trees for game AI
  - Node types: Action, Condition, Sequence, Selector, Parallel
  - Decorators: Inverter, Repeater
  - Builder pattern for easy construction
  
- **pathfinding.py**: Pathfinding algorithms
  - A* algorithm
  - Dijkstra's algorithm
  - Breadth-first search
  - Grid-based navigation
  - Path smoothing
  - NavMesh support

### 4. Graphics Engine

#### Rendering (`engine/rendering/`)
- **renderer.py**: Core rendering system
  - Color management
  - Material system
  - Mesh generation (cube, sphere, plane)
  - Light sources
  - Camera system
  - Render pipeline

#### Scene Management (`engine/scene/`)
- **scene.py**: Scene graph and entity system
  - Entity-component architecture
  - Scene hierarchy
  - Camera entities
  - Light entities
  - Mesh entities
  - Scene manager for multiple scenes

#### 2D Engine (`engine/2d/`)
- **sprite.py**: 2D sprite system
  - Sprite rendering
  - Animation system
  - Sprite sheets
  - Particle systems
  - Tile maps

#### 3D Engine (`engine/3d/`)
- **camera.py**: Advanced camera systems
  - Free camera
  - Orbit camera
  - First-person camera
  - Third-person camera
  - Cinematic camera with waypoints

### 5. Web Framework

#### Server (`web/server/`)
- **http_server.py**: Built-in HTTP server
  - Request/Response abstraction
  - Routing system
  - Middleware support
  - JSON support
  - Static file serving

#### Frontend (`web/frontend/`)
- **ui.py**: UI framework without HTML/CSS
  - Component-based UI
  - Layout containers (Row, Column, Grid)
  - Common widgets (Button, Input, Text, Image)
  - Card and List components
  - Page builder
  - Automatic HTML generation

### 6. Development Tools

#### CLI (`mythos_cli/`)
- **cli.py**: Command-line interface
  - `mythos run`: Execute Mythos files
  - `mythos build`: Compile to bytecode
  - `mythos web`: Start web server
  - `mythos game`: Run games
  - `mythos repl`: Interactive shell
  - `mythos init`: Project scaffolding

#### Debugger (`tools/debugger.py`)
- Breakpoints with conditions
- Step over/into/out
- Variable inspection
- Watch expressions
- Call stack visualization
- Expression evaluation

#### Profiler (`tools/debugger.py`)
- Function timing
- Call counting
- Instruction statistics
- Performance reports

## Data Flow

### Compilation Flow
```
1. Source Code (string)
   ↓
2. Lexer → Tokens
   ↓
3. Parser → AST
   ↓
4. Bytecode Compiler → Instructions + Constants
   ↓
5. VM Execution
```

### Execution Flow
```
1. VM loads bytecode
   ↓
2. Instruction dispatch loop
   ↓
3. Stack operations
   ↓
4. Variable lookups (local → global)
   ↓
5. Function calls (new call frame)
   ↓
6. Built-in function integration
   ↓
7. Return values
```

### Scene Rendering Flow
```
1. Scene definition (Mythos code)
   ↓
2. Scene parser creates entities
   ↓
3. Entity components attached
   ↓
4. Update loop (game logic)
   ↓
5. Render loop
   ↓
6. Camera transformation
   ↓
7. Mesh rendering
   ↓
8. Display
```

## Memory Management

### Stack
- Used for expression evaluation
- Function arguments
- Temporary values
- Grows and shrinks during execution

### Heap
- Objects and arrays
- Function closures
- Class instances
- Managed by Python's garbage collector

### Call Stack
- Function call frames
- Local variables
- Return addresses
- Limited depth to prevent stack overflow

## Optimization Strategies

### Compile-Time
- Constant folding
- Dead code elimination
- Jump optimization
- Inline caching (planned)

### Runtime
- Efficient instruction dispatch
- Stack-based architecture (fewer memory accesses)
- Built-in function optimization
- JIT compilation (planned)

## Extension Points

### Custom Built-ins
Add functions to `VirtualMachine._init_builtins()`

### New Opcodes
1. Add to `OpCode` enum
2. Implement in `BytecodeCompiler.compile()`
3. Handle in `VirtualMachine.execute()`

### Standard Library Modules
Create new modules in `standard_library/`

### Language Features
1. Add tokens to `Lexer`
2. Add AST nodes to `compiler/ast/nodes.py`
3. Add parsing logic to `Parser`
4. Add compilation logic to `BytecodeCompiler`
5. Add execution logic to `VirtualMachine`

## Performance Characteristics

### Time Complexity
- Lexing: O(n) where n = source length
- Parsing: O(n) where n = token count
- Compilation: O(n) where n = AST nodes
- Execution: O(i) where i = instruction count

### Space Complexity
- Tokens: O(n)
- AST: O(n)
- Bytecode: O(n)
- Stack: O(d) where d = call depth
- Heap: O(m) where m = allocated objects

## Future Enhancements

### Planned Features
1. **JIT Compilation**: Compile hot paths to native code
2. **Type Inference**: Optional static typing
3. **Async/Await**: Native async support
4. **Module System**: Better import/export
5. **Package Manager**: Dependency management
6. **LSP Server**: IDE integration
7. **Debugger Protocol**: Remote debugging
8. **WASM Target**: Compile to WebAssembly
9. **GPU Compute**: Shader integration
10. **Native Extensions**: C/C++ bindings

### Optimization Opportunities
1. Inline caching for property access
2. Hidden classes for objects
3. Specialized instructions for common patterns
4. Register-based VM (alternative to stack)
5. Bytecode verification
6. Profile-guided optimization
7. Escape analysis
8. Loop unrolling
9. Tail call optimization
10. Constant propagation

## Testing Strategy

### Unit Tests
- Lexer: Token generation
- Parser: AST construction
- Compiler: Bytecode generation
- VM: Instruction execution
- Standard library: Function correctness

### Integration Tests
- End-to-end compilation
- Example programs
- Web applications
- Game scenarios

### Performance Tests
- Benchmark suite
- Memory profiling
- Execution speed
- Compilation speed

## Security Considerations

### Sandboxing
- Limit file system access
- Network restrictions
- Resource limits (memory, CPU)
- Safe built-in functions

### Input Validation
- Source code sanitization
- Bytecode verification
- Type checking
- Bounds checking

## Conclusion

Mythos is designed to be simple yet powerful, with a clean architecture that's easy to understand and extend. The modular design allows for independent development of components while maintaining a cohesive system.
