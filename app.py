import os
import ast
import openai
import streamlit as st
from dotenv import load_dotenv
from tqdm import tqdm
import re
import tempfile
from pathlib import Path

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Streamlit app config
st.set_page_config(page_title="Automatic Test Case Generator", layout="wide")

# Session state
# Session state
if "functions" not in st.session_state:
    st.session_state["functions"] = {}
if "test_files" not in st.session_state:
    st.session_state["test_files"] = {}
if "errors" not in st.session_state:
    st.session_state["errors"] = []
if "project_dir" not in st.session_state:
    st.session_state["project_dir"] = ""
if "saved_files" not in st.session_state:
    st.session_state["saved_files"] = {}

if "scanned_expander_open" not in st.session_state:
    st.session_state["scanned_expander_open"] = False
    
if "test_expander_open" not in st.session_state:
    st.session_state["test_expander_open"] = False



import ast
import os
import streamlit as st
from tqdm import tqdm

class TestScanner:

    def __init__(self, project_dir):
        self.project_dir = os.path.abspath(project_dir)
        self.functions = {}
        self.classes = {}
        self.ast_trees = {}

    def scan_project(self):
        python_files = []
        for root, _, files in os.walk(self.project_dir):
            for file in files:
                if file.endswith(".py") and not file.startswith("test_") and file != "__init__.py":  # Skip __init__.py
                    file_path = os.path.join(root, file)
                    python_files.append(file_path)

        for file_path in tqdm(python_files, desc="Scanning files", unit="file"):
            self.extract_definitions(file_path)

        return self.functions, self.classes, self.ast_trees

    def extract_definitions(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                content = f.read()
                tree = ast.parse(content, filename=file_path)
                self.ast_trees[file_path] = self.get_clean_ast(tree)  # Cleaned AST tree
            except SyntaxError as e:
                st.session_state["errors"].append(f"Syntax error in {file_path}: {e}")
                return

        # Extract functions (excluding __init__)
        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

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
                methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]  # Exclude __init__
                if methods:
                    class_info += "\n  ├── Methods: " + ", ".join(methods)
                structure.append(class_info)

            elif isinstance(node, ast.FunctionDef) and not any(isinstance(n, ast.ClassDef) for n in ast.walk(node)):
                # Standalone functions (not inside a class)
                structure.append(f"📄 Function: {node.name}")

        return "\n".join(structure) if structure else "No classes or functions found."

            
            
class TestGenerator:
    def __init__(self, project_dir,model="gpt-4o", api_key=OPENAI_API_KEY):
        self.project_dir = os.path.abspath(project_dir)
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def clean_generated_code(self, test_code):
        return re.sub(r'```[a-zA-Z]*', '', test_code).strip()

    def read_file_content(self, file_path):
        """Reads the content of a given Python file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            st.session_state["errors"].append(f"Error reading {file_path}: {e}")
            return None

    def generate_tests(self, file_path, functions):
        """
        Generates pytest test cases for multiple functions in a single request.
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

    def create_test_file(self, file_path, functions):
        test_code = self.generate_tests(file_path, functions)
        test_file_name = f"test_{os.path.basename(file_path)}"
        test_file_path = os.path.join(self.project_dir,"tests", test_file_name)
        os.makedirs(os.path.dirname(test_file_path), exist_ok=True)
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write(test_code)
        return test_file_path

def find_closest_folder(file_path):
    """Finds the closest subfolder containing files starting from the uploaded file's directory."""
    directory = file_path.parent
    subfolders = [sub for sub in directory.iterdir() if sub.is_dir()]
    print(subfolders)
    for subfolder in subfolders:
        print(os.path.abspath(subfolder))
        if file_path.name in os.listdir(os.path.abspath(subfolder)):
            return subfolder
    return directory  # Return parent directory if not in any subfolder


# Streamlit UI
st.title("Automatic Test Case Generator")




st.header('Default Options')
uploaded_file = st.file_uploader("Upload a file from the desired directory to get its path", type=None)
    
if uploaded_file is not None:
         # Save file temporarily to retrieve its absolute path
        #with open(uploaded_file.name, "wb") as f:
        #    f.write(uploaded_file.getbuffer())
        
        file_path = Path(uploaded_file.name).resolve()
        selected_directory = find_closest_folder(file_path)
        st.session_state['project_dir']=selected_directory
        #os.remove(file_path)

if st.button("Refresh"):
    st.session_state["scanned_expander_open"] = False
    st.session_state["test_expander_open"] = False
    st.session_state['project_dir']=""
    

if st.session_state['project_dir']!="":


    st.write(f"Selected Project Directory: {st.session_state['project_dir']}")


    if st.button("Scan Project"):
        scanner = TestScanner(st.session_state["project_dir"])
        functions, classes, ast_trees = scanner.scan_project()
        st.session_state["functions"] = functions
        st.session_state["classes"] = classes
        st.session_state["ast_trees"] = ast_trees
        st.session_state["scanned_expander_open"] = True
        st.success("Scanning complete!")
        st.session_state["test_expander_open"] = True

    if st.session_state["scanned_expander_open"]:
        with st.expander("📂 Scanned Code Summary", expanded=True):
            for file, funcs in st.session_state["functions"].items():
                # Skip displaying __init__.py
                if os.path.basename(file) == "__init__.py":
                    continue
                
                st.write(f"### {os.path.basename(file)}")

                # Display functions
                if funcs:
                    st.write("**Functions:**")
                    st.write(", ".join(funcs))

                # Display classes
                if file in st.session_state["classes"] and st.session_state["classes"][file]:
                    st.write("**Classes:**")
                    st.write(", ".join(st.session_state["classes"][file]))

                # Display cleaned AST tree
                if file in st.session_state["ast_trees"]:
                    st.write(f"📜 **Class-Method Hierarchy for {os.path.basename(file)}:**")
                    st.code(st.session_state["ast_trees"][file], language="plaintext")

                        
    if st.button("Generate Tests"):
        st.session_state["scanned_expander_open"] = True 
        with st.spinner("Generating test cases..."):
            generator = TestGenerator(st.session_state["project_dir"])
            for file, funcs in st.session_state["functions"].items():
                test_path = generator.create_test_file(file, funcs)
                st.session_state["test_files"][file] = test_path
            st.success("Test cases generated successfully!")

        st.session_state["test_expander_open"] = True  # Keep expander open
        
    if st.session_state["test_expander_open"]:
        with st.expander("📄 Generated Test Files", expanded=True):
            for file, test_file in st.session_state["test_files"].items():
                st.write(f"### {os.path.basename(test_file)}")
                with open(test_file, "r") as f:
                    test_code = f.read()
                edited_code = st.text_area(f"Edit {os.path.basename(test_file)}", test_code, height=200, key=f"edit_{test_file}")
                if st.button(f"Save {os.path.basename(test_file)}", key=f"save_{test_file}"):
                    with open(test_file, "w") as f:
                        f.write(edited_code)
                    st.session_state["saved_files"][test_file] = True
                    st.success(f"Successfully saved {os.path.basename(test_file)}")
                    st.session_state["test_expander_open"] = True  # Keep expander open after saving

        



    if st.session_state["errors"]:
        if st.button("Show Errors"):
            with st.expander("🚨 Errors Detected"):
                st.error("\n".join(st.session_state["errors"]))

else:
    st.warning("Please select a project directory to begin.")
                
                

