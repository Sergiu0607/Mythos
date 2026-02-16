"""
Mythos AI - Pathfinding algorithms
"""
from typing import List, Tuple, Set, Dict, Optional, Callable
from dataclasses import dataclass
import heapq
from standard_library.math.core import Vector2, Vector3

@dataclass
class Node:
    """Node in a pathfinding graph"""
    position: Tuple[int, int]
    g_cost: float = float('inf')  # Cost from start
    h_cost: float = 0  # Heuristic cost to goal
    parent: Optional['Node'] = None
    
    @property
    def f_cost(self) -> float:
        """Total cost (g + h)"""
        return self.g_cost + self.h_cost
    
    def __lt__(self, other):
        return self.f_cost < other.f_cost
    
    def __eq__(self, other):
        return self.position == other.position
    
    def __hash__(self):
        return hash(self.position)

class Grid:
    """2D grid for pathfinding"""
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.obstacles: Set[Tuple[int, int]] = set()
        self.weights: Dict[Tuple[int, int], float] = {}
    
    def add_obstacle(self, x: int, y: int):
        """Add an obstacle at position"""
        self.obstacles.add((x, y))
    
    def remove_obstacle(self, x: int, y: int):
        """Remove obstacle at position"""
        self.obstacles.discard((x, y))
    
    def set_weight(self, x: int, y: int, weight: float):
        """Set movement cost weight for a cell"""
        self.weights[(x, y)] = weight
    
    def is_walkable(self, x: int, y: int) -> bool:
        """Check if position is walkable"""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return (x, y) not in self.obstacles
    
    def get_weight(self, x: int, y: int) -> float:
        """Get movement cost weight for a cell"""
        return self.weights.get((x, y), 1.0)
    
    def get_neighbors(self, x: int, y: int, diagonal: bool = True) -> List[Tuple[int, int]]:
        """Get walkable neighbors of a position"""
        neighbors = []
        
        # Cardinal directions
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        # Add diagonal directions
        if diagonal:
            directions.extend([(1, 1), (1, -1), (-1, 1), (-1, -1)])
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.is_walkable(nx, ny):
                neighbors.append((nx, ny))
        
        return neighbors

