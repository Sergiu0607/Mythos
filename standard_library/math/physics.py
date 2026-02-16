"""
Mythos Physics Library - Physics calculations and simulations
"""
import math
from typing import Tuple, List
from standard_library.math.core import Vector2, Vector3

class PhysicsBody2D:
    """2D Physics body with position, velocity, and acceleration"""
    def __init__(self, position: Vector2 = None, mass: float = 1.0):
        self.position = position or Vector2(0, 0)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.mass = mass
        self.forces = []
    
    def apply_force(self, force: Vector2):
        """Apply a force to the body"""
        self.forces.append(force)
    
    def update(self, dt: float):
        """Update physics simulation"""
        # Calculate net force
        net_force = Vector2(0, 0)
        for force in self.forces:
            net_force = net_force + force
        
        # F = ma, so a = F/m
        self.acceleration = net_force / self.mass if self.mass > 0 else Vector2(0, 0)
        
        # Update velocity and position
        self.velocity = self.velocity + self.acceleration * dt
        self.position = self.position + self.velocity * dt
        
        # Clear forces
        self.forces = []

class PhysicsBody3D:
    """3D Physics body with position, velocity, and acceleration"""
    def __init__(self, position: Vector3 = None, mass: float = 1.0):
        self.position = position or Vector3(0, 0, 0)
        self.velocity = Vector3(0, 0, 0)
        self.acceleration = Vector3(0, 0, 0)
        self.mass = mass
        self.forces = []
    
    def apply_force(self, force: Vector3):
        """Apply a force to the body"""
        self.forces.append(force)
    
    def update(self, dt: float):
        """Update physics simulation"""
        # Calculate net force
        net_force = Vector3(0, 0, 0)
        for force in self.forces:
            net_force = net_force + force
        
        # F = ma, so a = F/m
        self.acceleration = net_force / self.mass if self.mass > 0 else Vector3(0, 0, 0)
        
        # Update velocity and position
        self.velocity = self.velocity + self.acceleration * dt
        self.position = self.position + self.velocity * dt
        
        # Clear forces
        self.forces = []

# Physics constants
GRAVITY_EARTH = 9.81  # m/s^2
SPEED_OF_LIGHT = 299792458  # m/s
PLANCK_CONSTANT = 6.62607015e-34  # J⋅s
BOLTZMANN_CONSTANT = 1.380649e-23  # J/K

# Kinematics
def velocity(distance: float, time: float) -> float:
    """Calculate velocity: v = d/t"""
    return distance / time if time != 0 else 0

def acceleration(velocity_change: float, time: float) -> float:
    """Calculate acceleration: a = Δv/t"""
    return velocity_change / time if time != 0 else 0

def distance_with_constant_acceleration(initial_velocity: float, acceleration: float, time: float) -> float:
    """Calculate distance: d = v₀t + ½at²"""
    return initial_velocity * time + 0.5 * acceleration * time ** 2

def final_velocity(initial_velocity: float, acceleration: float, time: float) -> float:
    """Calculate final velocity: v = v₀ + at"""
    return initial_velocity + acceleration * time

def projectile_motion(initial_velocity: float, angle: float, gravity: float = GRAVITY_EARTH) -> Tuple[float, float, float]:
    """
    Calculate projectile motion
    Returns: (max_height, range, time_of_flight)
    """
    angle_rad = math.radians(angle)
    vx = initial_velocity * math.cos(angle_rad)
    vy = initial_velocity * math.sin(angle_rad)
    
    time_of_flight = 2 * vy / gravity
    max_height = (vy ** 2) / (2 * gravity)
    range_distance = vx * time_of_flight
    
    return max_height, range_distance, time_of_flight

# Dynamics
def force(mass: float, acceleration: float) -> float:
    """Newton's second law: F = ma"""
    return mass * acceleration

def momentum(mass: float, velocity: float) -> float:
    """Calculate momentum: p = mv"""
    return mass * velocity

def kinetic_energy(mass: float, velocity: float) -> float:
    """Calculate kinetic energy: KE = ½mv²"""
    return 0.5 * mass * velocity ** 2

def potential_energy(mass: float, height: float, gravity: float = GRAVITY_EARTH) -> float:
    """Calculate gravitational potential energy: PE = mgh"""
    return mass * gravity * height

def work(force: float, distance: float, angle: float = 0) -> float:
    """Calculate work: W = Fd cos(θ)"""
    return force * distance * math.cos(math.radians(angle))

def power(work: float, time: float) -> float:
    """Calculate power: P = W/t"""
    return work / time if time != 0 else 0

# Collisions
def elastic_collision_1d(m1: float, v1: float, m2: float, v2: float) -> Tuple[float, float]:
    """
    Calculate velocities after elastic collision in 1D
    Returns: (v1_final, v2_final)
    """
    v1_final = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
    v2_final = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)
    return v1_final, v2_final

def inelastic_collision_1d(m1: float, v1: float, m2: float, v2: float) -> float:
    """
    Calculate final velocity after perfectly inelastic collision
    Returns: v_final
    """
    return (m1 * v1 + m2 * v2) / (m1 + m2)

# Circular motion
def centripetal_acceleration(velocity: float, radius: float) -> float:
    """Calculate centripetal acceleration: a = v²/r"""
    return velocity ** 2 / radius if radius != 0 else 0

def centripetal_force(mass: float, velocity: float, radius: float) -> float:
    """Calculate centripetal force: F = mv²/r"""
    return mass * velocity ** 2 / radius if radius != 0 else 0

def angular_velocity(linear_velocity: float, radius: float) -> float:
    """Calculate angular velocity: ω = v/r"""
    return linear_velocity / radius if radius != 0 else 0

# Gravity
def gravitational_force(m1: float, m2: float, distance: float) -> float:
    """
    Calculate gravitational force between two masses
    F = G(m1*m2)/r²
    """
    G = 6.67430e-11  # Gravitational constant
    return G * m1 * m2 / (distance ** 2) if distance != 0 else 0

def escape_velocity(mass: float, radius: float) -> float:
    """Calculate escape velocity from a celestial body"""
    G = 6.67430e-11
    return math.sqrt(2 * G * mass / radius) if radius != 0 else 0

# Waves
def wave_speed(frequency: float, wavelength: float) -> float:
    """Calculate wave speed: v = fλ"""
    return frequency * wavelength

def doppler_effect(source_frequency: float, source_velocity: float, observer_velocity: float, wave_speed: float) -> float:
    """
    Calculate observed frequency due to Doppler effect
    Positive velocity = moving towards each other
    """
    return source_frequency * (wave_speed + observer_velocity) / (wave_speed - source_velocity)

# Thermodynamics
def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit"""
    return celsius * 9/5 + 32

def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert Fahrenheit to Celsius"""
    return (fahrenheit - 32) * 5/9

def celsius_to_kelvin(celsius: float) -> float:
    """Convert Celsius to Kelvin"""
    return celsius + 273.15

def kelvin_to_celsius(kelvin: float) -> float:
    """Convert Kelvin to Celsius"""
    return kelvin - 273.15

def ideal_gas_law(pressure: float = None, volume: float = None, n: float = None, temperature: float = None) -> float:
    """
    Ideal gas law: PV = nRT
    Provide 3 values to calculate the 4th
    """
    R = 8.314  # Gas constant J/(mol⋅K)
    
    if pressure is None:
        return n * R * temperature / volume
    elif volume is None:
        return n * R * temperature / pressure
    elif n is None:
        return pressure * volume / (R * temperature)
    elif temperature is None:
        return pressure * volume / (n * R)
