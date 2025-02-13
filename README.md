# Automatic Test Case Generator

## Overview
The **Automatic Test Case Generator** is a Streamlit-based application that scans Python projects, extracts function definitions, and generates unit test cases using OpenAI's GPT model. The generated tests follow `pytest` best practices and aim to cover various scenarios, including correct inputs, edge cases, and error handling.

## Features
- **Project Scanning**: Identifies Python files and extracts function definitions.
- **AI-Powered Test Generation**: Uses OpenAI's API to generate `pytest` unit tests.
- **Interactive UI**: Users can scan projects, generate tests, and edit test files within the Streamlit interface.
- **Error Handling**: Detects syntax errors in scanned files.

## Technologies Used
- **Python**
- **Streamlit** (for UI)
- **OpenAI API** (for test case generation)
- **Ast Module** (for Python syntax analysis)
- **OS & Pathlib** (for file system operations)
- **Pytest** (for running generated test cases)

## Installation
### Prerequisites
Ensure you have Python 3.8+ installed on your system.

### Step 1: Clone the Repository
```sh
 git clone https://github.com/your-username/automatic-test-case-generator.git
 cd automatic-test-case-generator
```

### Step 2: Create and Activate a Virtual Environment
```sh
 python -m venv venv
 source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```sh
 pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables
Create a `.env` file in the root directory and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage
### 1. Run the Application
```sh
 streamlit run app.py
```

### 2. Upload a File
- Upload any Python file from your project to determine its path.
- The closest project directory is automatically selected.

### 3. Scan the Project
- Click **"Scan Project"** to detect Python functions across your project.
- A summary of discovered functions will be displayed.

### 4. Generate Test Cases
- Click **"Generate Tests"** to create test files.
- Test cases are stored in a `tests/` folder.

### 5. Edit and Save Tests
- Modify the generated test files directly within the UI.
- Click **"Save"** to update the test file.

### 6. Handle Errors
- If syntax errors are detected in scanned files, they will be displayed in the UI.

## Folder Structure
```
project_root/
│── tests/                 # Generated test files
│── app.py                 # Streamlit application
│── requirements.txt       # Dependencies
│── .env                   # API key configuration
│── README.md              # Documentation
```

## Example Test Output
Example generated `test_file.py`:
```python
import pytest
from my_module import my_function

def test_my_function():
    assert my_function(2, 3) == 5  # Example correct case
    assert my_function(-1, 1) == 0  # Edge case
    with pytest.raises(TypeError):
        my_function("string", 2)  # Error handling
```

## Troubleshooting
- **OpenAI API Error**: Check your API key in `.env`.
- **File Not Found**: Ensure the uploaded file exists and is accessible.
- **No Functions Found**: Verify that the Python files contain valid function definitions.

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests.

## License
This project is licensed under the MIT License.