def heuristic_manhattan(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
    """Manhattan distance heuristic"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def heuristic_euclidean(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
    """Euclidean distance heuristic"""
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    return (dx * dx + dy * dy) ** 0.5

def heuristic_diagonal(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
    """Diagonal distance heuristic (Chebyshev)"""
    dx = abs(pos1[0] - pos2[0])
    dy = abs(pos1[1] - pos2[1])
    return max(dx, dy)

def astar(grid: Grid, start: Tuple[int, int], goal: Tuple[int, int], 
          heuristic: Callable = heuristic_euclidean, diagonal: bool = True) -> Optional[List[Tuple[int, int]]]:
    """
    A* pathfinding algorithm
    Returns path from start to goal, or None if no path exists
    """
    if not grid.is_walkable(*start) or not grid.is_walkable(*goal):
        return None
    
    # Initialize
    open_set = []
    closed_set: Set[Tuple[int, int]] = set()
    nodes: Dict[Tuple[int, int], Node] = {}
    
    start_node = Node(start, g_cost=0, h_cost=heuristic(start, goal))
    nodes[start] = start_node
    heapq.heappush(open_set, start_node)
    
    while open_set:
        current = heapq.heappop(open_set)
        
        if current.position == goal:
            # Reconstruct path
            path = []
            node = current
            while node:
                path.append(node.position)
                node = node.parent
            return list(reversed(path))
        
        closed_set.add(current.position)
        
        # Check neighbors
        for neighbor_pos in grid.get_neighbors(*current.position, diagonal):
            if neighbor_pos in closed_set:
                continue
            
            # Calculate cost
            dx = abs(neighbor_pos[0] - current.position[0])
            dy = abs(neighbor_pos[1] - current.position[1])
            move_cost = 1.414 if (dx + dy) == 2 else 1.0  # Diagonal vs cardinal
            move_cost *= grid.get_weight(*neighbor_pos)
            
            tentative_g = current.g_cost + move_cost
            
            if neighbor_pos not in nodes:
                nodes[neighbor_pos] = Node(neighbor_pos)
            
            neighbor = nodes[neighbor_pos]
            
            if tentative_g < neighbor.g_cost:
                neighbor.parent = current
                neighbor.g_cost = tentative_g
                neighbor.h_cost = heuristic(neighbor_pos, goal)
                
                if neighbor not in open_set:
                    heapq.heappush(open_set, neighbor)
    
    return None  # No path found

def dijkstra(grid: Grid, start: Tuple[int, int], goal: Tuple[int, int], 
             diagonal: bool = True) -> Optional[List[Tuple[int, int]]]:
    """
    Dijkstra's algorithm (A* with zero heuristic)
    """
    return astar(grid, start, goal, lambda p1, p2: 0, diagonal)

def breadth_first_search(grid: Grid, start: Tuple[int, int], goal: Tuple[int, int], 
                         diagonal: bool = False) -> Optional[List[Tuple[int, int]]]:
    """
    Breadth-First Search pathfinding
    Finds shortest path in terms of number of steps (unweighted)
    """
    if not grid.is_walkable(*start) or not grid.is_walkable(*goal):
        return None
    
    from collections import deque
    
    queue = deque([start])
    visited: Set[Tuple[int, int]] = {start}
    parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}
    
    while queue:
        current = queue.popleft()
        
        if current == goal:
            # Reconstruct path
            path = []
            pos = goal
            while pos is not None:
                path.append(pos)
                pos = parent[pos]
            return list(reversed(path))
        
        for neighbor in grid.get_neighbors(*current, diagonal):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
    
    return None  # No path found

def smooth_path(path: List[Tuple[int, int]], grid: Grid) -> List[Tuple[int, int]]:
    """
    Smooth a path by removing unnecessary waypoints
    Uses line-of-sight checks
    """
    if len(path) <= 2:
        return path
    
    smoothed = [path[0]]
    current_idx = 0
    
    while current_idx < len(path) - 1:
        # Try to skip as many waypoints as possible
        for i in range(len(path) - 1, current_idx, -1):
            if has_line_of_sight(path[current_idx], path[i], grid):
                smoothed.append(path[i])
                current_idx = i
                break
        else:
            # Can't skip any, move to next
            current_idx += 1
            if current_idx < len(path):
                smoothed.append(path[current_idx])
    
    return smoothed

def has_line_of_sight(pos1: Tuple[int, int], pos2: Tuple[int, int], grid: Grid) -> bool:
    """
    Check if there's a clear line of sight between two positions
    Uses Bresenham's line algorithm
    """
    x0, y0 = pos1
    x1, y1 = pos2
    
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    
    while True:
        if not grid.is_walkable(x0, y0):
            return False
        
        if x0 == x1 and y0 == y1:
            return True
        
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

class NavMesh:
    """Navigation mesh for 3D pathfinding"""
    def __init__(self):
        self.polygons: List[List[Vector3]] = []
        self.connections: Dict[int, List[int]] = {}
    
    def add_polygon(self, vertices: List[Vector3]) -> int:
        """Add a polygon to the nav mesh"""
        poly_id = len(self.polygons)
        self.polygons.append(vertices)
        self.connections[poly_id] = []
        return poly_id
    
    def connect_polygons(self, poly1: int, poly2: int):
        """Connect two polygons"""
        if poly1 in self.connections:
            self.connections[poly1].append(poly2)
        if poly2 in self.connections:
            self.connections[poly2].append(poly1)
    
    def find_path_3d(self, start: Vector3, goal: Vector3) -> Optional[List[Vector3]]:
        """Find path in 3D space using nav mesh"""
        # Simplified implementation
        # Real implementation would use funnel algorithm
        return [start, goal]

def find_path(grid: Grid, start: Tuple[int, int], goal: Tuple[int, int], 
              algorithm: str = "astar", smooth: bool = True) -> Optional[List[Tuple[int, int]]]:
    """
    Unified pathfinding function
    
    Args:
        grid: Grid to search
        start: Start position
        goal: Goal position
        algorithm: "astar", "dijkstra", or "bfs"
        smooth: Whether to smooth the resulting path
    
    Returns:
        Path from start to goal, or None if no path exists
    """
    if algorithm == "astar":
        path = astar(grid, start, goal)
    elif algorithm == "dijkstra":
        path = dijkstra(grid, start, goal)
    elif algorithm == "bfs":
        path = breadth_first_search(grid, start, goal)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")
    
    if path and smooth:
        path = smooth_path(path, grid)
    
    return path
