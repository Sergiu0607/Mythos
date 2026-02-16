"""
Mythos 3D Engine - Advanced camera system
"""
from standard_library.math.core import Vector3, Matrix4
import math

class Camera3D:
    """3D Camera with various projection modes"""
    def __init__(self, position: Vector3 = None):
        self.position = position or Vector3(0, 0, 10)
        self.target = Vector3(0, 0, 0)
        self.up = Vector3(0, 1, 0)
        
        # Projection settings
        self.fov = 60.0  # Field of view in degrees
        self.aspect_ratio = 16.0 / 9.0
        self.near_plane = 0.1
        self.far_plane = 1000.0
        
        # Rotation (Euler angles in degrees)
        self.yaw = 0.0
        self.pitch = 0.0
        self.roll = 0.0
    
    def look_at(self, target: Vector3):
        """Point camera at target"""
        self.target = target
    
    def forward(self) -> Vector3:
        """Get forward direction vector"""
        direction = (self.target - self.position).normalize()
        return direction
    
    def right(self) -> Vector3:
        """Get right direction vector"""
        forward = self.forward()
        right = forward.cross(self.up).normalize()
        return right
    
    def up_vector(self) -> Vector3:
        """Get up direction vector"""
        forward = self.forward()
        right = self.right()
        up = right.cross(forward).normalize()
        return up
    
    def rotate(self, yaw: float, pitch: float):
        """Rotate camera by yaw and pitch"""
        self.yaw += yaw
        self.pitch += pitch
        
        # Clamp pitch
        self.pitch = max(-89.0, min(89.0, self.pitch))
        
        # Update target based on rotation
        self._update_target_from_rotation()
    
    def _update_target_from_rotation(self):
        """Update target position from yaw and pitch"""
        yaw_rad = math.radians(self.yaw)
        pitch_rad = math.radians(self.pitch)
        
        direction = Vector3(
            math.cos(pitch_rad) * math.cos(yaw_rad),
            math.sin(pitch_rad),
            math.cos(pitch_rad) * math.sin(yaw_rad)
        )
        
        self.target = self.position + direction
    
    def move_forward(self, distance: float):
        """Move camera forward"""
        forward = self.forward()
        self.position = self.position + forward * distance
        self.target = self.target + forward * distance
    
    def move_right(self, distance: float):
        """Move camera right"""
        right = self.right()
        self.position = self.position + right * distance
        self.target = self.target + right * distance
    
    def move_up(self, distance: float):
        """Move camera up"""
        self.position.y += distance
        self.target.y += distance
    
    def get_view_matrix(self) -> Matrix4:
        """Calculate view matrix"""
        # Simplified - real implementation would use proper matrix math
        return Matrix4()
    
    def get_projection_matrix(self) -> Matrix4:
        """Calculate projection matrix"""
        # Simplified - real implementation would calculate perspective projection
        return Matrix4()

class OrbitCamera(Camera3D):
    """Camera that orbits around a target"""
    def __init__(self, target: Vector3 = None, distance: float = 10.0):
        super().__init__()
        self.target = target or Vector3(0, 0, 0)
        self.distance = distance
        self.orbit_speed = 1.0
        self.zoom_speed = 1.0
        self.min_distance = 1.0
        self.max_distance = 100.0
        
        self._update_position()
    
    def orbit(self, delta_yaw: float, delta_pitch: float):
        """Orbit around target"""
        self.yaw += delta_yaw * self.orbit_speed
        self.pitch += delta_pitch * self.orbit_speed
        
        # Clamp pitch
        self.pitch = max(-89.0, min(89.0, self.pitch))
        
        self._update_position()
    
    def zoom(self, delta: float):
        """Zoom in/out"""
        self.distance += delta * self.zoom_speed
        self.distance = max(self.min_distance, min(self.max_distance, self.distance))
        self._update_position()
    
    def _update_position(self):
        """Update camera position based on orbit parameters"""
        yaw_rad = math.radians(self.yaw)
        pitch_rad = math.radians(self.pitch)
        
        x = self.distance * math.cos(pitch_rad) * math.cos(yaw_rad)
        y = self.distance * math.sin(pitch_rad)
        z = self.distance * math.cos(pitch_rad) * math.sin(yaw_rad)
        
        self.position = self.target + Vector3(x, y, z)

