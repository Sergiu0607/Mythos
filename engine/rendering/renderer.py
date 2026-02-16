"""
Mythos Rendering Engine - Core renderer
"""
from typing import List, Tuple, Optional
from standard_library.math.core import Vector3, Matrix4
import numpy as np

class Color:
    """RGBA Color"""
    def __init__(self, r: float = 1.0, g: float = 1.0, b: float = 1.0, a: float = 1.0):
        self.r = max(0, min(1, r))
        self.g = max(0, min(1, g))
        self.b = max(0, min(1, b))
        self.a = max(0, min(1, a))
    
    @staticmethod
    def from_hex(hex_color: str) -> 'Color':
        """Create color from hex string like #FF0000"""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16) / 255
        g = int(hex_color[2:4], 16) / 255
        b = int(hex_color[4:6], 16) / 255
        return Color(r, g, b)
    
    def to_hex(self) -> str:
        """Convert to hex string"""
        r = int(self.r * 255)
        g = int(self.g * 255)
        b = int(self.b * 255)
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def __repr__(self):
        return f"Color({self.r}, {self.g}, {self.b}, {self.a})"

class Material:
    """Material properties for rendering"""
    def __init__(self, color: Color = None, metallic: float = 0.0, roughness: float = 0.5, emissive: Color = None):
        self.color = color or Color(1, 1, 1)
        self.metallic = metallic
        self.roughness = roughness
        self.emissive = emissive or Color(0, 0, 0)
        self.texture = None
    
    def set_texture(self, texture_path: str):
        """Set texture from file"""
        self.texture = texture_path

class Mesh:
    """3D Mesh with vertices, normals, and UVs"""
    def __init__(self):
        self.vertices: List[Vector3] = []
        self.normals: List[Vector3] = []
        self.uvs: List[Tuple[float, float]] = []
        self.indices: List[int] = []
        self.material: Optional[Material] = None
    
    @staticmethod
    def create_cube(size: float = 1.0) -> 'Mesh':
        """Create a cube mesh"""
        mesh = Mesh()
        s = size / 2
        
        # Vertices for a cube
        vertices = [
            Vector3(-s, -s, -s), Vector3(s, -s, -s), Vector3(s, s, -s), Vector3(-s, s, -s),  # Front
            Vector3(-s, -s, s), Vector3(s, -s, s), Vector3(s, s, s), Vector3(-s, s, s),      # Back
        ]
        
        # Indices for triangles
        indices = [
            0, 1, 2, 0, 2, 3,  # Front
            1, 5, 6, 1, 6, 2,  # Right
            5, 4, 7, 5, 7, 6,  # Back
            4, 0, 3, 4, 3, 7,  # Left
            3, 2, 6, 3, 6, 7,  # Top
            4, 5, 1, 4, 1, 0,  # Bottom
        ]
        
        mesh.vertices = vertices
        mesh.indices = indices
        return mesh
    
    @staticmethod
    def create_sphere(radius: float = 1.0, segments: int = 32) -> 'Mesh':
        """Create a sphere mesh"""
        mesh = Mesh()
        
        for lat in range(segments + 1):
            theta = lat * np.pi / segments
            sin_theta = np.sin(theta)
            cos_theta = np.cos(theta)
            
            for lon in range(segments + 1):
                phi = lon * 2 * np.pi / segments
                sin_phi = np.sin(phi)
                cos_phi = np.cos(phi)
                
                x = cos_phi * sin_theta
                y = cos_theta
                z = sin_phi * sin_theta
                
                mesh.vertices.append(Vector3(x * radius, y * radius, z * radius))
                mesh.normals.append(Vector3(x, y, z))
                mesh.uvs.append((lon / segments, lat / segments))
        
        # Generate indices
        for lat in range(segments):
            for lon in range(segments):
                first = lat * (segments + 1) + lon
                second = first + segments + 1
                
                mesh.indices.extend([first, second, first + 1])
                mesh.indices.extend([second, second + 1, first + 1])
        
        return mesh
    
    @staticmethod
    def create_plane(width: float = 1.0, height: float = 1.0) -> 'Mesh':
        """Create a plane mesh"""
        mesh = Mesh()
        w = width / 2
        h = height / 2
        
        mesh.vertices = [
            Vector3(-w, 0, -h),
            Vector3(w, 0, -h),
            Vector3(w, 0, h),
            Vector3(-w, 0, h)
        ]
        
        mesh.normals = [Vector3(0, 1, 0)] * 4
        mesh.uvs = [(0, 0), (1, 0), (1, 1), (0, 1)]
        mesh.indices = [0, 1, 2, 0, 2, 3]
        
        return mesh

