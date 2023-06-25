import os


class cd:
    """
    Context manager for changing the current working directory
    credit: https://tinyurl.com/3rzevesc
    """

    def __init__(self, new_path: str):
        self.new_path = os.path.expanduser(new_path)

    def __enter__(self) -> None:
        self.saved_path = os.getcwd()
        os.chdir(self.new_path)

    def __exit__(self, etype, value, traceback):  # type: ignore
        os.chdir(self.saved_path)


def create_directory(directory_path: str) -> None:
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created successfully.")
    else:
        print(f"Directory '{directory_path}' already exists.")


def write_shebang(file_path: str, new_line: str = "\n") -> None:
    with open(file_path, "w") as file:
        file.write("#! /bin/sh" + new_line)


def append_to_file(file_path: str, content: str, new_line: str = "\n") -> None:
    with open(file_path, "a") as file:
        file.write(content + new_line)
