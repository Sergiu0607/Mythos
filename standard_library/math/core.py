"""
Mythos Math Standard Library - Core mathematical functions
"""
import math
import cmath
from typing import Union, List, Tuple

class Vector2:
    """2D Vector class"""
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y
    
    def __add__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: float) -> 'Vector2':
        return Vector2(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar: float) -> 'Vector2':
        return Vector2(self.x / scalar, self.y / scalar)
    
    def dot(self, other: 'Vector2') -> float:
        """Dot product"""
        return self.x * other.x + self.y * other.y
    
    def length(self) -> float:
        """Vector magnitude"""
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def normalize(self) -> 'Vector2':
        """Return normalized vector"""
        length = self.length()
        if length == 0:
            return Vector2(0, 0)
        return Vector2(self.x / length, self.y / length)
    
    def distance_to(self, other: 'Vector2') -> float:
        """Distance to another vector"""
        return (self - other).length()
    
    def angle(self) -> float:
        """Angle in radians"""
        return math.atan2(self.y, self.x)
    
    def rotate(self, angle: float) -> 'Vector2':
        """Rotate by angle in radians"""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return Vector2(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a
        )
    
    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"

class Vector3:
    """3D Vector class"""
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar: float) -> 'Vector3':
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __truediv__(self, scalar: float) -> 'Vector3':
        return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)
    
    def dot(self, other: 'Vector3') -> float:
        """Dot product"""
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other: 'Vector3') -> 'Vector3':
        """Cross product"""
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    def length(self) -> float:
        """Vector magnitude"""
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
    
    def normalize(self) -> 'Vector3':
        """Return normalized vector"""
        length = self.length()
        if length == 0:
            return Vector3(0, 0, 0)
        return Vector3(self.x / length, self.y / length, self.z / length)
    
    def distance_to(self, other: 'Vector3') -> float:
        """Distance to another vector"""
        return (self - other).length()
    
    def __repr__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"

class Matrix4:
    """4x4 Matrix for 3D transformations"""
    def __init__(self, elements: List[float] = None):
        if elements is None:
            # Identity matrix
            self.elements = [
                1, 0, 0, 0,
                0, 1, 0, 0,
                0, 0, 1, 0,
                0, 0, 0, 1
            ]
        else:
            self.elements = elements
    
    def multiply(self, other: 'Matrix4') -> 'Matrix4':
        """Matrix multiplication"""
        result = [0] * 16
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    result[i * 4 + j] += self.elements[i * 4 + k] * other.elements[k * 4 + j]
        return Matrix4(result)
    
    def translate(self, x: float, y: float, z: float) -> 'Matrix4':
        """Create translation matrix"""
        return Matrix4([
            1, 0, 0, x,
            0, 1, 0, y,
            0, 0, 1, z,
            0, 0, 0, 1
        ])
    
    def scale(self, x: float, y: float, z: float) -> 'Matrix4':
        """Create scale matrix"""
        return Matrix4([
            x, 0, 0, 0,
            0, y, 0, 0,
            0, 0, z, 0,
            0, 0, 0, 1
        ])
    
    def rotate_x(self, angle: float) -> 'Matrix4':
        """Rotate around X axis"""
        c = math.cos(angle)
        s = math.sin(angle)
        return Matrix4([
            1, 0, 0, 0,
            0, c, -s, 0,
            0, s, c, 0,
            0, 0, 0, 1
        ])
    
    def rotate_y(self, angle: float) -> 'Matrix4':
        """Rotate around Y axis"""
        c = math.cos(angle)
        s = math.sin(angle)
        return Matrix4([
            c, 0, s, 0,
            0, 1, 0, 0,
            -s, 0, c, 0,
            0, 0, 0, 1
        ])
    
    def rotate_z(self, angle: float) -> 'Matrix4':
        """Rotate around Z axis"""
        c = math.cos(angle)
        s = math.sin(angle)
        return Matrix4([
            c, -s, 0, 0,
            s, c, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1
        ])

# Trigonometric functions
def sin(x: float) -> float:
    return math.sin(x)

def cos(x: float) -> float:
    return math.cos(x)

def tan(x: float) -> float:
    return math.tan(x)

def asin(x: float) -> float:
    return math.asin(x)

def acos(x: float) -> float:
    return math.acos(x)

def atan(x: float) -> float:
    return math.atan(x)

def atan2(y: float, x: float) -> float:
    return math.atan2(y, x)

# Exponential and logarithmic
def exp(x: float) -> float:
    return math.exp(x)

def log(x: float, base: float = math.e) -> float:
    return math.log(x, base)

def log10(x: float) -> float:
    return math.log10(x)

def log2(x: float) -> float:
    return math.log2(x)

# Power and roots
def sqrt(x: float) -> float:
    return math.sqrt(x)

def pow(x: float, y: float) -> float:
    return x ** y

def cbrt(x: float) -> float:
    """Cube root"""
    return x ** (1/3)

# Rounding
def floor(x: float) -> int:
    return math.floor(x)

def ceil(x: float) -> int:
    return math.ceil(x)

def round_num(x: float, decimals: int = 0) -> float:
    return round(x, decimals)

def trunc(x: float) -> int:
    return math.trunc(x)

# Absolute and sign
def abs_val(x: float) -> float:
    return abs(x)

def sign(x: float) -> int:
    """Return -1, 0, or 1"""
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0

# Min/Max
def min_val(*args) -> float:
    return min(args)

def max_val(*args) -> float:
    return max(args)

def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp value between min and max"""
    return max(min_val, min(max_val, value))

# Linear interpolation
def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation between a and b"""
    return a + (b - a) * t

# Random numbers
import random

def random_float(min_val: float = 0, max_val: float = 1) -> float:
    """Random float between min and max"""
    return random.uniform(min_val, max_val)

def random_int(min_val: int, max_val: int) -> int:
    """Random integer between min and max (inclusive)"""
    return random.randint(min_val, max_val)

# Constants
PI = math.pi
E = math.e
TAU = math.tau
INF = math.inf
NAN = math.nan
