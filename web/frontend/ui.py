"""
Mythos UI Framework - Build UIs without HTML/CSS
"""
from typing import List, Dict, Any, Optional, Callable

class UIElement:
    """Base UI element"""
    def __init__(self, element_type: str):
        self.type = element_type
        self.children: List['UIElement'] = []
        self.props: Dict[str, Any] = {}
        self.styles: Dict[str, str] = {}
        self.events: Dict[str, Callable] = {}
    
    def add_child(self, child: 'UIElement'):
        """Add child element"""
        self.children.append(child)
        return self
    
    def set_prop(self, key: str, value: Any):
        """Set property"""
        self.props[key] = value
        return self
    
    def set_style(self, key: str, value: str):
        """Set style"""
        self.styles[key] = value
        return self
    
    def on(self, event: str, handler: Callable):
        """Add event handler"""
        self.events[event] = handler
        return self
    
    def render(self) -> str:
        """Render to HTML"""
        # Build attributes
        attrs = []
        for key, value in self.props.items():
            attrs.append(f'{key}="{value}"')
        
        # Build styles
        if self.styles:
            style_str = '; '.join([f'{k}: {v}' for k, v in self.styles.items()])
            attrs.append(f'style="{style_str}"')
        
        # Build event handlers (would be converted to JavaScript)
        for event, handler in self.events.items():
            attrs.append(f'on{event}="handleEvent(event)"')
        
        attrs_str = ' '.join(attrs)
        
        # Render children
        children_html = ''.join([child.render() for child in self.children])
        
        # Self-closing tags
        if self.type in ('img', 'input', 'br', 'hr'):
            return f'<{self.type} {attrs_str} />'
        
        return f'<{self.type} {attrs_str}>{children_html}</{self.type}>'

class Text(UIElement):
    """Text element"""
    def __init__(self, content: str, tag: str = "p"):
        super().__init__(tag)
        self.content = content
    
    def render(self) -> str:
        attrs_str = ' '.join([f'{k}="{v}"' for k, v in self.props.items()])
        if self.styles:
            style_str = '; '.join([f'{k}: {v}' for k, v in self.styles.items()])
            attrs_str += f' style="{style_str}"'
        return f'<{self.type} {attrs_str}>{self.content}</{self.type}>'

class Button(UIElement):
    """Button element"""
    def __init__(self, text: str, on_click: Callable = None):
        super().__init__("button")
        self.text = text
        if on_click:
            self.on("click", on_click)
    
    def render(self) -> str:
        attrs_str = ' '.join([f'{k}="{v}"' for k, v in self.props.items()])
        if self.styles:
            style_str = '; '.join([f'{k}: {v}' for k, v in self.styles.items()])
            attrs_str += f' style="{style_str}"'
        
        # Add default button styles
        default_styles = "padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer;"
        attrs_str += f' style="{default_styles}"'
        
        return f'<button {attrs_str}>{self.text}</button>'

class Input(UIElement):
    """Input element"""
    def __init__(self, input_type: str = "text", placeholder: str = "", value: str = ""):
        super().__init__("input")
        self.set_prop("type", input_type)
        if placeholder:
            self.set_prop("placeholder", placeholder)
        if value:
            self.set_prop("value", value)

class Container(UIElement):
    """Container element (div)"""
    def __init__(self):
        super().__init__("div")

class Row(UIElement):
    """Horizontal layout container"""
    def __init__(self):
        super().__init__("div")
        self.set_style("display", "flex")
        self.set_style("flex-direction", "row")

class Column(UIElement):
    """Vertical layout container"""
    def __init__(self):
        super().__init__("div")
        self.set_style("display", "flex")
        self.set_style("flex-direction", "column")

class Image(UIElement):
    """Image element"""
    def __init__(self, src: str, alt: str = ""):
        super().__init__("img")
        self.set_prop("src", src)
        self.set_prop("alt", alt)

class Link(UIElement):
    """Link element"""
    def __init__(self, href: str, text: str):
        super().__init__("a")
        self.set_prop("href", href)
        self.text = text
    
    def render(self) -> str:
        attrs_str = ' '.join([f'{k}="{v}"' for k, v in self.props.items()])
        return f'<a {attrs_str}>{self.text}</a>'

class List(UIElement):
    """List element"""
    def __init__(self, items: List[str], ordered: bool = False):
        super().__init__("ol" if ordered else "ul")
        for item in items:
            li = UIElement("li")
            li.props["_content"] = item
            self.add_child(li)
    
    def render(self) -> str:
        items_html = ''.join([f'<li>{child.props.get("_content", "")}</li>' for child in self.children])
        return f'<{self.type}>{items_html}</{self.type}>'

class Card(Container):
    """Card component"""
    def __init__(self, title: str = "", content: str = ""):
        super().__init__()
        self.set_style("border", "1px solid #ddd")
        self.set_style("border-radius", "8px")
        self.set_style("padding", "20px")
        self.set_style("margin", "10px")
        self.set_style("box-shadow", "0 2px 4px rgba(0,0,0,0.1)")
        
        if title:
            title_elem = Text(title, "h3")
            title_elem.set_style("margin-top", "0")
            self.add_child(title_elem)
        
        if content:
            content_elem = Text(content, "p")
            self.add_child(content_elem)

class Grid(UIElement):
    """Grid layout"""
    def __init__(self, columns: int = 3, gap: str = "10px"):
        super().__init__("div")
        self.set_style("display", "grid")
        self.set_style("grid-template-columns", f"repeat({columns}, 1fr)")
        self.set_style("gap", gap)

class Page:
    """Full page component"""
    def __init__(self, title: str = "Mythos App"):
        self.title = title
        self.head_elements: List[str] = []
        self.body = Container()
        self.body.set_style("font-family", "Arial, sans-serif")
        self.body.set_style("margin", "0")
        self.body.set_style("padding", "20px")
    
    def add_element(self, element: UIElement):
        """Add element to page body"""
        self.body.add_child(element)
        return self
    
    def add_style(self, css: str):
        """Add custom CSS"""
        self.head_elements.append(f"<style>{css}</style>")
        return self
    
    def add_script(self, js: str):
        """Add custom JavaScript"""
        self.head_elements.append(f"<script>{js}</script>")
        return self
    
    def render(self) -> str:
        """Render full HTML page"""
        head_content = '\n'.join(self.head_elements)
        body_content = self.body.render()
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.title}</title>
    {head_content}
</head>
<body>
    {body_content}
</body>
</html>"""

# Helper functions
def text(content: str, tag: str = "p") -> Text:
    """Create text element"""
    return Text(content, tag)

def button(text: str, on_click: Callable = None) -> Button:
    """Create button"""
    return Button(text, on_click)

def input_field(input_type: str = "text", placeholder: str = "", value: str = "") -> Input:
    """Create input field"""
    return Input(input_type, placeholder, value)

def container() -> Container:
    """Create container"""
    return Container()

def row() -> Row:
    """Create row layout"""
    return Row()

def column() -> Column:
    """Create column layout"""
    return Column()

def image(src: str, alt: str = "") -> Image:
    """Create image"""
    return Image(src, alt)

def link(href: str, text: str) -> Link:
    """Create link"""
    return Link(href, text)

def list_items(items: List[str], ordered: bool = False) -> List:
    """Create list"""
    return List(items, ordered)

def card(title: str = "", content: str = "") -> Card:
    """Create card"""
    return Card(title, content)

def grid(columns: int = 3, gap: str = "10px") -> Grid:
    """Create grid layout"""
    return Grid(columns, gap)

def page(title: str = "Mythos App") -> Page:
    """Create page"""
    return Page(title)
