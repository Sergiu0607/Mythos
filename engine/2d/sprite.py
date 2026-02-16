"""
Mythos 2D Engine - Sprite and animation system
"""
from typing import List, Dict, Optional, Tuple
from standard_library.math.core import Vector2
from engine.rendering.renderer import Color
import time

class Texture:
    """2D Texture"""
    def __init__(self, path: str, width: int = 0, height: int = 0):
        self.path = path
        self.width = width
        self.height = height
        self.data = None  # Would contain actual image data
    
    @staticmethod
    def load(path: str) -> 'Texture':
        """Load texture from file"""
        # Would use PIL or similar to load image
        return Texture(path, 64, 64)

class Sprite:
    """2D Sprite"""
    def __init__(self, texture: Texture = None):
        self.texture = texture
        self.position = Vector2(0, 0)
        self.size = Vector2(32, 32)
        self.rotation = 0.0
        self.scale = Vector2(1, 1)
        self.color = Color(1, 1, 1, 1)
        self.visible = True
        self.flip_x = False
        self.flip_y = False
        self.layer = 0  # Z-order
    
    def set_texture(self, texture: Texture):
        """Set sprite texture"""
        self.texture = texture
        if texture:
            self.size = Vector2(texture.width, texture.height)
    
    def get_bounds(self) -> Tuple[float, float, float, float]:
        """Get sprite bounding box (x, y, width, height)"""
        w = self.size.x * self.scale.x
        h = self.size.y * self.scale.y
        return (self.position.x, self.position.y, w, h)
    
    def contains_point(self, point: Vector2) -> bool:
        """Check if point is inside sprite"""
        x, y, w, h = self.get_bounds()
        return (x <= point.x <= x + w and y <= point.y <= y + h)

class Animation:
    """Sprite animation"""
    def __init__(self, name: str, frames: List[Texture], frame_duration: float = 0.1):
        self.name = name
        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = True
        self.current_frame = 0
        self.time_accumulator = 0.0
        self.playing = False
    
    def play(self):
        """Start playing animation"""
        self.playing = True
        self.current_frame = 0
        self.time_accumulator = 0.0
    
    def stop(self):
        """Stop animation"""
        self.playing = False
    
    def pause(self):
        """Pause animation"""
        self.playing = False
    
    def resume(self):
        """Resume animation"""
        self.playing = True
    
    def update(self, dt: float) -> Optional[Texture]:
        """Update animation and return current frame"""
        if not self.playing or not self.frames:
            return self.frames[self.current_frame] if self.frames else None
        
        self.time_accumulator += dt
        
        while self.time_accumulator >= self.frame_duration:
            self.time_accumulator -= self.frame_duration
            self.current_frame += 1
            
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.playing = False
        
        return self.frames[self.current_frame]

class AnimatedSprite(Sprite):
    """Sprite with animation support"""
    def __init__(self):
        super().__init__()
        self.animations: Dict[str, Animation] = {}
        self.current_animation: Optional[Animation] = None
    
    def add_animation(self, animation: Animation):
        """Add an animation"""
        self.animations[animation.name] = animation
    
    def play_animation(self, name: str):
        """Play an animation by name"""
        if name in self.animations:
            if self.current_animation:
                self.current_animation.stop()
            self.current_animation = self.animations[name]
            self.current_animation.play()
    
    def stop_animation(self):
        """Stop current animation"""
        if self.current_animation:
            self.current_animation.stop()
    
    def update(self, dt: float):
        """Update sprite animation"""
        if self.current_animation:
            frame = self.current_animation.update(dt)
            if frame:
                self.texture = frame

class SpriteSheet:
    """Sprite sheet for managing multiple sprites in one texture"""
    def __init__(self, texture: Texture, frame_width: int, frame_height: int):
        self.texture = texture
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frames: List[Tuple[int, int]] = []
        
        # Calculate frames
        cols = texture.width // frame_width
        rows = texture.height // frame_height
        
        for row in range(rows):
            for col in range(cols):
                self.frames.append((col * frame_width, row * frame_height))
    
    def get_frame(self, index: int) -> Tuple[int, int, int, int]:
        """Get frame coordinates (x, y, width, height)"""
        if 0 <= index < len(self.frames):
            x, y = self.frames[index]
            return (x, y, self.frame_width, self.frame_height)
        return (0, 0, self.frame_width, self.frame_height)
    
    def create_animation(self, name: str, frame_indices: List[int], frame_duration: float = 0.1) -> Animation:
        """Create animation from frame indices"""
        # In real implementation, would create sub-textures
        frames = [self.texture for _ in frame_indices]
        return Animation(name, frames, frame_duration)

class ParticleSystem:
    """2D Particle system"""
    def __init__(self, max_particles: int = 100):
        self.max_particles = max_particles
        self.particles: List['Particle'] = []
        self.position = Vector2(0, 0)
        self.emission_rate = 10  # Particles per second
        self.emission_accumulator = 0.0
        self.active = True
    
    def emit(self, count: int = 1):
        """Emit particles"""
        for _ in range(count):
            if len(self.particles) < self.max_particles:
                particle = Particle()
                particle.position = Vector2(self.position.x, self.position.y)
                particle.velocity = Vector2(
                    (random.random() - 0.5) * 100,
                    (random.random() - 0.5) * 100
                )
                particle.lifetime = 2.0
                particle.size = 4.0
                self.particles.append(particle)
    
    def update(self, dt: float):
        """Update particle system"""
        if self.active:
            self.emission_accumulator += dt
            while self.emission_accumulator >= 1.0 / self.emission_rate:
                self.emission_accumulator -= 1.0 / self.emission_rate
                self.emit(1)
        
        # Update particles
        for particle in self.particles[:]:
            particle.update(dt)
            if particle.is_dead():
                self.particles.remove(particle)

class Particle:
    """Single particle"""
    def __init__(self):
        self.position = Vector2(0, 0)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.color = Color(1, 1, 1, 1)
        self.size = 4.0
        self.lifetime = 1.0
        self.age = 0.0
    
    def update(self, dt: float):
        """Update particle"""
        self.velocity = self.velocity + self.acceleration * dt
        self.position = self.position + self.velocity * dt
        self.age += dt
        
        # Fade out
        self.color.a = 1.0 - (self.age / self.lifetime)
    
    def is_dead(self) -> bool:
        """Check if particle is dead"""
        return self.age >= self.lifetime

class TileMap:
    """2D Tile map"""
    def __init__(self, width: int, height: int, tile_size: int = 32):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.tiles: List[List[int]] = [[0 for _ in range(width)] for _ in range(height)]
        self.tileset: Optional[SpriteSheet] = None
    
    def set_tile(self, x: int, y: int, tile_id: int):
        """Set tile at position"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[y][x] = tile_id
    
    def get_tile(self, x: int, y: int) -> int:
        """Get tile at position"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return 0
    
    def world_to_tile(self, world_pos: Vector2) -> Tuple[int, int]:
        """Convert world position to tile coordinates"""
        return (int(world_pos.x // self.tile_size), int(world_pos.y // self.tile_size))
    
    def tile_to_world(self, tile_x: int, tile_y: int) -> Vector2:
        """Convert tile coordinates to world position"""
        return Vector2(tile_x * self.tile_size, tile_y * self.tile_size)

import random
