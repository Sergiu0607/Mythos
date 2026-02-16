"""
Mythos AI - Behavior Trees for game AI
"""
from enum import Enum, auto
from typing import List, Callable, Optional, Any
from abc import ABC, abstractmethod

class NodeStatus(Enum):
    """Status of a behavior tree node"""
    SUCCESS = auto()
    FAILURE = auto()
    RUNNING = auto()

class BehaviorNode(ABC):
    """Base class for behavior tree nodes"""
    def __init__(self, name: str = "Node"):
        self.name = name
        self.status = NodeStatus.FAILURE
    
    @abstractmethod
    def tick(self, context: Any) -> NodeStatus:
        """Execute the node"""
        pass
    
    def reset(self):
        """Reset node state"""
        self.status = NodeStatus.FAILURE

class ActionNode(BehaviorNode):
    """Leaf node that performs an action"""
    def __init__(self, name: str, action: Callable):
        super().__init__(name)
        self.action = action
    
    def tick(self, context: Any) -> NodeStatus:
        """Execute the action"""
        try:
            result = self.action(context)
            if result is True:
                self.status = NodeStatus.SUCCESS
            elif result is False:
                self.status = NodeStatus.FAILURE
            else:
                self.status = NodeStatus.RUNNING
            return self.status
        except Exception as e:
            print(f"Action '{self.name}' failed: {e}")
            self.status = NodeStatus.FAILURE
            return self.status

class ConditionNode(BehaviorNode):
    """Leaf node that checks a condition"""
    def __init__(self, name: str, condition: Callable):
        super().__init__(name)
        self.condition = condition
    
    def tick(self, context: Any) -> NodeStatus:
        """Check the condition"""
        try:
            result = self.condition(context)
            self.status = NodeStatus.SUCCESS if result else NodeStatus.FAILURE
            return self.status
        except Exception as e:
            print(f"Condition '{self.name}' failed: {e}")
            self.status = NodeStatus.FAILURE
            return self.status

class CompositeNode(BehaviorNode):
    """Node with multiple children"""
    def __init__(self, name: str):
        super().__init__(name)
        self.children: List[BehaviorNode] = []
    
    def add_child(self, child: BehaviorNode):
        """Add a child node"""
        self.children.append(child)
        return self
    
    def reset(self):
        """Reset this node and all children"""
        super().reset()
        for child in self.children:
            child.reset()

class SequenceNode(CompositeNode):
    """Execute children in sequence until one fails"""
    def __init__(self, name: str = "Sequence"):
        super().__init__(name)
        self.current_child = 0
    
    def tick(self, context: Any) -> NodeStatus:
        """Execute children in sequence"""
        while self.current_child < len(self.children):
            child = self.children[self.current_child]
            status = child.tick(context)
            
            if status == NodeStatus.FAILURE:
                self.current_child = 0
                self.status = NodeStatus.FAILURE
                return self.status
            
            if status == NodeStatus.RUNNING:
                self.status = NodeStatus.RUNNING
                return self.status
            
            # SUCCESS - move to next child
            self.current_child += 1
        
        # All children succeeded
        self.current_child = 0
        self.status = NodeStatus.SUCCESS
        return self.status
    
    def reset(self):
        super().reset()
        self.current_child = 0

class SelectorNode(CompositeNode):
    """Execute children until one succeeds"""
    def __init__(self, name: str = "Selector"):
        super().__init__(name)
        self.current_child = 0
    
    def tick(self, context: Any) -> NodeStatus:
        """Execute children until one succeeds"""
        while self.current_child < len(self.children):
            child = self.children[self.current_child]
            status = child.tick(context)
            
            if status == NodeStatus.SUCCESS:
                self.current_child = 0
                self.status = NodeStatus.SUCCESS
                return self.status
            
            if status == NodeStatus.RUNNING:
                self.status = NodeStatus.RUNNING
                return self.status
            
            # FAILURE - try next child
            self.current_child += 1
        
        # All children failed
        self.current_child = 0
        self.status = NodeStatus.FAILURE
        return self.status
    
    def reset(self):
        super().reset()
        self.current_child = 0

class ParallelNode(CompositeNode):
    """Execute all children simultaneously"""
    def __init__(self, name: str = "Parallel", success_threshold: int = 1):
        super().__init__(name)
        self.success_threshold = success_threshold
    
    def tick(self, context: Any) -> NodeStatus:
        """Execute all children"""
        success_count = 0
        failure_count = 0
        running_count = 0
        
        for child in self.children:
            status = child.tick(context)
            
            if status == NodeStatus.SUCCESS:
                success_count += 1
            elif status == NodeStatus.FAILURE:
                failure_count += 1
            else:
                running_count += 1
        
        # Check if enough children succeeded
        if success_count >= self.success_threshold:
            self.status = NodeStatus.SUCCESS
            return self.status
        
        # Check if too many failed
        remaining = len(self.children) - failure_count
        if remaining < self.success_threshold:
            self.status = NodeStatus.FAILURE
            return self.status
        
        # Still running
        self.status = NodeStatus.RUNNING
        return self.status

