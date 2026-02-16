"""
Mythos Web Server - Built-in HTTP server
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Callable, Any, Optional
import json
import mimetypes
from urllib.parse import urlparse, parse_qs

class Route:
    """HTTP Route"""
    def __init__(self, path: str, handler: Callable, method: str = "GET"):
        self.path = path
        self.handler = handler
        self.method = method.upper()
        self.params: Dict[str, str] = {}

class Request:
    """HTTP Request wrapper"""
    def __init__(self, method: str, path: str, headers: Dict, body: str = ""):
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body
        self.query: Dict[str, Any] = {}
        self.params: Dict[str, str] = {}
        
        # Parse query string
        parsed = urlparse(path)
        self.path = parsed.path
        self.query = parse_qs(parsed.query)
    
    def json(self) -> Dict:
        """Parse body as JSON"""
        try:
            return json.loads(self.body)
        except:
            return {}

class Response:
    """HTTP Response wrapper"""
    def __init__(self):
        self.status_code = 200
        self.headers: Dict[str, str] = {"Content-Type": "text/html"}
        self.body = ""
    
    def set_status(self, code: int):
        """Set status code"""
        self.status_code = code
        return self
    
    def set_header(self, key: str, value: str):
        """Set response header"""
        self.headers[key] = value
        return self
    
    def json(self, data: Any):
        """Send JSON response"""
        self.headers["Content-Type"] = "application/json"
        self.body = json.dumps(data)
        return self
    
    def html(self, content: str):
        """Send HTML response"""
        self.headers["Content-Type"] = "text/html"
        self.body = content
        return self
    
    def text(self, content: str):
        """Send plain text response"""
        self.headers["Content-Type"] = "text/plain"
        self.body = content
        return self

class Router:
    """HTTP Router"""
    def __init__(self):
        self.routes: Dict[str, Dict[str, Route]] = {}
        self.middleware: list = []
    
    def add_route(self, method: str, path: str, handler: Callable):
        """Add a route"""
        method = method.upper()
        if method not in self.routes:
            self.routes[method] = {}
        self.routes[method][path] = Route(path, handler, method)
    
    def get(self, path: str, handler: Callable):
        """Add GET route"""
        self.add_route("GET", path, handler)
    
    def post(self, path: str, handler: Callable):
        """Add POST route"""
        self.add_route("POST", path, handler)
    
    def put(self, path: str, handler: Callable):
        """Add PUT route"""
        self.add_route("PUT", path, handler)
    
    def delete(self, path: str, handler: Callable):
        """Add DELETE route"""
        self.add_route("DELETE", path, handler)
    
    def use(self, middleware: Callable):
        """Add middleware"""
        self.middleware.append(middleware)
    
    def match_route(self, method: str, path: str) -> Optional[Route]:
        """Match a route"""
        method = method.upper()
        
        if method not in self.routes:
            return None
        
        # Exact match
        if path in self.routes[method]:
            return self.routes[method][path]
        
        # Pattern matching (simplified)
        for route_path, route in self.routes[method].items():
            if self._match_pattern(route_path, path):
                return route
        
        return None
    
    def _match_pattern(self, pattern: str, path: str) -> bool:
        """Match route pattern with path parameters"""
        pattern_parts = pattern.split('/')
        path_parts = path.split('/')
        
        if len(pattern_parts) != len(path_parts):
            return False
        
        for pattern_part, path_part in zip(pattern_parts, path_parts):
            if pattern_part.startswith(':'):
                # Path parameter
                continue
            elif pattern_part != path_part:
                return False
        
        return True

class MythosHTTPHandler(BaseHTTPRequestHandler):
    """Custom HTTP request handler"""
    router: Router = None
    
    def do_GET(self):
        self._handle_request("GET")
    
    def do_POST(self):
        self._handle_request("POST")
    
    def do_PUT(self):
        self._handle_request("PUT")
    
    def do_DELETE(self):
        self._handle_request("DELETE")
    
    def _handle_request(self, method: str):
        """Handle HTTP request"""
        # Read body for POST/PUT
        body = ""
        if method in ("POST", "PUT"):
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
        
        # Create request object
        request = Request(method, self.path, dict(self.headers), body)
        
        # Match route
        route = self.router.match_route(method, request.path)
        
        if not route:
            self._send_error(404, "Not Found")
            return
        
        # Create response object
        response = Response()
        
        try:
            # Execute middleware
            for middleware in self.router.middleware:
                middleware(request, response)
            
            # Execute route handler
            route.handler(request, response)
            
            # Send response
            self._send_response(response)
        
        except Exception as e:
            self._send_error(500, f"Internal Server Error: {str(e)}")
    
    def _send_response(self, response: Response):
        """Send HTTP response"""
        self.send_response(response.status_code)
        
        for key, value in response.headers.items():
            self.send_header(key, value)
        
        self.end_headers()
        self.wfile.write(response.body.encode('utf-8'))
    
    def _send_error(self, code: int, message: str):
        """Send error response"""
        self.send_response(code)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head><title>Error {code}</title></head>
        <body>
            <h1>{code} - {message}</h1>
        </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override to customize logging"""
        print(f"[{self.log_date_time_string()}] {format % args}")

class WebServer:
    """Mythos Web Server"""
    def __init__(self, host: str = "localhost", port: int = 8000):
        self.host = host
        self.port = port
        self.router = Router()
        self.server: Optional[HTTPServer] = None
    
    def route(self, path: str, method: str = "GET"):
        """Decorator for adding routes"""
        def decorator(handler: Callable):
            self.router.add_route(method, path, handler)
            return handler
        return decorator
    
    def get(self, path: str):
        """Decorator for GET routes"""
        return self.route(path, "GET")
    
    def post(self, path: str):
        """Decorator for POST routes"""
        return self.route(path, "POST")
    
    def use(self, middleware: Callable):
        """Add middleware"""
        self.router.use(middleware)
    
    def start(self):
        """Start the server"""
        MythosHTTPHandler.router = self.router
        self.server = HTTPServer((self.host, self.port), MythosHTTPHandler)
        
        print(f"Mythos Web Server running at http://{self.host}:{self.port}")
        print("Press Ctrl+C to stop")
        
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            self.stop()
    
    def stop(self):
        """Stop the server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            print("Server stopped")

# Helper function to create web app
def create_app(host: str = "localhost", port: int = 8000) -> WebServer:
    """Create a new web application"""
    return WebServer(host, port)
