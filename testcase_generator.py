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

class TestScanner:
    """
    Scans Python files in a project directory and extracts methods to generate tests.
    """
    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.functions = {}

    def scan_project(self):
        """
        Recursively scans the project directory for Python files and extracts function names.
        """
        print(f"\n📂 Scanning directory: {self.project_dir}")
        if not os.path.exists(self.project_dir):
            print(f"❌ Error: Directory '{self.project_dir}' does not exist!")
            exit(1)

        python_files = []
        for root, _, files in os.walk(self.project_dir):
            for file in files:
                if file.endswith(".py") and not file.startswith("test_"):
                    file_path = os.path.join(root, file)
                    python_files.append(file_path)

        if not python_files:
            print("⚠️ No Python files found!")
            return

        for file_path in tqdm(python_files, desc="📄 Processing files", unit="file"):
            self.extract_functions(file_path)

    def extract_functions(self, file_path):
        """
        Extracts function names from a given Python file.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                tree = ast.parse(f.read(), filename=file_path)
            except SyntaxError as e:
                print(f"❌ Syntax error in {file_path}: {e}")
                return

        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        if functions:
            self.functions[file_path] = functions
            print(f"✔ Found {len(functions)} function(s) in {file_path}")

    def get_functions(self):
        """
        Returns a dictionary with file paths as keys and function names as values.
        """
        return self.functions


class TestGenerator:
    """
    Uses an LLM to generate pytest-compatible test cases for scanned functions.
    """
    def __init__(self, project_dir,model="gpt-4o", api_key=OPENAI_API_KEY):
        self.project_dir = project_dir
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
    
    def clean_generated_code(self, test_code):
        """
        Removes unwanted markdown syntax (e.g., ```python and ```)
        """
        return re.sub(r'```[a-zA-Z]*', '', test_code).strip()

    def generate_tests(self, file_path, functions):
        """
        Generates pytest test cases for multiple functions in a single request.
        """
        prompt = f"""
        Generate pytest unit tests for the following functions in the file '{file_path}': {', '.join(functions)}.
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
        module_path = file_path.replace("/", ".").replace(".py", "")
        #test_content = f"import pytest\nfrom {module_path} import *\n\n"

        test_code = self.generate_tests(file_path, functions)
        
        
        if self.validate_test_code(test_code):
            test_content = test_code 
        else:
            print(f"⚠️ Skipping file '{file_path}' due to syntax errors in generated test.")
            return
        
        test_file_name = f"test_{os.path.basename(file_path)}"
        test_file_path = os.path.join(self.project_dir,"tests", test_file_name)
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
