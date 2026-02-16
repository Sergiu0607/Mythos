# Mythos Command Reference

Complete reference of all commands, functions, and APIs available in Mythos.

## Table of Contents

1. [Built-in Functions](#built-in-functions)
2. [Math Functions](#math-functions)
3. [Vector & Matrix Operations](#vector--matrix-operations)
4. [Physics Functions](#physics-functions)
5. [Web Framework](#web-framework)
6. [UI Components](#ui-components)
7. [Game Engine](#game-engine)
8. [AI Functions](#ai-functions)
9. [File I/O](#file-io)
10. [CLI Commands](#cli-commands)

---

## Built-in Functions

### Console & I/O

```mythos
print(value1, value2, ...)
# Print values to console
# Example: print("Hello", "World")

input(prompt)
# Get user input
# Example: name = input("Enter name: ")
```

### Type Conversion

```mythos
string(value)
# Convert to string
# Example: string(42) → "42"

number(value)
# Convert to number
# Example: number("3.14") → 3.14

boolean(value)
# Convert to boolean
# Example: boolean(1) → true
```

### Array Functions

```mythos
len(array)
# Get length of array/string
# Example: len([1, 2, 3]) → 3

range(start, end, step)
# Create range of numbers
# Example: range(0, 10) → [0, 1, 2, ..., 9]
# Example: range(0, 10, 2) → [0, 2, 4, 6, 8]
```


---

## Math Functions

### Basic Math

```mythos
abs(x)
# Absolute value
# Example: abs(-10) → 10

sqrt(x)
# Square root
# Example: sqrt(16) → 4

pow(x, y)
# Power (also: x ^ y)
# Example: pow(2, 3) → 8

cbrt(x)
# Cube root
# Example: cbrt(27) → 3

min(a, b, ...)
# Minimum value
# Example: min(5, 2, 8) → 2

max(a, b, ...)
# Maximum value
# Example: max(5, 2, 8) → 8

clamp(value, min, max)
# Clamp value between min and max
# Example: clamp(15, 0, 10) → 10
```

### Trigonometry

```mythos
sin(x)
# Sine (radians)
# Example: sin(PI / 2) → 1

cos(x)
# Cosine (radians)
# Example: cos(0) → 1

tan(x)
# Tangent (radians)
# Example: tan(PI / 4) → 1

asin(x)
# Arc sine
# Example: asin(1) → PI / 2

acos(x)
# Arc cosine
# Example: acos(1) → 0

atan(x)
# Arc tangent
# Example: atan(1) → PI / 4

atan2(y, x)
# Two-argument arc tangent
# Example: atan2(1, 1) → PI / 4
```

### Exponential & Logarithmic

```mythos
exp(x)
# e^x
# Example: exp(1) → 2.718...

log(x, base)
# Logarithm (default base e)
# Example: log(10) → 2.302...
# Example: log(100, 10) → 2

log10(x)
# Base-10 logarithm
# Example: log10(1000) → 3

log2(x)
# Base-2 logarithm
# Example: log2(8) → 3
```

### Rounding

```mythos
floor(x)
# Round down
# Example: floor(3.7) → 3

ceil(x)
# Round up
# Example: ceil(3.2) → 4

round(x, decimals)
# Round to nearest
# Example: round(3.14159, 2) → 3.14

trunc(x)
# Truncate decimal
# Example: trunc(3.9) → 3
```

### Utility

```mythos
sign(x)
# Sign of number (-1, 0, 1)
# Example: sign(-5) → -1

lerp(a, b, t)
# Linear interpolation
# Example: lerp(0, 10, 0.5) → 5

random_float(min, max)
# Random float between min and max
# Example: random_float(0, 1) → 0.573...

random_int(min, max)
# Random integer between min and max
# Example: random_int(1, 6) → 4
```

### Constants

```mythos
PI        # 3.14159...
E         # 2.71828...
TAU       # 6.28318... (2 * PI)
INF       # Infinity
NAN       # Not a Number
```


---

## Vector & Matrix Operations

### Vector2 (2D Vectors)

```mythos
v = Vector2(x, y)
# Create 2D vector
# Example: v = Vector2(10, 20)

v.x, v.y
# Access components
# Example: v.x → 10

v1 + v2
# Vector addition
# Example: Vector2(1, 2) + Vector2(3, 4) → Vector2(4, 6)

v1 - v2
# Vector subtraction

v * scalar
# Scalar multiplication
# Example: Vector2(2, 3) * 2 → Vector2(4, 6)

v / scalar
# Scalar division

v.dot(other)
# Dot product
# Example: Vector2(1, 0).dot(Vector2(0, 1)) → 0

v.length()
# Vector magnitude
# Example: Vector2(3, 4).length() → 5

v.normalize()
# Normalized vector (length 1)
# Example: Vector2(3, 4).normalize() → Vector2(0.6, 0.8)

v.distance_to(other)
# Distance to another vector
# Example: Vector2(0, 0).distance_to(Vector2(3, 4)) → 5

v.angle()
# Angle in radians
# Example: Vector2(1, 1).angle() → PI / 4

v.rotate(angle)
# Rotate by angle (radians)
# Example: Vector2(1, 0).rotate(PI / 2) → Vector2(0, 1)
```

### Vector3 (3D Vectors)

```mythos
v = Vector3(x, y, z)
# Create 3D vector
# Example: v = Vector3(1, 2, 3)

v.x, v.y, v.z
# Access components

v1 + v2, v1 - v2, v * scalar, v / scalar
# Same operations as Vector2

v.dot(other)
# Dot product
# Example: Vector3(1, 0, 0).dot(Vector3(0, 1, 0)) → 0

v.cross(other)
# Cross product
# Example: Vector3(1, 0, 0).cross(Vector3(0, 1, 0)) → Vector3(0, 0, 1)

v.length()
# Vector magnitude

v.normalize()
# Normalized vector

v.distance_to(other)
# Distance to another vector
```

### Matrix4 (4x4 Matrices)

```mythos
m = Matrix4()
# Create identity matrix

m = Matrix4(elements)
# Create from 16 elements

m1.multiply(m2)
# Matrix multiplication

m.translate(x, y, z)
# Create translation matrix

m.scale(x, y, z)
# Create scale matrix

m.rotate_x(angle)
# Rotate around X axis

m.rotate_y(angle)
# Rotate around Y axis

m.rotate_z(angle)
# Rotate around Z axis
```


---

## Physics Functions

### Kinematics

```mythos
velocity(distance, time)
# Calculate velocity: v = d/t
# Example: velocity(100, 10) → 10

acceleration(velocity_change, time)
# Calculate acceleration: a = Δv/t
# Example: acceleration(20, 5) → 4

distance_with_constant_acceleration(v0, a, t)
# Distance: d = v₀t + ½at²
# Example: distance_with_constant_acceleration(0, 10, 5) → 125

final_velocity(v0, a, t)
# Final velocity: v = v₀ + at
# Example: final_velocity(10, 5, 2) → 20

projectile_motion(velocity, angle, gravity)
# Calculate projectile motion
# Returns: (max_height, range, time_of_flight)
# Example: projectile_motion(20, 45) → (10.2, 40.8, 2.88)
```

### Dynamics

```mythos
force(mass, acceleration)
# Newton's second law: F = ma
# Example: force(10, 5) → 50

momentum(mass, velocity)
# Momentum: p = mv
# Example: momentum(5, 10) → 50

kinetic_energy(mass, velocity)
# Kinetic energy: KE = ½mv²
# Example: kinetic_energy(2, 10) → 100

potential_energy(mass, height, gravity)
# Potential energy: PE = mgh
# Example: potential_energy(10, 5) → 490.5

work(force, distance, angle)
# Work: W = Fd cos(θ)
# Example: work(10, 5, 0) → 50

power(work, time)
# Power: P = W/t
# Example: power(100, 10) → 10
```

### Collisions

```mythos
elastic_collision_1d(m1, v1, m2, v2)
# Elastic collision velocities
# Returns: (v1_final, v2_final)
# Example: elastic_collision_1d(1, 5, 1, 0) → (0, 5)

inelastic_collision_1d(m1, v1, m2, v2)
# Perfectly inelastic collision
# Returns: v_final
# Example: inelastic_collision_1d(2, 5, 3, 0) → 2
```

### Circular Motion

```mythos
centripetal_acceleration(velocity, radius)
# Centripetal acceleration: a = v²/r
# Example: centripetal_acceleration(10, 5) → 20

centripetal_force(mass, velocity, radius)
# Centripetal force: F = mv²/r
# Example: centripetal_force(2, 10, 5) → 40

angular_velocity(linear_velocity, radius)
# Angular velocity: ω = v/r
# Example: angular_velocity(10, 2) → 5
```

### Gravity

```mythos
gravitational_force(m1, m2, distance)
# Gravitational force: F = G(m1*m2)/r²
# Example: gravitational_force(1e10, 1e10, 1000) → 6674.3

escape_velocity(mass, radius)
# Escape velocity from celestial body
# Example: escape_velocity(5.972e24, 6.371e6) → 11186

GRAVITY_EARTH  # 9.81 m/s²
```

### Waves

```mythos
wave_speed(frequency, wavelength)
# Wave speed: v = fλ
# Example: wave_speed(440, 0.78) → 343.2

doppler_effect(source_freq, source_vel, observer_vel, wave_speed)
# Doppler effect frequency shift
# Example: doppler_effect(440, 10, 0, 343) → 453.2
```

### Thermodynamics

```mythos
celsius_to_fahrenheit(celsius)
# Convert C to F
# Example: celsius_to_fahrenheit(0) → 32

fahrenheit_to_celsius(fahrenheit)
# Convert F to C
# Example: fahrenheit_to_celsius(32) → 0

celsius_to_kelvin(celsius)
# Convert C to K
# Example: celsius_to_kelvin(0) → 273.15

kelvin_to_celsius(kelvin)
# Convert K to C
# Example: kelvin_to_celsius(273.15) → 0

ideal_gas_law(pressure, volume, n, temperature)
# PV = nRT (provide 3, get 4th)
# Example: ideal_gas_law(pressure:101325, volume:0.0224, n:1, temperature:None) → 273.15
```

### Physics Constants

```mythos
GRAVITY_EARTH          # 9.81 m/s²
SPEED_OF_LIGHT         # 299792458 m/s
PLANCK_CONSTANT        # 6.626e-34 J⋅s
BOLTZMANN_CONSTANT     # 1.381e-23 J/K
```


---

## Web Framework

### Server

```mythos
web.app { ... }
# Create web application
# Example:
# web.app {
#   route "/" { ... }
# }

web.start(port: 8000, host: "localhost")
# Start web server
# Example: web.start(port: 3000)

route "path" { ... }
# Define route handler
# Example:
# route "/" {
#   return ui.page("Home").render()
# }

route "/api/data" {
  return json({name: "Mythos", version: "1.0"})
}
```

### Request Object

```mythos
request.method
# HTTP method (GET, POST, etc.)

request.path
# Request path

request.query
# Query parameters
# Example: /search?q=mythos → request.query.q → "mythos"

request.headers
# Request headers

request.body
# Request body (string)

request.json()
# Parse body as JSON
# Example: data = request.json()

request.params
# URL parameters
# Example: /user/:id → request.params.id
```

### Response Object

```mythos
response.set_status(code)
# Set status code
# Example: response.set_status(404)

response.set_header(key, value)
# Set response header
# Example: response.set_header("Content-Type", "text/html")

response.json(data)
# Send JSON response
# Example: response.json({status: "ok"})

response.html(content)
# Send HTML response
# Example: response.html("<h1>Hello</h1>")

response.text(content)
# Send plain text
# Example: response.text("Hello World")
```

### Middleware

```mythos
server.use(middleware_function)
# Add middleware
# Example:
# function logger(request, response) {
#   print(request.method, request.path)
# }
# server.use(logger)
```


---

## UI Components

### Page

```mythos
ui.page(title)
# Create page
# Example: page = ui.page("My App")

page.add_element(element)
# Add element to page
# Example: page.add_element(ui.text("Hello"))

page.add_style(css)
# Add custom CSS
# Example: page.add_style("body { background: #f0f0f0; }")

page.add_script(js)
# Add custom JavaScript
# Example: page.add_script("console.log('Hello');")

page.render()
# Render to HTML
# Example: html = page.render()
```

### Text Elements

```mythos
ui.text(content, tag)
# Create text element
# Example: ui.text("Hello World", "h1")
# Example: ui.text("Paragraph", "p")

text.set_style(key, value)
# Set style
# Example: text.set_style("color", "red")
```

### Button

```mythos
ui.button(text, on_click)
# Create button
# Example: ui.button("Click Me", handle_click)

button.set_style(key, value)
# Set button style
# Example: button.set_style("background", "#007bff")
```

### Input

```mythos
ui.input(type, placeholder, value)
# Create input field
# Example: ui.input("text", "Enter name", "")
# Example: ui.input("email", "Email address", "")
# Example: ui.input("password", "Password", "")

input.set_prop(key, value)
# Set property
# Example: input.set_prop("required", true)
```

### Layout Containers

```mythos
ui.container()
# Create div container
# Example: container = ui.container()

ui.row()
# Horizontal layout
# Example: row = ui.row()

ui.column()
# Vertical layout
# Example: col = ui.column()

ui.grid(columns, gap)
# Grid layout
# Example: grid = ui.grid(3, "10px")

container.add_child(element)
# Add child element
# Example: container.add_child(ui.text("Hello"))
```

### Other Components

```mythos
ui.image(src, alt)
# Create image
# Example: ui.image("/logo.png", "Logo")

ui.link(href, text)
# Create link
# Example: ui.link("/about", "About Us")

ui.list(items, ordered)
# Create list
# Example: ui.list(["Item 1", "Item 2"], false)

ui.card(title, content)
# Create card
# Example: ui.card("Welcome", "This is a card")
```

### Styling

```mythos
element.set_style(property, value)
# Set CSS style
# Example: element.set_style("color", "blue")
# Example: element.set_style("font-size", "20px")
# Example: element.set_style("margin", "10px")

element.set_prop(property, value)
# Set HTML property
# Example: element.set_prop("id", "main")
# Example: element.set_prop("class", "container")
```

### Events

```mythos
element.on(event, handler)
# Add event handler
# Example: button.on("click", handle_click)
# Example: input.on("change", handle_change)

# Available events:
# - click
# - change
# - submit
# - focus
# - blur
# - keypress
# - keydown
# - keyup
# - mouseenter
# - mouseleave
```


---

## Game Engine

### Scene Management

```mythos
scene name { ... }
# Define scene
# Example:
# scene main {
#   cube position:(0, 0, 0)
#   camera position:(0, 5, 10)
# }

scene.create_cube(name, position, size, color)
# Create cube entity
# Example: cube = scene.create_cube("Player", Vector3(0, 0, 0), 1.0, Color.from_hex("#FF0000"))

scene.create_sphere(name, position, radius, color)
# Create sphere entity
# Example: sphere = scene.create_sphere("Ball", Vector3(5, 0, 0), 0.5)

scene.create_plane(name, position, width, height, color)
# Create plane entity
# Example: plane = scene.create_plane("Ground", Vector3(0, 0, 0), 100, 100)

scene.create_camera(name, position, target)
# Create camera
# Example: cam = scene.create_camera("MainCam", Vector3(0, 5, 10), Vector3(0, 0, 0))

scene.create_light(name, type, position, color, intensity)
# Create light
# Example: light = scene.create_light("Sun", "directional", Vector3(0, 10, 0), Color(1, 1, 1), 1.0)

scene.find_entity(name)
# Find entity by name
# Example: player = scene.find_entity("Player")

scene.update(delta_time)
# Update scene
# Example: scene.update(0.016)
```

### Entity Properties

```mythos
entity.position
# Entity position (Vector3)
# Example: entity.position = Vector3(10, 0, 5)

entity.rotation
# Entity rotation (Vector3, Euler angles)
# Example: entity.rotation = Vector3(0, 45, 0)

entity.scale
# Entity scale (Vector3)
# Example: entity.scale = Vector3(2, 2, 2)

entity.visible
# Visibility flag
# Example: entity.visible = false

entity.active
# Active flag
# Example: entity.active = true

entity.add_child(child)
# Add child entity
# Example: entity.add_child(weapon)

entity.remove_child(child)
# Remove child entity

entity.add_component(name, component)
# Add component
# Example: entity.add_component("health", {value: 100})

entity.get_component(name)
# Get component
# Example: health = entity.get_component("health")
```

### Camera

```mythos
camera.position
# Camera position
# Example: camera.position = Vector3(0, 10, 20)

camera.target
# Look-at target
# Example: camera.target = Vector3(0, 0, 0)

camera.fov
# Field of view (degrees)
# Example: camera.fov = 60

camera.look_at(target)
# Point camera at target
# Example: camera.look_at(player.position)

camera.forward()
# Get forward direction
# Example: dir = camera.forward()

camera.right()
# Get right direction

camera.move_forward(distance)
# Move camera forward
# Example: camera.move_forward(5)

camera.move_right(distance)
# Move camera right

camera.rotate(yaw, pitch)
# Rotate camera
# Example: camera.rotate(10, 5)
```

### Lighting

```mythos
light.type
# Light type: "point", "directional", "spot", "ambient"
# Example: light.type = "directional"

light.color
# Light color
# Example: light.color = Color(1, 0.8, 0.6)

light.intensity
# Light intensity
# Example: light.intensity = 1.5

light.position
# Light position (for point/spot)
# Example: light.position = Vector3(0, 10, 0)

light.direction
# Light direction (for directional/spot)
# Example: light.direction = Vector3(0, -1, 0)

light.range
# Light range (for point/spot)
# Example: light.range = 20

light.angle
# Spot light angle (degrees)
# Example: light.angle = 45
```

### Materials

```mythos
material.color
# Material color
# Example: material.color = Color(1, 0, 0)

material.metallic
# Metallic value (0-1)
# Example: material.metallic = 0.8

material.roughness
# Roughness value (0-1)
# Example: material.roughness = 0.3

material.emissive
# Emissive color
# Example: material.emissive = Color(1, 1, 0)

material.set_texture(path)
# Set texture
# Example: material.set_texture("textures/wood.png")
```

### 2D Sprites

```mythos
sprite.texture
# Sprite texture
# Example: sprite.texture = Texture.load("player.png")

sprite.position
# Sprite position (Vector2)
# Example: sprite.position = Vector2(100, 200)

sprite.size
# Sprite size (Vector2)
# Example: sprite.size = Vector2(32, 32)

sprite.rotation
# Sprite rotation (degrees)
# Example: sprite.rotation = 45

sprite.scale
# Sprite scale (Vector2)
# Example: sprite.scale = Vector2(2, 2)

sprite.color
# Sprite tint color
# Example: sprite.color = Color(1, 0.5, 0.5)

sprite.visible
# Visibility flag
# Example: sprite.visible = true

sprite.flip_x, sprite.flip_y
# Flip flags
# Example: sprite.flip_x = true

sprite.layer
# Z-order layer
# Example: sprite.layer = 10
```

### Animation

```mythos
animation.play()
# Play animation
# Example: animation.play()

animation.stop()
# Stop animation

animation.pause()
# Pause animation

animation.resume()
# Resume animation

animation.loop
# Loop flag
# Example: animation.loop = true

animated_sprite.add_animation(animation)
# Add animation
# Example: sprite.add_animation(walk_animation)

animated_sprite.play_animation(name)
# Play animation by name
# Example: sprite.play_animation("walk")
```

### Input

```mythos
input.key_pressed(key)
# Check if key is pressed
# Example: if input.key_pressed("w") { move_forward() }

input.key_down(key)
# Check if key was just pressed

input.key_up(key)
# Check if key was just released

input.mouse_button_pressed(button)
# Check if mouse button is pressed
# Example: if input.mouse_button_pressed("left") { shoot() }

input.mouse_position()
# Get mouse position
# Example: pos = input.mouse_position()

input.mouse_delta()
# Get mouse movement delta
# Example: delta = input.mouse_delta()

input.lock_mouse()
# Lock mouse cursor (for FPS games)

input.unlock_mouse()
# Unlock mouse cursor
```

### Game Loop

```mythos
function update(dt) { ... }
# Update function called every frame
# dt = delta time in seconds
# Example:
# function update(dt) {
#   player.position.x += speed * dt
# }

game.start()
# Start game loop
# Example: game.start()

game.stop()
# Stop game loop

game.pause()
# Pause game

game.resume()
# Resume game
```

### Collision Detection

```mythos
collides(entity1, entity2)
# Check collision between entities
# Example: if collides(player, enemy) { game_over() }

physics.raycast(ray, max_distance)
# Cast ray and check for hits
# Example: hit = physics.raycast(Ray(pos, dir), 100)

hit.object
# Hit object

hit.point
# Hit point (Vector3)

hit.distance
# Hit distance
```


---

## AI Functions

### Behavior Trees

```mythos
BehaviorTree(root)
# Create behavior tree
# Example: tree = BehaviorTree(root_node)

tree.tick(context)
# Execute tree
# Example: tree.tick(enemy_data)

tree.reset()
# Reset tree state

# Node Types:

ActionNode(name, action_function)
# Action node
# Example: ActionNode("Attack", attack_enemy)

ConditionNode(name, condition_function)
# Condition node
# Example: ConditionNode("Enemy Visible", check_enemy)

SequenceNode(name)
# Sequence node (AND logic)
# Example: seq = SequenceNode("Combat Sequence")

SelectorNode(name)
# Selector node (OR logic)
# Example: sel = SelectorNode("Choose Action")

ParallelNode(name, success_threshold)
# Parallel node
# Example: par = ParallelNode("Multi-task", 2)

InverterNode(name, child)
# Inverter decorator
# Example: inv = InverterNode("Not", condition)

RepeaterNode(name, count, child)
# Repeater decorator
# Example: rep = RepeaterNode("Repeat 5x", 5, action)
```

### Behavior Tree Builder

```mythos
builder = BehaviorTreeBuilder()

builder.sequence(name)
# Start sequence
# Example: builder.sequence("Main")

builder.selector(name)
# Start selector
# Example: builder.selector("Choose")

builder.parallel(name, threshold)
# Start parallel
# Example: builder.parallel("Multi", 2)

builder.action(name, function)
# Add action
# Example: builder.action("Move", move_to_target)

builder.condition(name, function)
# Add condition
# Example: builder.condition("Can See", check_visibility)

builder.inverter(name)
# Start inverter
# Example: builder.inverter("Not")

builder.repeater(name, count)
# Start repeater
# Example: builder.repeater("Loop", 3)

builder.end()
# End current node
# Example: builder.end()

builder.build()
# Build tree
# Example: tree = builder.build()
```

### Pathfinding

```mythos
Grid(width, height)
# Create pathfinding grid
# Example: grid = Grid(100, 100)

grid.add_obstacle(x, y)
# Add obstacle
# Example: grid.add_obstacle(10, 20)

grid.remove_obstacle(x, y)
# Remove obstacle

grid.set_weight(x, y, weight)
# Set movement cost
# Example: grid.set_weight(5, 5, 2.0)

grid.is_walkable(x, y)
# Check if walkable
# Example: if grid.is_walkable(x, y) { ... }

grid.get_neighbors(x, y, diagonal)
# Get neighbors
# Example: neighbors = grid.get_neighbors(10, 10, true)
```

### Pathfinding Algorithms

```mythos
astar(grid, start, goal, heuristic, diagonal)
# A* pathfinding
# Returns: path or null
# Example: path = astar(grid, (0, 0), (10, 10))

dijkstra(grid, start, goal, diagonal)
# Dijkstra's algorithm
# Example: path = dijkstra(grid, start, goal)

breadth_first_search(grid, start, goal, diagonal)
# BFS pathfinding
# Example: path = breadth_first_search(grid, start, goal)

find_path(grid, start, goal, algorithm, smooth)
# Unified pathfinding
# algorithm: "astar", "dijkstra", "bfs"
# Example: path = find_path(grid, start, goal, "astar", true)

smooth_path(path, grid)
# Smooth path
# Example: smooth = smooth_path(path, grid)

has_line_of_sight(pos1, pos2, grid)
# Check line of sight
# Example: visible = has_line_of_sight(start, end, grid)
```

### Heuristics

```mythos
heuristic_manhattan(pos1, pos2)
# Manhattan distance
# Example: dist = heuristic_manhattan((0, 0), (3, 4)) → 7

heuristic_euclidean(pos1, pos2)
# Euclidean distance
# Example: dist = heuristic_euclidean((0, 0), (3, 4)) → 5

heuristic_diagonal(pos1, pos2)
# Diagonal distance (Chebyshev)
# Example: dist = heuristic_diagonal((0, 0), (3, 4)) → 4
```

### NavMesh (3D)

```mythos
NavMesh()
# Create navigation mesh
# Example: navmesh = NavMesh()

navmesh.add_polygon(vertices)
# Add polygon
# Example: navmesh.add_polygon([v1, v2, v3])

navmesh.connect_polygons(poly1, poly2)
# Connect polygons
# Example: navmesh.connect_polygons(0, 1)

navmesh.find_path_3d(start, goal)
# Find 3D path
# Example: path = navmesh.find_path_3d(start_pos, goal_pos)
```


---

## File I/O

### File Operations

```mythos
file.read(path)
# Read file contents
# Example: content = file.read("data.txt")

file.write(path, content)
# Write to file
# Example: file.write("output.txt", "Hello World")

file.append(path, content)
# Append to file
# Example: file.append("log.txt", "New entry\n")

file.exists(path)
# Check if file exists
# Example: if file.exists("config.json") { ... }

file.delete(path)
# Delete file
# Example: file.delete("temp.txt")

file.copy(source, destination)
# Copy file
# Example: file.copy("data.txt", "backup.txt")

file.move(source, destination)
# Move/rename file
# Example: file.move("old.txt", "new.txt")
```

### Directory Operations

```mythos
dir.create(path)
# Create directory
# Example: dir.create("output")

dir.exists(path)
# Check if directory exists
# Example: if dir.exists("data") { ... }

dir.list(path)
# List directory contents
# Example: files = dir.list(".")

dir.delete(path)
# Delete directory
# Example: dir.delete("temp")
```

### JSON

```mythos
json.parse(string)
# Parse JSON string
# Example: data = json.parse('{"name": "Mythos"}')

json.stringify(object)
# Convert to JSON string
# Example: str = json.stringify({name: "Mythos", version: 1})

json.load(path)
# Load JSON from file
# Example: config = json.load("config.json")

json.save(path, object)
# Save JSON to file
# Example: json.save("data.json", {users: []})
```


---

## CLI Commands

### Running Programs

```bash
mythos run <file>
# Run a Mythos file
# Example: mythos run hello.mythos

mythos run <file> --debug
# Run with debug output
# Example: mythos run app.mythos --debug
```

### Building

```bash
mythos build <file>
# Compile to bytecode
# Example: mythos build app.mythos

mythos build <file> -o <output>
# Specify output file
# Example: mythos build app.mythos -o app.mythosb
```

### Web Server

```bash
mythos web <file>
# Start web server
# Example: mythos web app.mythos

mythos web <file> --port <port>
# Specify port
# Example: mythos web app.mythos --port 3000

mythos web <file> --host <host> --port <port>
# Specify host and port
# Example: mythos web app.mythos --host 0.0.0.0 --port 8080
```

### Game

```bash
mythos game <file>
# Run game
# Example: mythos game mygame.mythos

mythos game <file> --fullscreen
# Run in fullscreen
# Example: mythos game mygame.mythos --fullscreen
```

### REPL

```bash
mythos repl
# Start interactive shell
# Example: mythos repl

# In REPL:
>>> x = 10
>>> print(x * 2)
20
>>> exit
```

### Project Initialization

```bash
mythos init <name>
# Create new project
# Example: mythos init my-project

mythos init <name> --type <type>
# Specify project type: web, game, cli
# Example: mythos init my-game --type game
```

### Version & Help

```bash
mythos --version
# Show version
# Example: mythos --version

mythos --help
# Show help
# Example: mythos --help

mythos <command> --help
# Show command help
# Example: mythos run --help
```

---

## Quick Reference Tables

### Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `+` | Addition | `5 + 3 → 8` |
| `-` | Subtraction | `5 - 3 → 2` |
| `*` | Multiplication | `5 * 3 → 15` |
| `/` | Division | `6 / 3 → 2` |
| `^` | Power | `2 ^ 3 → 8` |
| `%` | Modulo | `7 % 3 → 1` |
| `==` | Equal | `5 == 5 → true` |
| `!=` | Not equal | `5 != 3 → true` |
| `<` | Less than | `3 < 5 → true` |
| `>` | Greater than | `5 > 3 → true` |
| `<=` | Less or equal | `3 <= 3 → true` |
| `>=` | Greater or equal | `5 >= 5 → true` |
| `and` | Logical AND | `true and false → false` |
| `or` | Logical OR | `true or false → true` |
| `not` | Logical NOT | `not true → false` |

### Keywords

| Keyword | Purpose | Example |
|---------|---------|---------|
| `if` | Conditional | `if x > 0 { ... }` |
| `else` | Alternative | `else { ... }` |
| `elif` | Else if | `elif x < 0 { ... }` |
| `while` | Loop | `while x < 10 { ... }` |
| `for` | For loop | `for i in range(10) { ... }` |
| `in` | Membership | `for item in array { ... }` |
| `function` | Define function | `function add(a, b) { ... }` |
| `return` | Return value | `return a + b` |
| `class` | Define class | `class Player { ... }` |
| `new` | Create instance | `new Player()` |
| `this` | Current instance | `this.health = 100` |
| `import` | Import module | `import math` |
| `from` | Import from | `from math import sin` |
| `break` | Exit loop | `break` |
| `continue` | Skip iteration | `continue` |
| `true` | Boolean true | `x = true` |
| `false` | Boolean false | `x = false` |
| `null` | Null value | `x = null` |

### Data Types

| Type | Example | Description |
|------|---------|-------------|
| Number | `42`, `3.14` | Integer or float |
| String | `"hello"`, `'world'` | Text |
| Boolean | `true`, `false` | True or false |
| Null | `null` | No value |
| Array | `[1, 2, 3]` | Ordered list |
| Object | `{name: "Alice"}` | Key-value pairs |
| Vector2 | `Vector2(10, 20)` | 2D vector |
| Vector3 | `Vector3(1, 2, 3)` | 3D vector |
| Matrix4 | `Matrix4()` | 4x4 matrix |
| Color | `Color(1, 0, 0)` | RGBA color |

---

## Examples

### Hello World
```mythos
print("Hello, Mythos!")
```

### Variables & Math
```mythos
x = 10
y = 20
sum = x + y
print("Sum:", sum)
```

### Functions
```mythos
function greet(name) {
  return "Hello, " + name + "!"
}
print(greet("World"))
```

### Arrays
```mythos
numbers = [1, 2, 3, 4, 5]
for num in numbers {
  print(num * 2)
}
```

### Web App
```mythos
web.app {
  route "/" {
    page = ui.page("Home")
    page.add(ui.text("Welcome!", "h1"))
    return page.render()
  }
}
web.start()
```

### 3D Scene
```mythos
scene main {
  cube position:(0, 0, 0) color:#FF0000
  camera position:(0, 5, 10)
  light sun type:directional
}
game.start()
```

### Pathfinding
```mythos
grid = Grid(50, 50)
grid.add_obstacle(10, 10)
path = find_path(grid, (0, 0), (20, 20), "astar")
print("Path:", path)
```

---

**For more examples, see the `examples/` directory.**

**For detailed documentation, see `docs/language-reference.md`.**
