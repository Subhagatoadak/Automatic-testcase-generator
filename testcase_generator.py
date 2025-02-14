import os
import ast
import openai
from dotenv import load_dotenv
from tqdm import tqdm
import re

# Load environment variables
load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

import os
import ast
import openai
from dotenv import load_dotenv
from tqdm import tqdm
import re

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class TestScanner:
    """
    Scans Python files in a project directory and extracts functions and classes for test generation.
    """
    def __init__(self, project_dir):
        self.project_dir = os.path.abspath(project_dir)
        self.functions = {}
        self.classes = {}
        self.ast_trees = {}

    def scan_project(self):
        """
        Recursively scans the project directory for Python files and extracts functions and class methods.
        """
        print(f"\n📂 Scanning directory: {self.project_dir}")
        if not os.path.exists(self.project_dir):
            print(f"❌ Error: Directory '{self.project_dir}' does not exist!")
            exit(1)

        python_files = []
        for root, _, files in os.walk(self.project_dir):
            for file in files:
                if file.endswith(".py") and not file.startswith("test_") and file != "__init__.py":  # Exclude __init__.py
                    file_path = os.path.join(root, file)
                    python_files.append(file_path)

        if not python_files:
            print("⚠️ No Python files found!")
            return

        for file_path in tqdm(python_files, desc="📄 Processing files", unit="file"):
            self.extract_definitions(file_path)

        return self.functions, self.classes, self.ast_trees

    def extract_definitions(self, file_path):
        """
        Extracts function and class definitions from a Python file.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                content = f.read()
                tree = ast.parse(content, filename=file_path)
                self.ast_trees[file_path] = self.get_clean_ast(tree)  # Cleaned AST tree
            except SyntaxError as e:
                print(f"❌ Syntax error in {file_path}: {e}")
                return

        # Extract functions, excluding __init__
        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name != "__init__"]

        # Extract classes
        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

        if functions:
            self.functions[file_path] = functions
        if classes:
            self.classes[file_path] = classes

    def get_clean_ast(self, tree):
        """
        Returns a cleaned-up version of the AST showing class-method hierarchy.
        Excludes __init__ methods inside classes.
        """
        structure = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_info = f"📂 Class: {node.name}"
                methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef) and n.name != "__init__"]  # Exclude __init__
                if methods:
                    class_info += "\n  ├── Methods: " + ", ".join(methods)
                structure.append(class_info)

            elif isinstance(node, ast.FunctionDef) and not any(isinstance(n, ast.ClassDef) for n in ast.walk(node)) and node.name != "__init__":
                # Standalone functions (not inside a class) - Exclude __init__
                structure.append(f"📄 Function: {node.name}")

        return "\n".join(structure) if structure else "No classes or functions found."

    def get_functions(self):
        """
        Returns a dictionary with file paths as keys and function names as values.
        """
        return self.functions



class TestGenerator:
    """
    Uses an LLM to generate pytest-compatible test cases for scanned functions.
    """
    def __init__(self, project_dir, model="gpt-4o", api_key=OPENAI_API_KEY):
        self.project_dir = os.path.abspath(project_dir)
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def clean_generated_code(self, test_code):
        """
        Removes unwanted markdown syntax (e.g., ```python and ```)
        """
        return re.sub(r'```[a-zA-Z]*', '', test_code).strip()

    def read_file_content(self, file_path):
        """
        Reads the content of a given Python file.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            return None

    def generate_tests(self, file_path, functions):
        """
        Generates pytest unit tests for multiple functions in a single request.
        """
        if os.path.basename(file_path) == "__init__.py":  # Skip __init__.py
            return None 
        
        file_content = self.read_file_content(file_path)
        if file_content is None:
            return "Error reading file."

        prompt = f"""
        Below is the content (between ```python and ```) of a Python file named '{file_path}':
        
        ```python
        {file_content}
        ```

        Generate pytest unit tests for the following functions: {', '.join(functions)}.
        Each function should be tested for:
        - Correct input and expected output
        - Edge cases
        - Error handling

        Ensure the tests follow pytest best practices.
        Do NOT include explanations or comments.
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        return self.clean_generated_code(response.choices[0].message.content.strip())

    def validate_test_code(self, test_code):
        """
        Validates the generated test code to ensure there are no syntax errors.
        """
        try:
            ast.parse(test_code)
            return True
        except SyntaxError as e:
            print(f"❌ Syntax error in generated test code: {e}")
            return False

    def create_test_file(self, file_path, functions):
        """
        Generates a test file with pytest test cases for all functions in a file.
        """
        if os.path.basename(file_path) == "__init__.py":
            return None  # Skip __init__.py

        test_code = self.generate_tests(file_path, functions)
        
        if test_code is None:
            return
        
        if self.validate_test_code(test_code):
            test_content = test_code
        else:
            print(f"⚠️ Skipping file '{file_path}' due to syntax errors in generated test.")
            return
        
        test_file_name = f"test_{os.path.basename(file_path)}"
        test_file_path = os.path.join(self.project_dir, "tests", test_file_name)
        os.makedirs(os.path.dirname(test_file_path), exist_ok=True)

        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write(test_content)

        print(f"✅ Generated test file: {test_file_path}")



def main():
    project_dir = "Project_test_folder/"  # Set your project directory

    scanner = TestScanner(project_dir)
    scanner.scan_project()

    test_generator = TestGenerator(project_dir)

    function_data = scanner.get_functions()
    if not function_data:
        print("⚠️ No functions found for test generation.")
        return

    for file_path, functions in function_data.items():
        print(f"\n📝 Creating test file for {file_path} ({len(functions)} functions)")
        test_generator.create_test_file(file_path, functions)

    print("\n🎉 Test case generation complete! Run `pytest tests/` to execute the tests.")


if __name__ == "__main__":
    main()
