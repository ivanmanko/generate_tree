# Directory Tree Generator

![License](https://img.shields.io/github/license/ivanmanko/generate_tree)
![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)

A versatile Python script to generate a tree-like representation of any directory structure, with support for exclusion patterns defined in both `.gitignore` and `.treeignore` files. Perfect for documenting project structures, visualizing directories, and sharing insights about your codebase.

## Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
  - [Advanced Options](#advanced-options)
- [Examples](#examples)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Recursive Directory Traversal:** Explore all subdirectories and files from any root directory.
- **Exclusion Support:** Utilize both `.gitignore` and `.treeignore` files to exclude specific files and folders.
- **Default Exclusions:** Automatically excludes common directories like `.git/`, `__pycache__/`, and others.
- **Color-Coded Output:** Differentiate between directories, Python packages, files, and symbolic links with colors for enhanced readability when outputting to the console.
- **Output to File:** Save the generated tree structure to a text file without ANSI color codes.
- **Symbolic Link Handling:** Detect and display symbolic links, preventing infinite loops.
- **Cross-Platform Compatibility:** Works seamlessly on Windows, macOS, and Linux.

## Demo

![Demo Screenshot](./assets/demo.png)

*Example output of the Directory Tree Generator.*

## Installation

### Prerequisites

- **Python 3.6 or higher** must be installed on your system. You can download it from the [official website](https://www.python.org/downloads/).

### Clone the Repository

```bash
git clone https://github.com/yourusername/directory-tree-generator.git
cd directory-tree-generator
```

### Install Dependencies

It's recommended to use a virtual environment to manage dependencies.

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Alternatively, install the required packages directly:

```bash
pip install pathspec colorama
```

## Usage

The `get_tree.py` script can be run from any directory to visualize its structure.

### Basic Usage

Navigate to the directory you want to visualize and run the script:

```bash
python get_tree.py
```

*This will print the directory tree to the console, excluding the `.git` directory and any patterns specified in `.gitignore` and `.treeignore` files in the root directory.*

### Advanced Options

```bash
usage: get_tree.py [-h] [-o OUTPUT] [directory]

Generate a tree-like structure of a directory with exclusion support using .treeignore and .gitignore.

positional arguments:
  directory             The root directory to generate the tree from. Defaults to the current directory.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Path to a file to save the tree structure. If not provided, it will be printed to the console.
```

#### Examples

- **Generate Tree for Current Directory:**

  ```bash
  python get_tree.py
  ```

- **Specify a Different Root Directory:**

  ```bash
  python get_tree.py /path/to/your/project
  ```

- **Save Output to a File:**

  ```bash
  python get_tree.py -o tree_structure.txt
  ```

- **Combine Options:**

  ```bash
  python get_tree.py /path/to/your/project -o project_tree.txt
  ```

## Examples

### Basic Output

```bash
Loaded exclusion patterns from '/home/ivan/ucar/ucar_package/.treeignore'.
Loaded exclusion patterns from '/home/ivan/ucar/ucar_package/.gitignore'.
Exclusion patterns loaded from '.treeignore' and '.gitignore'.
project_root/
├── src/
│   ├── main.py
│   ├── utils.py
│   └── modules/
│       ├── module1.py
│       └── module2.py
├── tests/
│   ├── test_main.py
│   └── test_utils.py
├── .gitignore
├── README.md
└── requirements.txt
```

*Note:* The `.git/` directory and any files or directories matching patterns in `.treeignore` and `.gitignore` are excluded from the output.

### Output Saved to File

After running:

```bash
python get_tree.py -o tree_structure.txt
```

**Content of `tree_structure.txt`:**

```
project_root/
├── src/
│   ├── main.py
│   ├── utils.py
│   └── modules/
│       ├── module1.py
│       └── module2.py
├── tests/
│   ├── test_main.py
│   └── test_utils.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Customization

### Creating and Customizing `.treeignore`

To exclude specific files and directories from the tree output, define your exclusion patterns in a `.treeignore` file located in the root directory of your project.

**Example `.treeignore` File:**

```gitignore
# Additional exclusions
build/
dist/
*.env
```

**Adding Custom Patterns:**

Feel free to add or remove patterns based on your project's requirements. For instance, if you use a different virtual environment directory or have other directories you wish to exclude, simply add them to the `.treeignore` file.

### Handling Nested `.treeignore` Files

Currently, the script only recognizes a single `.treeignore` file in the root directory. If you have nested directories that require their own exclusion patterns, you can:

1. **Manually Add Patterns:** Extend your root `.treeignore` to include nested patterns.

   **Example:**

   ```gitignore
   # Exclude specific nested directories
   nested_dir/.cache/
   nested_dir/temp/
   ```

2. **Modify the Script:** Enhance the script to detect and load multiple `.treeignore` files within subdirectories. This requires more complex logic and is beyond the current scope but can be implemented as an advanced feature.

### Color-Coding Enhancements

The script uses the `colorama` library to color-code different elements for better readability:

- **Blue (`Fore.BLUE`):** Python packages (directories containing `__init__.py`)
- **Cyan (`Fore.CYAN`):** Regular directories
- **Green (`Fore.GREEN`):** Files
- **Magenta (`Fore.MAGENTA`):** Symbolic links and symlink loops
- **Red (`Fore.RED`):** Permission Denied errors

*Note:* Colors are only applied when outputting to the console. When saving to a file using the `-o` option, colors are disabled to prevent ANSI escape sequences from appearing in the output file.

## Troubleshooting

If you encounter issues with the `.git` directory or other patterns not being excluded, follow these steps:

### 1. Verify `.gitignore` and `.treeignore` Content

- **Ensure `.gitignore` Contains `.git/`:**

  ```gitignore
  # Exclude Git metadata
  .git/
  
  # Exclude Python cache
  __pycache__/
  *.pyc
  
  # Exclude virtual environments
  venv/
  env/
  .venv/
  ```

- **Check `.treeignore` Patterns:**

  ```gitignore
  # Additional exclusions
  build/
  dist/
  *.env
  ```

### 2. Confirm Script Execution Context

- **Navigate to the Root Directory:**

  Ensure you are running the script from the root directory where `.gitignore` and `.treeignore` are located.

  ```bash
  cd /path/to/your/project/
  python get_tree.py
  ```

### 3. Check for Hidden Characters or Typos

- Open `.gitignore` and `.treeignore` in a plain text editor.
- Ensure there are no hidden characters or typos.
- Patterns should be correctly specified (e.g., directories end with a slash `/`).

### 4. Update Dependencies

Ensure that both `pathspec` and `colorama` are up-to-date.

```bash
pip install --upgrade pathspec colorama
```

### 5. Ensure Correct Permissions

Verify that the script has permission to read all directories and files.

```bash
ls -l get_tree.py
```

Ensure that you have the necessary read permissions for all directories you want to traverse.

### 6. Test Exclusion Patterns

Add temporary files or directories that match exclusion patterns to verify they are being excluded.

```bash
mkdir test_dir
echo "Test" > test_file.pyc
```

Run the script and ensure `test_dir/` and `test_file.pyc` are excluded from the output.

### 7. Review Script Output Messages

The script prints messages indicating which ignore files were loaded. Confirm that both `.gitignore` and `.treeignore` are being loaded.

**Example Output:**

```
Loaded exclusion patterns from '/home/ivan/ucar/ucar_package/.treeignore'.
Loaded exclusion patterns from '/home/ivan/ucar/ucar_package/.gitignore'.
Exclusion patterns loaded from '.treeignore' and '.gitignore'.
ucar_package/
├── run.py
├── ucar/
│   ├── __init__.py
│   ├── application.py
│   ├── core.py
│   ├── database.py
│   ├── models.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── jwt_auth_service.py
│   │   ├── registration.py
│   │   ├── authorization.py
│   │   ├── employers.py
│   │   └── protected_service.py
│   └── transport/
│       ├── __init__.py
│       ├── http/
│       │   └── __init__.py
│       └── jwt_auth/
│           ├── __init__.py
│           ├── auth.py
│           ├── jwt_auth_roles.py
│           ├── schemas.py
│           ├── utils.py
│           └── config.py
└── other_dir/
    ├── file1.txt
    └── file2.py
```

### 8. Verify Relative Path Calculation

Ensure that the script correctly calculates relative paths from the initial root directory, which is essential for accurate pattern matching.

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository:**

   Click the "Fork" button at the top right of the repository page.

2. **Create a New Branch:**

   ```bash
   git checkout -b feature/YourFeatureName
   ```

3. **Make Your Changes:**

   Implement your feature or fix.

4. **Commit Your Changes:**

   ```bash
   git commit -m "Add feature: YourFeatureName"
   ```

5. **Push to the Branch:**

   ```bash
   git push origin feature/YourFeatureName
   ```

6. **Create a Pull Request:**

   Navigate to the repository on GitHub and click "Compare & pull request."

## License

This project is licensed under the [MIT License](LICENSE).

---

*Developed with ❤️ by [Ivan Manko](https://github.com/ivanmanko)*
