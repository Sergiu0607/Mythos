"""
Mythos Scene Management - Scene graph and entity system
"""
from typing import List, Dict, Optional, Any
from standard_library.math.core import Vector3
from engine.rendering.renderer import RenderObject, Camera, Light, Mesh, Material, Color

class Entity:
    """Base entity in the scene"""
    def __init__(self, name: str = "Entity"):
        self.name = name
        self.position = Vector3(0, 0, 0)
        self.rotation = Vector3(0, 0, 0)
        self.scale = Vector3(1, 1, 1)
        self.parent: Optional['Entity'] = None
        self.children: List['Entity'] = []
        self.components: Dict[str, Any] = {}
        self.active = True
    
    def add_child(self, child: 'Entity'):
        """Add child entity"""
        child.parent = self
        self.children.append(child)
    
    def remove_child(self, child: 'Entity'):
        """Remove child entity"""
        if child in self.children:
            child.parent = None
            self.children.remove(child)
    
    def add_component(self, name: str, component: Any):
        """Add component to entity"""
        self.components[name] = component
    
    def get_component(self, name: str) -> Optional[Any]:
        """Get component by name"""
        return self.components.get(name)
    
    def update(self, delta_time: float):
        """Update entity and children"""
        if not self.active:
            return
        
        # Update children
        for child in self.children:
            child.update(delta_time)

class MeshEntity(Entity):
    """Entity with a mesh renderer"""
    def __init__(self, name: str = "MeshEntity", mesh: Mesh = None, material: Material = None):
        super().__init__(name)
        self.mesh = mesh
        self.material = material or Material()
        self.render_object: Optional[RenderObject] = None
    
    def create_render_object(self) -> RenderObject:
        """Create render object for this entity"""
        if not self.mesh:
            return None
        
        self.render_object = RenderObject(self.mesh, self.material)
        self.render_object.position = self.position
        self.render_object.rotation = self.rotation
        self.render_object.scale = self.scale
        return self.render_object
    
    def update(self, delta_time: float):
        """Update mesh entity"""
        super().update(delta_time)
        
        # Sync render object with entity transform
        if self.render_object:
            self.render_object.position = self.position
            self.render_object.rotation = self.rotation
            self.render_object.scale = self.scale

class CameraEntity(Entity):
    """Entity with a camera"""
    def __init__(self, name: str = "Camera"):
        super().__init__(name)
        self.camera = Camera()
    
    def update(self, delta_time: float):
        """Update camera entity"""
        super().update(delta_time)
        self.camera.position = self.position

class LightEntity(Entity):
    """Entity with a light"""
    def __init__(self, name: str = "Light", light_type: str = "point"):
        super().__init__(name)
        self.light = Light(light_type)
    
    def update(self, delta_time: float):
        """Update light entity"""
        super().update(delta_time)
        self.light.position = self.position

class Scene:
    """Scene containing entities"""
    def __init__(self, name: str = "Scene"):
        self.name = name
        self.root = Entity("Root")
        self.entities: List[Entity] = []
        self.camera: Optional[CameraEntity] = None
        self.lights: List[LightEntity] = []
        self.ambient_light = Color(0.2, 0.2, 0.2)
    
    def add_entity(self, entity: Entity, parent: Entity = None):
        """Add entity to scene"""
        self.entities.append(entity)
        
        if parent:
            parent.add_child(entity)
        else:
            self.root.add_child(entity)
        
        # Track cameras and lights
        if isinstance(entity, CameraEntity):
            if not self.camera:
                self.camera = entity
        elif isinstance(entity, LightEntity):
            self.lights.append(entity)
    
    def remove_entity(self, entity: Entity):
        """Remove entity from scene"""
        if entity in self.entities:
            self.entities.remove(entity)
            if entity.parent:
                entity.parent.remove_child(entity)
    
    def find_entity(self, name: str) -> Optional[Entity]:
        """Find entity by name"""
        for entity in self.entities:
            if entity.name == name:
                return entity
        return None
    
    def get_all_mesh_entities(self) -> List[MeshEntity]:
        """Get all mesh entities in scene"""
        return [e for e in self.entities if isinstance(e, MeshEntity)]
    
    def update(self, delta_time: float):
        """Update all entities in scene"""
        self.root.update(delta_time)
    
    def create_cube(self, name: str = "Cube", position: Vector3 = None, size: float = 1.0, color: Color = None) -> MeshEntity:
        """Helper to create a cube entity"""
        mesh = Mesh.create_cube(size)
        material = Material(color or Color(1, 1, 1))
        entity = MeshEntity(name, mesh, material)
        if position:
            entity.position = position
        self.add_entity(entity)
        return entity
    
    def create_sphere(self, name: str = "Sphere", position: Vector3 = None, radius: float = 1.0, color: Color = None) -> MeshEntity:
        """Helper to create a sphere entity"""
        mesh = Mesh.create_sphere(radius)
        material = Material(color or Color(1, 1, 1))
        entity = MeshEntity(name, mesh, material)
        if position:
            entity.position = position
        self.add_entity(entity)
        return entity
    
    def create_plane(self, name: str = "Plane", position: Vector3 = None, width: float = 1.0, height: float = 1.0, color: Color = None) -> MeshEntity:
        """Helper to create a plane entity"""
        mesh = Mesh.create_plane(width, height)
        material = Material(color or Color(1, 1, 1))
        entity = MeshEntity(name, mesh, material)
        if position:
            entity.position = position
        self.add_entity(entity)
        return entity
    
    def create_camera(self, name: str = "Camera", position: Vector3 = None, target: Vector3 = None) -> CameraEntity:
        """Helper to create a camera entity"""
        entity = CameraEntity(name)
        if position:
            entity.position = position
        if target:
            entity.camera.look_at(target)
        self.add_entity(entity)
        return entity
    
    def create_light(self, name: str = "Light", light_type: str = "point", position: Vector3 = None, color: Color = None, intensity: float = 1.0) -> LightEntity:
        """Helper to create a light entity"""
        entity = LightEntity(name, light_type)
        if position:
            entity.position = position
        if color:
            entity.light.color = color
        entity.light.intensity = intensity
        self.add_entity(entity)
        return entity

class SceneManager:
    """Manages multiple scenes"""
    def __init__(self):
        self.scenes: Dict[str, Scene] = {}
        self.active_scene: Optional[Scene] = None
    
    def create_scene(self, name: str) -> Scene:
        """Create a new scene"""
        scene = Scene(name)
        self.scenes[name] = scene
        if not self.active_scene:
            self.active_scene = scene
        return scene
    
    def load_scene(self, name: str):
        """Load a scene by name"""
        if name in self.scenes:
            self.active_scene = self.scenes[name]
        else:
            raise ValueError(f"Scene '{name}' not found")
    
    def get_scene(self, name: str) -> Optional[Scene]:
        """Get scene by name"""
        return self.scenes.get(name)
    
    def update(self, delta_time: float):
        """Update active scene"""
        if self.active_scene:
            self.active_scene.update(delta_time)