class Light:
    """Light source"""
    def __init__(self, light_type: str = "point", color: Color = None, intensity: float = 1.0):
        self.type = light_type  # "point", "directional", "spot", "ambient"
        self.color = color or Color(1, 1, 1)
        self.intensity = intensity
        self.position = Vector3(0, 0, 0)
        self.direction = Vector3(0, -1, 0)
        self.range = 10.0
        self.angle = 45.0  # For spotlights

class Camera:
    """Camera for rendering"""
    def __init__(self, position: Vector3 = None, target: Vector3 = None):
        self.position = position or Vector3(0, 0, 10)
        self.target = target or Vector3(0, 0, 0)
        self.up = Vector3(0, 1, 0)
        self.fov = 60.0  # Field of view in degrees
        self.near = 0.1
        self.far = 1000.0
        self.aspect_ratio = 16.0 / 9.0
    
    def look_at(self, target: Vector3):
        """Point camera at target"""
        self.target = target
    
    def get_view_matrix(self) -> Matrix4:
        """Calculate view matrix"""
        # Simplified view matrix calculation
        forward = (self.target - self.position).normalize()
        right = forward.cross(self.up).normalize()
        up = right.cross(forward)
        
        # This would return a proper view matrix
        return Matrix4()
    
    def get_projection_matrix(self) -> Matrix4:
        """Calculate projection matrix"""
        # Simplified projection matrix
        return Matrix4()

class RenderObject:
    """Object to be rendered"""
    def __init__(self, mesh: Mesh, material: Material = None):
        self.mesh = mesh
        self.material = material or Material()
        self.position = Vector3(0, 0, 0)
        self.rotation = Vector3(0, 0, 0)
        self.scale = Vector3(1, 1, 1)
        self.visible = True
    
    def get_transform_matrix(self) -> Matrix4:
        """Get transformation matrix"""
        matrix = Matrix4()
        # Apply transformations
        matrix = matrix.translate(self.position.x, self.position.y, self.position.z)
        matrix = matrix.rotate_x(self.rotation.x)
        matrix = matrix.rotate_y(self.rotation.y)
        matrix = matrix.rotate_z(self.rotation.z)
        matrix = matrix.scale(self.scale.x, self.scale.y, self.scale.z)
        return matrix

class Renderer:
    """Main rendering engine"""
    def __init__(self, width: int = 800, height: int = 600):
        self.width = width
        self.height = height
        self.camera: Optional[Camera] = None
        self.objects: List[RenderObject] = []
        self.lights: List[Light] = []
        self.clear_color = Color(0.1, 0.1, 0.1)
    
    def set_camera(self, camera: Camera):
        """Set active camera"""
        self.camera = camera
        self.camera.aspect_ratio = self.width / self.height
    
    def add_object(self, obj: RenderObject):
        """Add object to scene"""
        self.objects.append(obj)
    
    def add_light(self, light: Light):
        """Add light to scene"""
        self.lights.append(light)
    
    def render(self):
        """Render the scene"""
        if not self.camera:
            raise RuntimeError("No camera set")
        
        # Clear screen
        self._clear()
        
        # Get view and projection matrices
        view_matrix = self.camera.get_view_matrix()
        proj_matrix = self.camera.get_projection_matrix()
        
        # Render each object
        for obj in self.objects:
            if not obj.visible:
                continue
            
            # Get object transform
            model_matrix = obj.get_transform_matrix()
            
            # Render mesh
            self._render_mesh(obj.mesh, obj.material, model_matrix, view_matrix, proj_matrix)
    
    def _clear(self):
        """Clear the screen"""
        pass  # Implementation would clear the framebuffer
    
    def _render_mesh(self, mesh: Mesh, material: Material, model: Matrix4, view: Matrix4, projection: Matrix4):
        """Render a mesh"""
        # This would contain the actual rendering logic
        # - Transform vertices
        # - Apply lighting
        # - Rasterize triangles
        # - Apply materials and textures
        pass
    
    def resize(self, width: int, height: int):
        """Resize viewport"""
        self.width = width
        self.height = height
        if self.camera:
            self.camera.aspect_ratio = width / height