class FirstPersonCamera(Camera3D):
    """First-person camera controller"""
    def __init__(self, position: Vector3 = None):
        super().__init__(position)
        self.move_speed = 5.0
        self.look_sensitivity = 0.1
        self.sprint_multiplier = 2.0
        self.is_sprinting = False
    
    def process_mouse_movement(self, delta_x: float, delta_y: float):
        """Process mouse movement for looking"""
        self.rotate(delta_x * self.look_sensitivity, -delta_y * self.look_sensitivity)
    
    def process_movement(self, forward: float, right: float, up: float, dt: float):
        """Process WASD movement"""
        speed = self.move_speed
        if self.is_sprinting:
            speed *= self.sprint_multiplier
        
        if forward != 0:
            self.move_forward(forward * speed * dt)
        if right != 0:
            self.move_right(right * speed * dt)
        if up != 0:
            self.move_up(up * speed * dt)

class ThirdPersonCamera(Camera3D):
    """Third-person camera that follows a target"""
    def __init__(self, target: Vector3 = None):
        super().__init__()
        self.follow_target = target or Vector3(0, 0, 0)
        self.offset = Vector3(0, 2, -5)
        self.look_at_offset = Vector3(0, 1, 0)
        self.smoothness = 5.0
        self.collision_radius = 0.5
    
    def update(self, dt: float):
        """Update camera to follow target"""
        # Calculate desired position
        desired_position = self.follow_target + self.offset
        
        # Smooth interpolation
        t = 1.0 - math.exp(-self.smoothness * dt)
        self.position.x += (desired_position.x - self.position.x) * t
        self.position.y += (desired_position.y - self.position.y) * t
        self.position.z += (desired_position.z - self.position.z) * t
        
        # Look at target with offset
        self.target = self.follow_target + self.look_at_offset
    
    def set_offset(self, offset: Vector3):
        """Set camera offset from target"""
        self.offset = offset

class CinematicCamera(Camera3D):
    """Camera for cinematic sequences"""
    def __init__(self):
        super().__init__()
        self.waypoints: list = []
        self.current_waypoint = 0
        self.playing = False
        self.loop = False
        self.speed = 1.0
        self.progress = 0.0
    
    def add_waypoint(self, position: Vector3, target: Vector3, duration: float = 1.0):
        """Add a camera waypoint"""
        self.waypoints.append({
            'position': position,
            'target': target,
            'duration': duration
        })
    
    def play(self):
        """Start playing cinematic"""
        self.playing = True
        self.current_waypoint = 0
        self.progress = 0.0
    
    def stop(self):
        """Stop playing cinematic"""
        self.playing = False
    
    def update(self, dt: float):
        """Update cinematic camera"""
        if not self.playing or not self.waypoints:
            return
        
        if self.current_waypoint >= len(self.waypoints) - 1:
            if self.loop:
                self.current_waypoint = 0
                self.progress = 0.0
            else:
                self.playing = False
                return
        
        current = self.waypoints[self.current_waypoint]
        next_wp = self.waypoints[self.current_waypoint + 1]
        
        self.progress += dt * self.speed / current['duration']
        
        if self.progress >= 1.0:
            self.current_waypoint += 1
            self.progress = 0.0
        else:
            # Interpolate between waypoints
            t = self.progress
            # Smooth interpolation (ease in-out)
            t = t * t * (3.0 - 2.0 * t)
            
            self.position = self._lerp_vector3(current['position'], next_wp['position'], t)
            self.target = self._lerp_vector3(current['target'], next_wp['target'], t)
    
    def _lerp_vector3(self, a: Vector3, b: Vector3, t: float) -> Vector3:
        """Linear interpolation between two vectors"""
        return Vector3(
            a.x + (b.x - a.x) * t,
            a.y + (b.y - a.y) * t,
            a.z + (b.z - a.z) * t
        )
