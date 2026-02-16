"""
Mythos CLI - Command-line interface for Mythos
"""
import sys
import os
import argparse
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.bytecode.compiler import BytecodeCompiler
from runtime.vm import VirtualMachine

class MythosCLI:
    """Mythos command-line interface"""
    
    def __init__(self):
        self.version = "1.0.0"
        self.parser = self._create_parser()
    
    def _create_parser(self):
        """Create argument parser"""
        parser = argparse.ArgumentParser(
            prog='mythos',
            description='Mythos Programming Language',
            epilog='For more information, visit https://mythos-lang.org'
        )
        
        parser.add_argument('--version', action='version', version=f'Mythos {self.version}')
        
        subparsers = parser.add_subparsers(dest='command', help='Commands')
        
        # Run command
        run_parser = subparsers.add_parser('run', help='Run a Mythos file')
        run_parser.add_argument('file', help='Mythos file to run')
        run_parser.add_argument('--debug', action='store_true', help='Enable debug mode')
        
        # Build command
        build_parser = subparsers.add_parser('build', help='Build a Mythos project')
        build_parser.add_argument('file', help='Mythos file to build')
        build_parser.add_argument('-o', '--output', help='Output file')
        
        # Web command
        web_parser = subparsers.add_parser('web', help='Start web server')
        web_parser.add_argument('file', help='Mythos web app file')
        web_parser.add_argument('-p', '--port', type=int, default=8000, help='Port number')
        web_parser.add_argument('--host', default='localhost', help='Host address')
        
        # Game command
        game_parser = subparsers.add_parser('game', help='Run a Mythos game')
        game_parser.add_argument('file', help='Mythos game file')
        game_parser.add_argument('--fullscreen', action='store_true', help='Run in fullscreen')
        
        # REPL command
        subparsers.add_parser('repl', help='Start interactive REPL')
        
        # Init command
        init_parser = subparsers.add_parser('init', help='Initialize a new Mythos project')
        init_parser.add_argument('name', help='Project name')
        init_parser.add_argument('--type', choices=['web', 'game', 'cli'], default='cli', help='Project type')
        
        return parser
    
    def run(self, args=None):
        """Run the CLI"""
        args = self.parser.parse_args(args)
        
        if not args.command:
            self.parser.print_help()
            return
        
        if args.command == 'run':
            self.run_file(args.file, args.debug)
        elif args.command == 'build':
            self.build_file(args.file, args.output)
        elif args.command == 'web':
            self.run_web(args.file, args.host, args.port)
        elif args.command == 'game':
            self.run_game(args.file, args.fullscreen)
        elif args.command == 'repl':
            self.start_repl()
        elif args.command == 'init':
            self.init_project(args.name, args.type)
    
    def run_file(self, filename: str, debug: bool = False):
        """Run a Mythos file"""
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found")
            sys.exit(1)
        
        try:
            with open(filename, 'r') as f:
                source = f.read()
            
            # Compile
            if debug:
                print("Compiling...")
            
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            
            if debug:
                print(f"Tokens: {len(tokens)}")
                for token in tokens[:10]:  # Show first 10 tokens
                    print(f"  {token}")
            
            parser = Parser(tokens)
            ast = parser.parse()
            
            if debug:
                print(f"AST nodes: {len(ast.statements)}")
            
            compiler = BytecodeCompiler()
            compiler.compile(ast)
            bytecode = compiler.get_bytecode()
            
            if debug:
                print(f"Instructions: {len(bytecode['instructions'])}")
                print(f"Constants: {bytecode['constants']}")
                print("\nBytecode:")
                for i, instr in enumerate(bytecode['instructions']):
                    print(f"  {i}: {instr}")
            
            # Execute
            if debug:
                print("\nExecuting...")
            
            vm = VirtualMachine()
            vm.execute(bytecode['instructions'], bytecode['constants'])
            
            if debug:
                print("Execution complete")
        
        except Exception as e:
            print(f"Error: {e}")
            if debug:
                import traceback
                traceback.print_exc()
            sys.exit(1)
    
    def build_file(self, filename: str, output: str = None):
        """Build a Mythos file to bytecode"""
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found")
            sys.exit(1)
        
        if not output:
            output = filename.replace('.mythos', '.mythosb')
        
        try:
            with open(filename, 'r') as f:
                source = f.read()
            
            # Compile
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            ast = parser.parse()
            compiler = BytecodeCompiler()
            compiler.compile(ast)
            bytecode = compiler.get_bytecode()
            
            # Save bytecode
            import pickle
            with open(output, 'wb') as f:
                pickle.dump(bytecode, f)
            
            print(f"Built successfully: {output}")
        
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    def run_web(self, filename: str, host: str, port: int):
        """Run a Mythos web application"""
        print(f"Starting web server at http://{host}:{port}")
        print("Press Ctrl+C to stop")
        
        # This would integrate with the web server
        self.run_file(filename)
    
    def run_game(self, filename: str, fullscreen: bool):
        """Run a Mythos game"""
        print(f"Starting game: {filename}")
        if fullscreen:
            print("Running in fullscreen mode")
        
        # This would integrate with the game engine
        self.run_file(filename)
    
    def start_repl(self):
        """Start interactive REPL"""
        print(f"Mythos {self.version} REPL")
        print("Type 'exit' to quit")
        
        vm = VirtualMachine()
        
        while True:
            try:
                line = input(">>> ")
                
                if line.strip() in ('exit', 'quit'):
                    break
                
                if not line.strip():
                    continue
                
                # Compile and execute
                lexer = Lexer(line)
                tokens = lexer.tokenize()
                parser = Parser(tokens)
                ast = parser.parse()
                compiler = BytecodeCompiler()
                compiler.compile(ast)
                bytecode = compiler.get_bytecode()
                
                result = vm.execute(bytecode['instructions'], bytecode['constants'])
                
                if result is not None:
                    print(result)
            
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
            except Exception as e:
                print(f"Error: {e}")
    
    def init_project(self, name: str, project_type: str):
        """Initialize a new Mythos project"""
        print(f"Creating {project_type} project: {name}")
        
        # Create project directory
        os.makedirs(name, exist_ok=True)
        
        # Create main file
        main_file = os.path.join(name, 'main.mythos')
        
        if project_type == 'web':
            template = """# Mythos Web Application

web.app {
  route "/" {
    page = ui.page("My Mythos App")
    page.add(ui.text("Welcome to Mythos!", "h1"))
    page.add(ui.text("Start building your web app here.", "p"))
    return page.render()
  }
}

web.start(port: 8000)
"""
        elif project_type == 'game':
            template = """# Mythos Game

scene main {
  camera position:(0, 5, 10) lookAt:(0, 0, 0)
  light sun type:directional intensity:1.0
  cube size:1 position:(0, 0, 0) color:#FF0000
}

function update(dt) {
  # Game logic here
}

game.start()
"""
        else:  # cli
            template = """# Mythos CLI Application

print("Hello from Mythos!")

function main() {
  # Your code here
}

main()
"""
        
        with open(main_file, 'w') as f:
            f.write(template)
        
        print(f"Project created successfully!")
        print(f"Run with: mythos run {name}/main.mythos")

def main():
    """Main entry point"""
    cli = MythosCLI()
    cli.run()

if __name__ == '__main__':
    main()
