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



class TestScanner:
    def __init__(self, project_dir):
        self.project_dir = os.path.abspath(project_dir)
        self.functions = {}

    def scan_project(self):
        python_files = []
        for root, _, files in os.walk(self.project_dir):
            for file in files:
                if file.endswith(".py") and not file.startswith("test_"):
                    file_path = os.path.join(root, file)
                    python_files.append(file_path)

        for file_path in tqdm(python_files, desc="Scanning files", unit="file"):
            self.extract_functions(file_path)
        return self.functions

    def extract_functions(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                tree = ast.parse(f.read(), filename=file_path)
            except SyntaxError as e:
                st.session_state["errors"].append(f"Syntax error in {file_path}: {e}")
                return

        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        if functions:
            self.functions[file_path] = functions

class TestGenerator:
    def __init__(self, project_dir,model="gpt-4o", api_key=OPENAI_API_KEY):
        self.project_dir = os.path.abspath(project_dir)
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def clean_generated_code(self, test_code):
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
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        file_path = Path(uploaded_file.name).resolve()
        selected_directory = find_closest_folder(file_path)
        st.session_state['project_dir']=selected_directory
        os.remove(file_path)

if st.button("Refresh"):
    st.session_state["scanned_expander_open"] = False
    st.session_state["test_expander_open"] = False
    st.session_state['project_dir']=""
    

if st.session_state['project_dir']!="":


    st.write(f"Selected Project Directory: {st.session_state['project_dir']}")


    if st.button("Scan Project"):
        scanner = TestScanner(st.session_state["project_dir"])
        st.session_state["functions"] = scanner.scan_project()
        st.session_state["scanned_expander_open"] = True  # Keep expander open after scanning
        st.success("Scanning complete!")
        st.session_state["test_expander_open"] = True

    if st.session_state["scanned_expander_open"]:
        with st.expander("📂 Scanned Functions Summary", expanded=True):  # Keep it open
            for file, funcs in st.session_state["functions"].items():
                st.write(f"### {os.path.basename(file)}")
                st.write(", ".join(funcs))

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
                
                