class DecoratorNode(BehaviorNode):
    """Node that modifies behavior of a single child"""
    def __init__(self, name: str, child: BehaviorNode = None):
        super().__init__(name)
        self.child = child
    
    def set_child(self, child: BehaviorNode):
        """Set the child node"""
        self.child = child
        return self

class InverterNode(DecoratorNode):
    """Inverts the result of child"""
    def tick(self, context: Any) -> NodeStatus:
        """Invert child result"""
        if not self.child:
            self.status = NodeStatus.FAILURE
            return self.status
        
        status = self.child.tick(context)
        
        if status == NodeStatus.SUCCESS:
            self.status = NodeStatus.FAILURE
        elif status == NodeStatus.FAILURE:
            self.status = NodeStatus.SUCCESS
        else:
            self.status = NodeStatus.RUNNING
        
        return self.status

class RepeaterNode(DecoratorNode):
    """Repeats child N times or until failure"""
    def __init__(self, name: str, repeat_count: int = -1, child: BehaviorNode = None):
        super().__init__(name, child)
        self.repeat_count = repeat_count  # -1 = infinite
        self.current_count = 0
    
    def tick(self, context: Any) -> NodeStatus:
        """Repeat child execution"""
        if not self.child:
            self.status = NodeStatus.FAILURE
            return self.status
        
        while self.repeat_count < 0 or self.current_count < self.repeat_count:
            status = self.child.tick(context)
            
            if status == NodeStatus.FAILURE:
                self.current_count = 0
                self.status = NodeStatus.FAILURE
                return self.status
            
            if status == NodeStatus.RUNNING:
                self.status = NodeStatus.RUNNING
                return self.status
            
            self.current_count += 1
            self.child.reset()
        
        self.current_count = 0
        self.status = NodeStatus.SUCCESS
        return self.status
    
    def reset(self):
        super().reset()
        self.current_count = 0

class BehaviorTree:
    """Behavior tree for AI"""
    def __init__(self, root: BehaviorNode = None):
        self.root = root
        self.context: Any = None
    
    def set_root(self, root: BehaviorNode):
        """Set root node"""
        self.root = root
    
    def tick(self, context: Any = None) -> NodeStatus:
        """Execute the behavior tree"""
        if not self.root:
            return NodeStatus.FAILURE
        
        if context:
            self.context = context
        
        return self.root.tick(self.context)
    
    def reset(self):
        """Reset the tree"""
        if self.root:
            self.root.reset()

# Builder pattern for easy tree construction
class BehaviorTreeBuilder:
    """Builder for creating behavior trees"""
    def __init__(self):
        self.stack: List[BehaviorNode] = []
        self.root: Optional[BehaviorNode] = None
    
    def sequence(self, name: str = "Sequence"):
        """Start a sequence node"""
        node = SequenceNode(name)
        self._add_node(node)
        self.stack.append(node)
        return self
    
    def selector(self, name: str = "Selector"):
        """Start a selector node"""
        node = SelectorNode(name)
        self._add_node(node)
        self.stack.append(node)
        return self
    
    def parallel(self, name: str = "Parallel", success_threshold: int = 1):
        """Start a parallel node"""
        node = ParallelNode(name, success_threshold)
        self._add_node(node)
        self.stack.append(node)
        return self
    
    def action(self, name: str, action: Callable):
        """Add an action node"""
        node = ActionNode(name, action)
        self._add_node(node)
        return self
    
    def condition(self, name: str, condition: Callable):
        """Add a condition node"""
        node = ConditionNode(name, condition)
        self._add_node(node)
        return self
    
    def inverter(self, name: str = "Inverter"):
        """Start an inverter decorator"""
        node = InverterNode(name)
        self._add_node(node)
        self.stack.append(node)
        return self
    
    def repeater(self, name: str = "Repeater", count: int = -1):
        """Start a repeater decorator"""
        node = RepeaterNode(name, count)
        self._add_node(node)
        self.stack.append(node)
        return self
    
    def end(self):
        """End current composite/decorator node"""
        if self.stack:
            self.stack.pop()
        return self
    
    def build(self) -> BehaviorTree:
        """Build and return the behavior tree"""
        return BehaviorTree(self.root)
    
    def _add_node(self, node: BehaviorNode):
        """Add node to current parent or set as root"""
        if not self.stack:
            self.root = node
        else:
            parent = self.stack[-1]
            if isinstance(parent, CompositeNode):
                parent.add_child(node)
            elif isinstance(parent, DecoratorNode):
                parent.set_child(node)
