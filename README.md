# Automatic Test Case Generator

## Overview
This script scans a given project directory (`Project_test_folder/`) for Python files, extracts function definitions, and generates `pytest` unit tests using OpenAI's GPT-4o model. The generated test files are stored in the `tests/` directory.

## Features
- **Automatic Function Detection**: Scans `.py` files and extracts function names.
- **LLM-Based Test Generation**: Uses GPT-4o to generate `pytest` test cases.
- **Syntax Validation**: Ensures the generated tests are syntactically correct.
- **Progress Tracking**: Displays progress using `tqdm`.

## Prerequisites
### Install Dependencies
Ensure you have Python installed and set up a virtual environment if needed.
```bash
pip install openai pytest tqdm python-dotenv
```

### Set Up OpenAI API Key
Create a `.env` file in the root directory and add your OpenAI API key:
```plaintext
OPENAI_API_KEY=your_openai_api_key
```

## Usage
### 1. Add Your Python Files
Ensure that the directory `Project_test_folder/` contains the Python files you want to generate tests for.

Example structure:
```
Project_test_folder/
│── module1.py
│── module2.py
│── utils.py
```

### 2. Run the Script
Execute the script to scan and generate test cases:
```bash
python auto_test_creator.py
```

### 3. Run the Generated Tests
Once the test files are generated in the `tests/` directory, execute them using `pytest`:
```bash
pytest tests/
```

## Example Output
```plaintext
📂 Scanning directory: Project_test_folder/
✔ Found 3 function(s) in module1.py
✔ Found 2 function(s) in module2.py

📝 Creating test file for module1.py (3 functions)
✅ Generated test file: tests/test_module1.py

📝 Creating test file for module2.py (2 functions)
✅ Generated test file: tests/test_module2.py

🎉 Test case generation complete! Run `pytest tests/` to execute the tests.
```

## Customization
- Modify `project_dir` in `main()` to change the target directory.
- Adjust the prompt in `generate_tests()` to refine test case generation.

## License
This project is open-source and can be modified as needed.

## Support
For issues, open a GitHub issue or contact the maintainer.

