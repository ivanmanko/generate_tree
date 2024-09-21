import os
import argparse
from pathlib import Path
import sys

try:
    import pathspec
except ImportError:
    print("The 'pathspec' library is required for this script to run.")
    print("Please install it using 'pip install pathspec'")
    sys.exit(1)

try:
    from colorama import Fore, Style, init
except ImportError:
    print("The 'colorama' library is required for colored output.")
    print("Please install it using 'pip install colorama'")
    sys.exit(1)

# Initialize colorama
init(autoreset=True)

# Define default exclusion patterns
DEFAULT_IGNORE_PATTERNS = [
    # Exclude Git metadata
    '.git/',
    # Exclude Python cache directories and compiled files
    '__pycache__/',
    '*.pyc',
    # Exclude virtual environments
    'venv/',
    'env/',
    '.venv/',
    # Exclude Node.js modules
    'node_modules/',
    # Exclude IDE and editor directories
    '.vscode/',
    '.idea/',
    # Exclude OS-specific files
    '.DS_Store',
    'Thumbs.db',
    # Exclude logs and temporary files
    'logs/',
    '*.log',
    'tmp/',
    'temp/',
    # Exclude specific files
    'secret_config.yaml',
]

def load_ignore_patterns(ignore_files, default_patterns):
    """
    Load ignore patterns from default patterns and a list of ignore files.

    :param ignore_files: List of Path objects to ignore files.
    :param default_patterns: List of default exclusion patterns.
    :return: Compiled PathSpec object or None if no patterns are loaded.
    """
    patterns = set(default_patterns)

    for ignore_file in ignore_files:
        if ignore_file.exists():
            with ignore_file.open('r') as f:
                file_patterns = f.read().splitlines()
                # Remove empty lines and comments
                file_patterns = [line.strip() for line in file_patterns if line.strip() and not line.strip().startswith('#')]
                patterns.update(file_patterns)
            print(f"Loaded exclusion patterns from '{ignore_file}'.")
        else:
            print(f"Ignore file '{ignore_file}' not found. Skipping.")

    if patterns:
        spec = pathspec.PathSpec.from_lines('gitwildmatch', patterns)
        return spec
    return None

def should_ignore(path, spec, initial_root_dir):
    """
    Determine if a given path should be ignored based on the PathSpec.

    :param path: Path to check.
    :param spec: Compiled PathSpec object.
    :param initial_root_dir: Initial root directory for relative paths.
    :return: True if the path should be ignored, False otherwise.
    """
    if spec is None:
        return False

    # Compute the relative path from the initial root directory
    try:
        rel_path = os.path.relpath(path, initial_root_dir)
    except ValueError:
        # If path is on a different drive (Windows), relpath raises ValueError
        return False

    # pathspec expects POSIX-style paths
    rel_path_posix = rel_path.replace(os.sep, '/')
    return spec.match_file(rel_path_posix)

def generate_tree(current_dir, prefix, spec, visited, initial_root_dir, use_color):
    """
    Recursively generates and prints the directory tree structure.

    :param current_dir: The current directory being traversed.
    :param prefix: The prefix string used for formatting.
    :param spec: Compiled PathSpec object for exclusion.
    :param visited: Set of visited directories to prevent infinite loops.
    :param initial_root_dir: The initial root directory for relative paths.
    :param use_color: Boolean indicating whether to use color in output.
    """
    if visited is None:
        visited = set()

    real_path = os.path.realpath(current_dir)
    if real_path in visited:
        display_name = f"{os.path.basename(current_dir)}/ (symlink loop)"
        if use_color:
            display_name = Fore.MAGENTA + display_name + Style.RESET_ALL
        print(prefix + "└── " + display_name)
        return
    visited.add(real_path)

    try:
        items = sorted(os.listdir(current_dir))
    except PermissionError:
        display_name = "Permission Denied"
        if use_color:
            display_name = Fore.RED + display_name + Style.RESET_ALL
        print(prefix + "└── " + display_name)
        return

    for index, item in enumerate(items):
        path = os.path.join(current_dir, item)

        if should_ignore(path, spec, initial_root_dir):
            continue  # Skip ignored files/directories

        # Determine the connector based on position
        connector = "├── " if index < len(items) - 1 else "└── "
        is_last = index == len(items) - 1
        new_prefix = prefix + ("    " if is_last else "│   ")

        # Handle symbolic links
        if os.path.islink(path):
            try:
                target_path = os.readlink(path)
            except OSError:
                target_path = "unreachable"
            display_name = f"{item}@ -> {target_path}"
            if use_color:
                display_name = Fore.MAGENTA + display_name + Style.RESET_ALL
            print(prefix + connector + display_name)
            continue

        # Check if directory is a Python package
        if os.path.isdir(path):
            try:
                dir_contents = os.listdir(path)
            except PermissionError:
                dir_contents = []
            if "__init__.py" in dir_contents:
                # Python package
                display_name = f"{item}/"
                if use_color:
                    display_name = Fore.BLUE + display_name + Style.RESET_ALL
            else:
                # Regular directory
                display_name = f"{item}/"
                if use_color:
                    display_name = Fore.CYAN + display_name + Style.RESET_ALL
            print(prefix + connector + display_name)
            generate_tree(path, new_prefix, spec, visited, initial_root_dir, use_color)
        else:
            # Regular file
            display_name = f"{item}"
            if use_color:
                display_name = Fore.GREEN + display_name + Style.RESET_ALL
            print(prefix + connector + display_name)

def main():
    parser = argparse.ArgumentParser(
        description="Generate a tree-like structure of a directory with exclusion support using .treeignore and .gitignore."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="The root directory to generate the tree from. Defaults to the current directory."
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Path to a file to save the tree structure. If not provided, it will be printed to the console."
    )
    args = parser.parse_args()

    root_dir = os.path.abspath(args.directory)

    if not os.path.exists(root_dir):
        print(f"Error: The directory '{root_dir}' does not exist.")
        sys.exit(1)

    # Define ignore files: .treeignore and .gitignore
    ignore_files = [Path(root_dir) / ".treeignore", Path(root_dir) / ".gitignore"]

    # Load exclusion patterns from both .treeignore and .gitignore, plus default patterns
    spec = load_ignore_patterns(ignore_files, DEFAULT_IGNORE_PATTERNS)

    if spec:
        print("Exclusion patterns loaded from '.treeignore' and '.gitignore'.")
    else:
        print(f"No '.treeignore' or '.gitignore' file found in '{root_dir}'. Proceeding without exclusions.")

    # Determine if color should be used (only if output is to console)
    use_color = sys.stdout.isatty()

    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                original_stdout = sys.stdout
                sys.stdout = f
                print(os.path.basename(root_dir) + "/")
                generate_tree(root_dir, "", spec, visited=None, initial_root_dir=root_dir, use_color=False)
                sys.stdout = original_stdout
            print(f"Tree structure saved to '{args.output}'.")
        except Exception as e:
            print(f"Failed to write to output file '{args.output}': {e}")
            sys.exit(1)
    else:
        print(os.path.basename(root_dir) + "/")
        generate_tree(root_dir, "", spec, visited=None, initial_root_dir=root_dir, use_color=use_color)

if __name__ == "__main__":
    main()
